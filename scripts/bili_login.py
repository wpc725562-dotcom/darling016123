#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B站扫码登录 —— 拿到 SESSDATA 供 bili_analyze.py 免 ASR 取 AI 字幕。

为什么需要它：
    B站「AI 字幕」属于登录态资源。不带 SESSDATA 时 /x/player/v2 会返回
    need_login_subtitle=true 但 subtitles 为空 —— 只能退回语音转写（ASR），
    慢且消耗 Gemini 额度。带上 SESSDATA 可直接下载现成字幕。

为什么不用手抄 cookie：
    从 DevTools 里翻 SESSDATA 容易抄错、抄漏，也容易顺手贴进聊天记录。
    扫码是官方支持的正规入口，30 秒搞定。

用法：
    python scripts/bili_login.py                 # 终端显示二维码，扫码
    python scripts/bili_login.py --html qr.html  # 另外落一份 HTML（终端乱码时用）
    python scripts/bili_login.py --verify        # 只校验已存的 SESSDATA 是否还有效

SESSDATA 存放位置（按优先级）：
    --sessdata-out 指定 > 仓库根 .bili-sessdata > 用户目录 ~/.bili-sessdata
    ⚠️ 已在 .gitignore 里挡掉，但请勿手动提交或外发 —— 这是账号最高权限凭证。

依赖：qrcode（仅用于渲染二维码）。没装也能用，会退化为打印链接。
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
REFERER = "https://www.bilibili.com/"

GENERATE = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
POLL = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={}"
NAV = "https://api.bilibili.com/x/web-interface/nav"

# poll 返回的内层状态码
POLL_OK = 0          # 登录成功
POLL_UNSCANNED = 86101
POLL_UNCONFIRMED = 86090
POLL_EXPIRED = 86038


# ------------------------------------------------------------------ 基础

def _get(url, cookie=None, timeout=20):
    """GET 并返回 (json, headers)。"""
    h = {"User-Agent": UA, "Referer": REFERER}
    if cookie:
        h["Cookie"] = cookie
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8")), r.headers


def parse_sessdata(cookie_headers, redirect_url=""):
    """从 Set-Cookie 头或回调 URL 里挖出 SESSDATA。"""
    for raw in cookie_headers or []:
        for part in raw.split(";"):
            part = part.strip()
            if part.startswith("SESSDATA="):
                v = part[len("SESSDATA="):].strip()
                if v:
                    return v
    # 兜底：成功时 data.url 会把各 cookie 挂在 query 上
    if "SESSDATA=" in redirect_url:
        tail = redirect_url.split("SESSDATA=", 1)[1]
        v = tail.split("&", 1)[0]
        if v:
            return urllib.parse.unquote(v)
    return None


def save_sessdata(value, path):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8", newline="\n")
    # Windows 上 chmod 基本无效，但仍设一下，Linux/macOS 有效
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def verify(value):
    """调 nav 接口确认登录态。返回 (是否有效, 说明)。"""
    try:
        d, _ = _get(NAV, cookie=f"SESSDATA={value}")
    except Exception as e:
        return False, f"请求失败：{e}"
    if d.get("code") != 0:
        return False, f"接口返回 code={d.get('code')} {d.get('message')}"
    data = d.get("data") or {}
    if not data.get("isLogin"):
        return False, "未登录（SESSDATA 已失效或过期）"
    return True, f"已登录：{data.get('uname')}（uid {data.get('mid')}）"


# ------------------------------------------------------------------ 渲染

def render_terminal(url):
    """在终端画出二维码。返回 True 表示已渲染。"""
    try:
        import qrcode  # noqa: PLC0415
    except ImportError:
        return False
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    # 用半高块：一个字符行塞两行像素，扫描更紧凑
    out = []
    for y in range(0, n, 2):
        row = []
        for x in range(n):
            top = m[y][x]
            bot = m[y + 1][x] if y + 1 < n else False
            row.append("█" if (top and bot) else "▀" if top else "▄" if bot else " ")
        out.append("".join(row))
    text = "\n".join(out)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    try:
        print(text)
        return True
    except UnicodeEncodeError:
        return False


def write_html(url, path):
    """把二维码落成 HTML —— 终端编码不配合时的可靠退路。"""
    try:
        import qrcode  # noqa: PLC0415
        import qrcode.image.svg  # noqa: PLC0415
    except ImportError:
        return None
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage)
    import io  # noqa: PLC0415
    buf = io.BytesIO()
    img.save(buf)
    svg = buf.getvalue().decode("utf-8")
    svg = svg.replace("<svg ", '<svg style="width:min(80vw,520px);height:auto" ', 1)
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>B站扫码登录</title>
<style>
 body{{margin:0;min-height:100vh;display:flex;flex-direction:column;
      align-items:center;justify-content:center;gap:18px;
      background:#0f1115;color:#e8e8e8;
      font:16px/1.6 system-ui,"Microsoft YaHei",sans-serif}}
 .card{{background:#fff;padding:20px;border-radius:14px;line-height:0}}
 h1{{font-size:20px;margin:0;font-weight:600}}
 p{{margin:0;color:#9aa0a6;font-size:14px;text-align:center}}
</style></head><body>
<h1>用「哔哩哔哩」App 扫码</h1>
<div class="card">{svg}</div>
<p>扫码后在手机上点确认 · 本页可直接关闭</p>
</body></html>"""
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8", newline="\n")
    return p


# ------------------------------------------------------------------ 主流程

def do_login(a):
    print("请求二维码…")
    d, _ = _get(GENERATE)
    if d.get("code") != 0:
        print(f"✗ 获取二维码失败：code={d.get('code')} {d.get('message')}")
        return 2
    data = d["data"]
    key, url = data["qrcode_key"], data["url"]
    print(f"  有效期约 180 秒\n")

    rendered = render_terminal(url)
    if not rendered:
        print("⚠️  未装 qrcode 库或终端不支持方块字符，改用链接方式：")
        print("    1) 复制下面链接，粘贴到任意二维码生成网页/App：")
        print(f"       {url}")
        print("    2) 或用手机浏览器打开后从「扫一扫」进入")
        print("    装库后可自动出图：pip install qrcode\n")
    else:
        print()

    html_path = a.html
    if html_path is None:
        # 终端渲染失败时自动补一份 HTML
        html_path = None if rendered else "bili-qr.html"
    if html_path:
        p = write_html(url, html_path)
        if p:
            print(f"已写出网页版二维码：{p.resolve()}")
            print("（浏览器打开后扫码；终端乱码时用这个）\n")

    print("等待扫码…（Ctrl+C 取消）")
    deadline = time.time() + 180
    last = None
    while time.time() < deadline:
        try:
            pd, headers = _get(POLL.format(key))
        except urllib.error.URLError as e:
            print(f"  轮询异常（重试）：{e}")
            time.sleep(2)
            continue
        st = (pd.get("data") or {}).get("code")
        if st != last:
            label = {
                POLL_UNSCANNED: "  等待扫码…",
                POLL_UNCONFIRMED: "  已扫码，请在手机上点「确认登录」…",
                POLL_EXPIRED: "  ✗ 二维码已失效",
            }.get(st)
            if label:
                print(label)
            last = st
        if st == POLL_OK:
            redirect = (pd.get("data") or {}).get("url", "")
            sess = parse_sessdata(headers.get_all("Set-Cookie"), redirect)
            if not sess:
                print("✗ 登录成功但没解析出 SESSDATA —— 响应结构可能变了，请反馈")
                return 3
            ok, msg = verify(sess)
            print(f"\n{'✓' if ok else '⚠'} 登录态校验：{msg}")
            out = a.sessdata_out or default_path()
            p = save_sessdata(sess, out)
            print(f"✓ 已保存 SESSDATA → {p.resolve()}")
            print(f"  预览：{sess[:6]}…{sess[-4:]}（共 {len(sess)} 字符）")
            print(f"\n现在可以免 ASR 取字幕了：")
            print(f"  python scripts/bili_analyze.py BV1xx411c7mD --pages 1-3")
            return 0 if ok else 0
        if st == POLL_EXPIRED:
            print("请重新运行本脚本获取新二维码。")
            return 4
        time.sleep(2)

    print("✗ 超时（180 秒）未完成扫码。")
    return 5


def default_path():
    """默认落盘位置：仓库根（cwd）优先，否则用户目录。"""
    here = pathlib.Path(".bili-sessdata")
    try:
        here.parent.resolve()
        return here
    except OSError:
        return pathlib.Path.home() / ".bili-sessdata"


def do_verify(a):
    cand = []
    if a.sessdata_out:
        cand.append(pathlib.Path(a.sessdata_out))
    cand += [pathlib.Path(".bili-sessdata"), pathlib.Path.home() / ".bili-sessdata"]
    if os.environ.get("BILI_SESSDATA"):
        cand.insert(0, None)
    for c in cand:
        if c is None:
            v = os.environ["BILI_SESSDATA"]
            src = "环境变量 BILI_SESSDATA"
        else:
            if not c.exists():
                continue
            v = c.read_text(encoding="utf-8", errors="ignore").strip()
            src = str(c.resolve())
            if not v:
                continue
        ok, msg = verify(v)
        print(f"{'✓' if ok else '✗'} {src}\n    {msg}")
        return 0 if ok else 1
    print("✗ 没找到任何 SESSDATA。先运行：python scripts/bili_login.py")
    return 1


def main():
    ap = argparse.ArgumentParser(
        description="B站扫码登录，拿 SESSDATA（供 bili_analyze.py 免 ASR 取 AI 字幕）")
    ap.add_argument("--html", default=None,
                    help="额外把二维码写成 HTML 文件（终端乱码时用）")
    ap.add_argument("--sessdata-out", default=None,
                    help="SESSDATA 保存路径（默认 ./.bili-sessdata）")
    ap.add_argument("--verify", action="store_true",
                    help="只校验已保存的 SESSDATA 是否仍有效")
    a = ap.parse_args()
    return do_verify(a) if a.verify else do_login(a)


if __name__ == "__main__":
    sys.exit(main())
