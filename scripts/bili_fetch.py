#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站(Bilibili)元数据+音频抓取脚本 -- 免登录走官方API
用法: python bili_fetch.py BV号 [输出路径]

2026-09-18 修复: x/web-interface/view 已被风控，稳定返回 HTTP 412
  （4/4 个 BV 全部 412，无 cookie / 带 buvid3 cookie / 加完整浏览器头 均无效）
  改用 x/web-interface/wbi/view —— 同样 4/4 返回 200，且无需 wbi 签名。
  兜底: x/player/pagelist（拿 cid/分P/时长，同样免登录免签名）。
"""
import argparse, importlib.util, json, os, pathlib, subprocess, urllib.request

# ★ A5 残留（2026-09-20）：ffprobe 原先没有 timeout —— 外部命令挂住脚本就不返回。
SUBPROC_TIMEOUT = int(os.environ.get("ZHENTI_SUBPROC_TIMEOUT", "600"))

HERE = pathlib.Path(__file__).resolve().parent


def _find_ffprobe():
    """定位 ffprobe。

    ★ 2026-09-21 修：本脚本原先**裸调 `ffprobe`**，假定它在 PATH 上 —— 而实测
      PATH 上根本没有（`shutil.which` 返回 None）。ffprobe 实际装在
      `D:/ACLOS/Cross/recorder-release/`，只有 `bili_analyze.find_tool()` 那个
      兜底查找逻辑能找到它。

      后果很隐蔽：`dur()` 里 `subprocess.run` 抛 FileNotFoundError，
      而 main() 里没有 try —— **时长校验整段失效**，脚本在下完音频后崩掉。
      （`bili_analyze.py` / `bili_zhenti.py` 都用 find_tool 兜底，只有这个文件漏了。）

      修法：复用 bili_analyze 的 find_tool，不复制那份目录清单 ——
      否则下次换机器、换 ffmpeg 位置，两边会各自漂移。
    """
    from shutil import which
    p = which("ffprobe")
    if p:
        return p
    ba = _load_analyze()
    if ba is not None:
        return ba.find_tool("ffprobe")
    for c in (r"D:/ACLOS/Cross/recorder-release", r"C:/ffmpeg/bin",
              r"C:/Program Files/ffmpeg/bin", os.path.expanduser("~/scoop/shims")):
        exe = pathlib.Path(c) / ("ffprobe.exe" if os.name == "nt" else "ffprobe")
        if exe.exists():
            return str(exe)
    return None


def _load_analyze():
    """按路径载入同目录的 bili_analyze.py（同 bili_zhenti.py 的做法）。"""
    p = HERE / "bili_analyze.py"
    if not p.exists():
        return None
    spec = importlib.util.spec_from_file_location("bili_analyze", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FFPROBE = _find_ffprobe()

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
RE = "https://www.bilibili.com/"

def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": RE})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def get_meta(bvid):
    # 主: wbi/view（2026-09 实测免签名可用）
    try:
        d = api(f"https://api.bilibili.com/x/web-interface/wbi/view?bvid={bvid}")["data"]
        pages = [{"cid": p["cid"], "part": p["part"], "duration": p["duration"]} for p in d.get("pages", [])]
        return {"title": d["title"], "owner": d["owner"]["name"], "duration": d.get("duration", 0),
                "pages": pages, "pic": d.get("pic", ""), "src": "wbi/view"}
    except Exception as e:
        print(f"[warn] wbi/view 失败({e})，回退 pagelist")
    # 兜底: pagelist（无标题/UP主，但有 cid + 分P + 时长）
    ps = api(f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}")["data"]
    pages = [{"cid": p["cid"], "part": p["part"], "duration": p["duration"]} for p in ps]
    return {"title": pages[0]["part"] if pages else bvid, "owner": "(pagelist无此字段)",
            "duration": sum(p["duration"] for p in pages), "pages": pages, "pic": "", "src": "pagelist"}

def pick_audio(cid, bvid):
    d = api(f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&fnval=16&fourk=1")["data"]
    audios = sorted(d.get("dash", {}).get("audio", []), key=lambda a: a.get("bandwidth") or 0)
    if not audios: raise RuntimeError("无 Dash 音频流")
    return audios[0]["baseUrl"]

def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": RE})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        n = 0
        while True:
            c = r.read(1 << 20)
            if not c: break
            f.write(c); n += len(c)
    return n

def dur(path):
    """读音频时长。ffprobe 找不到时返回 None，而不是抛异常崩掉整条流水线。"""
    if not FFPROBE:
        return None
    o = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True,
                       timeout=SUBPROC_TIMEOUT).stdout.strip()
    return float(o) if o else None

def subtitle_tracks(cid, bvid):
    """探测字幕轨（`x/player/wbi/v2`；AI 字幕需登录，CC 字幕免登录）。

    ★ 为什么是 wbi 版而不是 `x/player/v2`：
      后者会**随机返回别的视频的字幕轨** —— 实测同一 cid 连打 15 次只 5 次命中，
      其余是火锅探店 / 装机 / 明星八卦，而 `code` 恒 0、`lan` 恒 `ai-zh`，
      **从响应完全看不出异常**。更坏的是对**真无轨**的视频它会凭空编一条
      别家视频的轨出来，把「无字幕」误判成「有字幕但串轨」。
      换 `x/player/wbi/v2` 后同一 cid **20/20 命中**，真无轨的稳定返回空数组。
      口径与 `bili_analyze.probe_subtitle` 保持一致（那边 2026-09-19 已换）。

    ★ 异常**不再吞成「无字幕」**：探测失败就抛，由调用方区分
      「确实没有」与「没查成」。`except: return [], False` 会把限流/超时
      伪装成永久的「此分P 无字幕」—— 那是本项目最贵的一类 bug。
    """
    d = api(f"https://api.bilibili.com/x/player/wbi/v2?bvid={bvid}&cid={cid}")
    if d.get("code") != 0:
        raise RuntimeError("player/wbi/v2 code=%s msg=%s"
                           % (d.get("code"), d.get("message")))
    data = d.get("data") or {}
    st = data.get("subtitle") or {}
    return st.get("subtitles") or [], bool(data.get("need_login_subtitle"))

def main(bvid, out):
    m = get_meta(bvid)
    print(f"标题: {m['title']}  |  UP: {m['owner']}  |  分P: {len(m['pages'])}  总时长: {m['duration']}s  [来源 {m['src']}]")
    if not m["pages"]: print("无分P, 中止"); return
    cid = m["pages"][0]["cid"]
    try:
        subs, need_login = subtitle_tracks(cid, bvid)
    except Exception as e:
        subs, need_login = None, None
        print(f"字幕: 探测失败（{e}）—— 这只说明**没查成**，不等于「无字幕」")
    if subs:
        print(f"字幕: {len(subs)} 轨 -> " + ", ".join(f"{s.get('lan_doc') or s.get('lan')}" for s in subs))
    elif subs == []:
        print(f"字幕: 无（AI 字幕需登录={need_login}；CC 字幕需 UP 主上传）")
    url = pick_audio(cid, bvid)
    print(f"音频流: {url[:70]}...")
    size = download(url, out)
    print(f"已下载: {out}  {size/1e6:.1f} MB")
    act, exp = dur(out), m["pages"][0]["duration"]
    print(f"时长校验: 实际 {act}s 元数据 {exp}s 差 {abs(act-exp):.1f}s " + ("OK" if act and abs(act-exp) <= 5 else "!!偏差过大"))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("bvid"); p.add_argument("out", nargs="?", default="audio.m4s")
    main(p.parse_args().bvid, p.parse_args().out)
