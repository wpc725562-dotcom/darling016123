# -*- coding: utf-8 -*-
"""
真题 Markdown → 可打印 HTML（浏览器打印成 PDF）
用法：
  python scripts/md-to-printable.py <输入.md> [输出.html]
  python scripts/md-to-printable.py --all   # 转换 docs/posts/math 下所有真题
"""
import re, sys, html, pathlib

def md_to_html(md_text, title=""):
    """把常见 markdown 语法转成打印友好的 HTML（够用即可）"""
    # 跳过 frontmatter (--- ... ---)
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            md_text = parts[2]
    lines = md_text.split("\n")
    out = []
    in_ol = False
    for line in lines:
        s = line.rstrip()
        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)", s)
        if m:
            if in_ol: out.append("</ol>"); in_ol = False
            lv = len(m.group(1))
            txt = html.escape(m.group(2))
            out.append(f"<h{lv}>{txt}</h{lv}>")
            continue
        # 有序列表（题目选项 A. B. C. 用列表）
        m = re.match(r"^(\d+)\.\s+(.*)", s)
        if m:
            if not in_ol: out.append("<ol>"); in_ol = True
            out.append(f"<li>{html.escape(m.group(2))}</li>")
            continue
        # 无序列表
        m = re.match(r"^[-*]\s+(.*)", s)
        if m:
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(f"<li>{html.escape(m.group(1))}</li>")
            continue
        # 引用块
        m = re.match(r"^>\s?(.*)", s)
        if m:
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(f"<blockquote>{html.escape(m.group(1))}</blockquote>")
            continue
        # 表格分隔行跳过
        if re.match(r"^\|?[\s:|-]+\|?$", s) and s.count("|") > 1:
            continue
        # 表格行
        if s.startswith("|") and s.count("|") > 1:
            if in_ol: out.append("</ol>"); in_ol = False
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not out or not out[-1].startswith("<table>"):
                out.append("<table border='1' cellpadding='6' style='border-collapse:collapse;width:100%'>")
                out.append("<tr>" + "".join(f"<th>{html.escape(c)}</th>" for c in cells) + "</tr>")
            else:
                out.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in cells) + "</tr>")
            continue
        # 空行
        if not s.strip():
            if in_ol: out.append("</ol>"); in_ol = False
            out.append("<div class='gap'></div>")
            continue
        # 普通段落：处理粗体/行内代码
        if in_ol: out.append("</ol>"); in_ol = False
        txt = html.escape(s)
        txt = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", txt)
        txt = re.sub(r"`(.+?)`", r"<code>\1</code>", txt)
        out.append(f"<p>{txt}</p>")
    if in_ol: out.append("</ol>")
    return "\n".join(out)

def wrap_html(body, title):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
body {{ font-family: "Microsoft YaHei", "Noto Sans SC", sans-serif; max-width: 800px; margin: 40px auto; padding: 0 24px; font-size: 14px; line-height: 1.8; color: #222; }}
h1 {{ font-size: 22px; border-bottom: 2px solid #333; padding-bottom: 8px; }}
h2 {{ font-size: 18px; margin-top: 24px; }}
h3 {{ font-size: 16px; }}
table {{ margin: 12px 0; }}
blockquote {{ border-left: 3px solid #999; margin: 8px 0; padding: 4px 12px; color: #555; background: #f7f7f7; }}
code {{ background: #f0f0f0; padding: 1px 5px; border-radius: 3px; }}
.gap {{ height: 8px; }}
@media print {{ body {{ margin: 0; padding: 0; max-width: none; }} }}
</style>
</head>
<body>
{body}
</body>
</html>"""

def convert(src, dst=None):
    p = pathlib.Path(src)
    text = p.read_text(encoding="utf-8")
    # 标题：优先 frontmatter title，其次第一个 # 行
    title = ""
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    if fm:
        tm = re.search(r"^title:\s*(.+)$", fm.group(1), re.M)
        if tm:
            title = tm.group(1).strip().strip('"\'')
    if not title:
        m = re.search(r"^#\s+(.+)$", text, re.M)
        title = m.group(1).strip() if m else p.stem
    body = md_to_html(text)
    html_doc = wrap_html(body, title)
    if dst is None:
        dst = p.with_suffix(".html")
    pathlib.Path(dst).write_text(html_doc, encoding="utf-8", newline="\n")
    return dst, title

if __name__ == "__main__":
    if "--all" in sys.argv:
        repo = pathlib.Path(__file__).resolve().parent.parent
        out_dir = repo / "docs" / "public" / "printable"
        out_dir.mkdir(exist_ok=True)
        for sub in ["math", "computer", "english", "politics"]:
            d = repo / "docs" / "posts" / sub
            if not d.exists(): continue
            for f in sorted(d.glob("*.md")):
                if f.name == "index.md": continue
                dst = out_dir / f"{sub}-{f.stem}.html"
                convert(f, dst)
                print(f"  {dst.name}")
        print("DONE: 已转换 docs/posts 下所有真题为可打印 HTML → docs/public/printable/")
        print("提示：在浏览器打开后用 Ctrl+P 打印为 PDF，或见 README 中 Chrome headless 命令")
    else:
        src = sys.argv[1]
        dst = sys.argv[2] if len(sys.argv) > 2 else None
        dst, title = convert(src, dst)
        print(f"已转换: {src} -> {dst}（{title}）")
