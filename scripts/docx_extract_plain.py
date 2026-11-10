"""把 docx 抽成纯文本，保留段落/标题层级线索。零第三方依赖。"""
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def para_text(p):
    parts = []
    for node in p.iter():
        tag = node.tag
        if tag == W + "t":
            parts.append(node.text or "")
        elif tag == W + "tab":
            parts.append("\t")
        elif tag == W + "br":
            parts.append("\n")
    return "".join(parts)


def para_style(p):
    ppr = p.find(W + "pPr")
    if ppr is None:
        return ""
    st = ppr.find(W + "pStyle")
    if st is None:
        return ""
    return st.get(W + "val") or ""


def outline_level(p):
    ppr = p.find(W + "pPr")
    if ppr is None:
        return None
    lvl = ppr.find(W + "outlineLvl")
    if lvl is None:
        return None
    try:
        return int(lvl.get(W + "val"))
    except (TypeError, ValueError):
        return None


def extract(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    body = root.find(W + "body")
    lines = []
    for el in body:
        if el.tag == W + "p":
            txt = para_text(el).strip()
            if not txt:
                continue
            style = para_style(el)
            lvl = outline_level(el)
            m = re.match(r"^(?:Heading|heading|标题)\s*(\d)", style)
            if m:
                lvl = int(m.group(1)) - 1
            elif style in ("Title",):
                lvl = 0
            if lvl is not None and lvl < 6:
                lines.append("#" * (lvl + 1) + " " + txt)
            else:
                lines.append(txt)
        elif el.tag == W + "tbl":
            for row in el.iter(W + "tr"):
                cells = []
                for cell in row.findall(W + "tc"):
                    ct = " ".join(para_text(p).strip() for p in cell.findall(W + "p"))
                    cells.append(re.sub(r"\s+", " ", ct).strip())
                if any(cells):
                    lines.append(" | ".join(cells))
    return "\n".join(lines)


if __name__ == "__main__":
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    text = extract(src)
    out.write_text(text, encoding="utf-8")
    print(f"{src.name} -> {out}  chars={len(text)} lines={text.count(chr(10))+1}")
