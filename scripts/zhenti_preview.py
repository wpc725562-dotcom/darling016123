#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""真题页转换 · 预览（dry-run 全管线）

把「前置搬运 → 转换器」整条管线跑在**源文件的副本**上，产物写到临时目录，一个字节都不动线上文件。
用于 --apply 之前先肉眼看一遍产物。

用法：
    python scripts/zhenti_preview.py english2019
    python scripts/zhenti_preview.py english2019 english2020jingxi

★ E1（2026-09-20）：临时目录原来硬编码 `D:/tmp`（写死盘符）。现在默认用系统临时目录，
  需要固定位置时设 `ZHENTI_TMP=/path/to/dir`。
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

# 本脚本依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path（理由见 zhenti_lint.py）。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr），正式输出仍走 print（stdout）。
from zhenti_log import add_logging_args, get_logger, setup_from_args  # noqa: E402

LOG = get_logger(__name__)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = ROOT / "scripts" / "zhenti_cfg"
TMP = pathlib.Path(os.environ.get("ZHENTI_TMP") or tempfile.gettempdir())

# ★ A5 残留（2026-09-20）：原先两个 subprocess 都没有 timeout ——
#   子脚本挂住（例如 stdin 等待、大页面卡在正则上）预览就永远不返回。
SUBPROC_TIMEOUT = int(os.environ.get("ZHENTI_SUBPROC_TIMEOUT", "120"))


def _run(cmd, label):
    """跑一个子脚本并**检查退出码**。

    ★ 原先 promote 那一步只看 stdout、完全不看 returncode：
      子脚本报错退出（rc≠0）时，它打的是空 stdout，于是这里
      `print(r.stdout.strip() or r.stderr[-800:])` 把 stderr 当输出打出来，
      看起来像「跑了、有输出」，实际是**失败**。预览脚本因此可能给你
      一个基于半成品的产物，还什么都不提示。
    """
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=SUBPROC_TIMEOUT)
    if r.returncode:
        LOG.warning("%s 退出码 %d", label, r.returncode)
        print(f"  [!] {label} 退出码 {r.returncode}")
        if r.stderr.strip():
            print(r.stderr.strip()[-1500:])
    return r


def run(name):
    cfg = json.loads((CFG / f"{name}.json").read_text(encoding="utf-8"))
    src = ROOT / cfg["file"]
    if not src.exists():
        LOG.error("%s：源文件不存在 %s", name, cfg["file"])
        print(f"  {name}: 源文件不存在 {cfg['file']}")
        return
    tmp = TMP / f"prev_{name}.md"
    shutil.copy2(src, tmp)
    LOG.debug("%s：源 → 临时副本 %s", name, tmp)

    spec = CFG / f"promote_{name}.json"
    if not spec.exists():
        spec = CFG / f"promote{cfg.get('year')}.json"
    if spec.exists():
        sp = json.loads(spec.read_text(encoding="utf-8"))
        if sp.get("file") == cfg["file"]:
            sp["file"] = str(tmp).replace("\\", "/")
            p2 = TMP / f"prev_{name}_promote.json"
            p2.write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8",
                          newline="\n")
            script = sp.get("script", "zhenti_promote_compact.py")
            LOG.info("%s：前置搬运 %s", name, script)
            r = _run(
                [sys.executable, str(ROOT / "scripts" / script),
                 "--spec", str(p2), "--out", str(tmp)],
                f"{name} 前置搬运 {script}")
            print(r.stdout.strip() or r.stderr[-800:])
        else:
            LOG.debug("%s：promote spec 的 file 与配置不一致，跳过前置搬运", name)
    else:
        LOG.debug("%s：没有对应的 promote spec，跳过前置搬运", name)

    c2 = dict(cfg)
    c2["file"] = str(tmp).replace("\\", "/")
    p3 = TMP / f"prev_{name}_cfg.json"
    p3.write_text(json.dumps(c2, ensure_ascii=False, indent=2), encoding="utf-8",
                  newline="\n")
    out = TMP / f"out_{name}.md"
    LOG.info("%s：转换 → %s", name, out)
    r = _run(
        [sys.executable, str(ROOT / "scripts" / "zhenti_convert.py"),
         "--config", str(p3), "--out", str(out)],
        f"{name} 转换")
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr[-1500:])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="真题页转换 · 预览（dry-run 全管线）")
    ap.add_argument("names", nargs="*", help="zhenti_cfg 里的配置名，如 english2019")
    add_logging_args(ap)
    _a = ap.parse_args()
    setup_from_args(_a)
    if not _a.names:
        ap.error("至少给一个配置名（zhenti_cfg/<name>.json）")
    for nm in _a.names:
        run(nm)
