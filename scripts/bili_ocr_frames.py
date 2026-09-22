#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bili_ocr_frames.py —— 对 B站 画面帧目录做批量 OCR，结果缓存成 jsonl，可增量续跑。

背景
----
本库大量取证依赖「读画面帧」（`bili_analyze.py` 抽的 jpg）。此前只能逐帧人读，
一个 296 帧的目录要读几十次；有了离线 OCR（`rapidocr-onnxruntime`）后可一次性把
全部帧的文字抽出来，再用正则捞关键行（如「解析：A」「第 N 题」「答案」）。

用法
----
    # 对单个帧目录做 OCR（结果写 <dir>/_ocr.jsonl，已抽过的帧自动跳过）
    python scripts/bili_ocr_frames.py data/bili-analyze/p2019-danxuan/frames

    # 只打印匹配行（不重新 OCR，读缓存）
    python scripts/bili_ocr_frames.py data/bili-analyze/p2019-danxuan/frames --grep "解析"

    # 一次处理 data/bili-analyze 下所有含 frames/ 的子目录
    python scripts/bili_ocr_frames.py --all

    # 强制重抽
    python scripts/bili_ocr_frames.py <dir> --redo

设计要点（都是踩过的坑）
------------------------
1. **必须增量续跑**：296 帧 × 1.4 s ≈ 7 分钟，中断一次就白干。逐帧写 jsonl，重启时跳过已有。
2. **OCR 结果要连 box 一起存**：同一屏常常多行，按 y 坐标排序才是正确的阅读顺序
   （rapidocr 的返回顺序不保证）。存 box 便于后续按区域切分。
3. **不要用 `-q` 静默 pip**：本项目曾因静默安装「成功但没装」浪费一轮。
4. `rapidocr_onnxruntime` 的 score 是 **float**，但返回项是 `[box, text, score]` 列表；
   用 `item[1]` / `item[2]` 取，不要直接解包成 `box, txt, score` 再格式化。
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_ANALYZE = ROOT / "data" / "bili-analyze"

CACHE_NAME = "_ocr.jsonl"
LOWCONF_NAME = "_ocr_lowconf.jsonl"


def build_ocr(det_max: int | None = None):
    """构造 RapidOCR。

    ★ `det_max` 非空 ⇒ 把检测端的 `limit_type` 从 min 改成 max（即**不放大**）。
      背景：默认 `limit_type=min, limit_side_len=736`，而我们的帧是 800×450 ——
      短边 450 < 736 ⇒ **被放大 1.64 倍**再进检测网络，等于白算 2.7 倍像素。
      实测 12 帧：默认 19.1s → max/800 16.9s（快约 12%）。

    ★ 为什么**默认不开**：同一批帧的「关键行」总数相同（66 → 66），
      但**逐帧不完全一致**（仅 7/12 帧相同）⇒ 存在阈值边界抖动，
      在未证实「关键行逐字等价」之前不默认启用。要快就显式传 `--det-max 800`。

    ★ 只传 `det_limit_*` 会抛 `KeyError: 'model_path'` —— rapidocr 1.2.3 的
      `update_det_params()` 无条件读 `det_dict['model_path']`；必须同时传
      `det_model_path=None` 才能走到「从 config 补默认路径」那一支。
    """
    from rapidocr_onnxruntime import RapidOCR
    if det_max:
        return RapidOCR(det_model_path=None, det_limit_type="max",
                        det_limit_side_len=det_max)
    return RapidOCR()


def load_cache(cache: pathlib.Path) -> dict[str, dict]:
    done: dict[str, dict] = {}
    if cache.exists():
        for line in cache.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "frame" in rec:
                done[rec["frame"]] = rec
    return done


def sort_by_reading_order(items: list) -> list:
    """按 y 中心、再按 x 排序 —— rapidocr 的返回顺序不保证是阅读顺序。"""
    def key(item):
        box = item[0]
        ys = [p[1] for p in box]
        xs = [p[0] for p in box]
        return (round(sum(ys) / len(ys) / 12), sum(xs) / len(xs))
    return sorted(items, key=key)


def ocr_dir(frame_dir: pathlib.Path, redo: bool = False, limit: int | None = None,
            min_conf: float = 0.85, det_max: int | None = None) -> dict:
    frames = sorted(frame_dir.glob("*.jpg"))
    if not frames and (frame_dir / "frames").is_dir():
        # ★ 容错：本库约定帧目录是 <BV>/frames/，但常有人把 <BV>/ 整个传进来。
        #   自动下钻一层，省一次白跑（下钻后 .parent 仍是 <BV>/，缓存路径不受影响）。
        print(f"[hint] {frame_dir} 下无 jpg，自动改用 {frame_dir.name}/frames/")
        frame_dir = frame_dir / "frames"
        frames = sorted(frame_dir.glob("*.jpg"))
    if not frames:
        print(f"[skip] {frame_dir} 无 jpg")
        return {"frames": 0, "new": 0}

    cache_path = frame_dir.parent / CACHE_NAME
    done = {} if redo else load_cache(cache_path)
    todo = [f for f in frames if f.name not in done]
    if limit:
        todo = todo[:limit]

    print(f"[ocr ] {frame_dir.parent.name}: 共 {len(frames)} 帧，已完成 {len(done)}，本次待处理 {len(todo)}")
    if not todo:
        return {"frames": len(frames), "new": 0}

    ocr = build_ocr(det_max)
    low = []                       # ★ D2：低置信行单独留档，不污染 _ocr.jsonl 的 schema
    t0 = time.time()
    with cache_path.open("a", encoding="utf-8", newline="\n") as fh:
        for i, fp in enumerate(todo, 1):
            try:
                res, _ = ocr(str(fp))
            except Exception as exc:                      # noqa: BLE001
                rec = {"frame": fp.name, "error": f"{type(exc).__name__}: {exc}", "lines": []}
            else:
                lines = []
                for item in (res or []):
                    box, txt, score = item[0], item[1], item[2]
                    lines.append({
                        "t": txt,
                        "s": round(float(score), 3),
                        "box": [[round(float(x), 1), round(float(y), 1)] for x, y in box],
                    })
                lines = sort_by_reading_order([[l["box"], l["t"], l["s"]] for l in lines])
                rec = {
                    "frame": fp.name,
                    "lines": [{"t": t, "s": s, "box": b} for b, t, s in lines],
                }
                for l in rec["lines"]:
                    if l["s"] < min_conf:
                        low.append({"frame": fp.name, "t": l["t"], "s": l["s"],
                                    "box": l["box"]})
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            if i % 20 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"       {i}/{len(todo)}  {el:.0f}s  预计剩余 {el / i * (len(todo) - i):.0f}s")

    if low:
        lp = frame_dir.parent / LOWCONF_NAME
        with lp.open("a", encoding="utf-8", newline="\n") as fh:
            for r in low:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return {"frames": len(frames), "new": len(todo), "low": len(low)}


def do_stats(dirs: list[pathlib.Path], min_conf: float) -> None:
    """汇总每个帧目录的「帧数 / 行数 / 中位置信度 / 低置信行数及占比 / 涉及帧数」。

    ★ 为什么这个汇总本身有价值：**中位置信度是「这版抽帧够不够」的量化指标** ——
      比「抽帧率与内容停留时长匹配吗」这种定性判断更硬。
      实测（2026-09-21，29513 行）：中位 0.803（政治 2025 张慧佳）～ 0.895（2019 多选）；
      全库 P10=0.615 / P50=0.862。中位数明显偏低的目录 = 分辨率不足或压缩过狠，
      再抽多少帧也读不准 ⇒ 该换源或加密抽帧。
    """
    import statistics
    tot_l = tot_low = 0
    rows = []
    for d in dirs:
        cache = d.parent / CACHE_NAME
        if not cache.exists():
            print(f"{d.parent.name:28s} 无 {CACHE_NAME}")
            continue
        nl = nf = nlow = 0
        low_frames = set()
        vals = []
        for line in cache.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            nf += 1
            for l in rec.get("lines", []):
                nl += 1
                s = float(l.get("s", 1.0))
                vals.append(s)
                if s < min_conf:
                    nlow += 1
                    low_frames.add(rec["frame"])
        tot_l += nl
        tot_low += nlow
        med = statistics.median(vals) if vals else 0.0
        rows.append((med, d.parent.name, nf, nl, nlow, len(low_frames)))
    for med, name, nf, nl, nlow, nlf in sorted(rows):
        pct = (nlow / nl * 100) if nl else 0.0
        print(f"{name:28s} 帧 {nf:4d}  行 {nl:5d}  中位 {med:.3f}  "
              f"低置信 {nlow:4d} ({pct:5.2f}%)  涉及帧 {nlf:4d}")
    pct = (tot_low / tot_l * 100) if tot_l else 0.0
    print(f"{'合计':28s} 行 {tot_l:5d}  低置信 {tot_low:4d} ({pct:5.2f}%)  阈值 {min_conf}")


def iter_targets(all_dirs: bool, explicit: list[str]) -> list[pathlib.Path]:
    if all_dirs:
        return sorted(p / "frames" for p in DEFAULT_ANALYZE.iterdir()
                      if (p / "frames").is_dir())
    out = []
    for raw in explicit:
        p = pathlib.Path(raw)
        if not p.is_absolute():
            p = (ROOT / p) if (ROOT / raw).exists() else p
        out.append(p)
    return out


def do_grep(dirs: list[pathlib.Path], pattern: str) -> None:
    import re
    rx = re.compile(pattern)
    for d in dirs:
        cache = d.parent / CACHE_NAME
        if not cache.exists():
            print(f"[grep] {d.parent.name}: 无 {CACHE_NAME}，先跑 OCR")
            continue
        print(f"\n=== {d.parent.name} ===")
        for line in cache.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            hits = [l["t"] for l in rec.get("lines", []) if rx.search(l["t"])]
            if hits:
                print(f"{rec['frame']}: " + " | ".join(hits))


def main() -> int:
    ap = argparse.ArgumentParser(description="B站 画面帧批量 OCR（增量缓存）")
    ap.add_argument("dirs", nargs="*", help="帧目录（含 *.jpg）")
    ap.add_argument("--all", action="store_true", help="处理 data/bili-analyze 下所有 frames/ 目录")
    ap.add_argument("--grep", help="只在缓存里打印匹配行（不 OCR）")
    ap.add_argument("--redo", action="store_true", help="忽略缓存重抽")
    ap.add_argument("--limit", type=int, help="本次最多处理多少帧（试跑用）")
    ap.add_argument("--min-conf", type=float, default=0.60,
                    help="低置信阈值（默认 0.60）。低于它的行另存 _ocr_lowconf.jsonl，"
                         "并在 --stats 里汇总占比。★ 默认值取自实测分布：全库 29513 行"
                         "置信度 P10=0.615 / P50=0.862 / P90=0.921 —— 取 0.60 正好"
                         "标出最差的约 10%%，而不是把一半正常行也标上")
    ap.add_argument("--det-max", type=int, default=None, metavar="N",
                    help="检测端不放大（limit_type=max, limit_side_len=N）。"
                         "实测快约 12%%，但关键行逐帧不完全一致，**默认关闭**")
    ap.add_argument("--stats", action="store_true",
                    help="只汇总缓存统计（帧数/行数/低置信行数/占比/涉及帧），不 OCR")
    args = ap.parse_args()

    targets = iter_targets(args.all, args.dirs)
    if not targets:
        ap.error("未指定帧目录（或用 --all）")

    if args.stats:
        do_stats(targets, args.min_conf)
        return 0

    if args.grep:
        do_grep(targets, args.grep)
        return 0

    total_new = total_low = 0
    for d in targets:
        st = ocr_dir(d, redo=args.redo, limit=args.limit,
                     min_conf=args.min_conf, det_max=args.det_max)
        total_new += st["new"]
        total_low += st.get("low", 0)
    print(f"\n完成：本次新抽 {total_new} 帧"
          + (f"，其中低置信行 {total_low} 条（已存 _ocr_lowconf.jsonl）" if total_low else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
