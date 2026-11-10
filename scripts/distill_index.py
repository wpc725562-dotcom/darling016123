"""扫盘生成总索引：把每个 txt 的头部【】字段抽成一张表。

输出 资料/电子书蒸馏/00-总索引.txt，可直接用于导入题库或做目录页。

除四层 txt 外，还会登记两类 .md 制品：
  · 蒸馏根目录的 00-*.md（跨科映射表等，如 00-政治真题考点映射表-*.md）
  · 各科根目录的 00-*.md（如 03-计算机/00-真题考点映射表-*.md）
这两类不计入「四层」合计，单独列在末尾「附加制品」区。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "资料" / "电子书蒸馏"
LAYERS = [
    ("章节", "章节精要"),
    ("模块", "模块导览"),
    ("考点笔记", "考点笔记"),
    ("配套题", "配套题"),
    ("答案解析", "答案解析"),
]
# 各科根目录下的单文件（不属四层）
SINGLE = ["错题本.txt", "公式速查.txt", "词汇表.txt", "范文库.txt"]


def parse_header(path):
    """只读前 30 行，抽【key】value 形式的字段。"""
    fields = {}
    with path.open(encoding="utf-8", errors="replace") as fh:
        for _ in range(30):
            line = fh.readline()
            if not line:
                break
            m = re.match(r"^【(.+?)】(.*)$", line.strip())
            if m:
                fields[m.group(1)] = m.group(2).strip()
    return fields


def artifacts(d):
    """目录下的 00-*.md 制品（映射表等），排除指令文件。"""
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("00-*.md") if not p.name.startswith("_"))


def main():
    lines = [
        "电子书蒸馏 · 总索引",
        "=" * 60,
        "",
        "字段说明：文件名 | 考点 | 考频 | 题型 | 字数",
        "",
    ]
    total_files = 0
    total_chars = 0
    extra = []  # (标签, Path)

    for p in artifacts(ROOT):
        extra.append(("蒸馏根目录", p))

    for course in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name[:2].isdigit()):
        lines.append(f"\n{'=' * 60}")
        lines.append(f"【课程】{course.name}")
        lines.append(f"{'=' * 60}")
        for layer, label in LAYERS:
            d = course / layer
            if not d.is_dir():
                continue
            # 四层主体是 .txt；真题精练册等制品用 .md，也要纳入，否则建了等于没建
            files = sorted(list(d.glob("*.txt")) + list(d.glob("*.md")))
            if not files:
                continue
            lines.append(f"\n-- {label}（{len(files)} 个）--")
            for f in files:
                text = f.read_text(encoding="utf-8", errors="replace")
                n = len(text.strip())
                total_files += 1
                total_chars += n
                h = parse_header(f)
                parts = [f.name]
                for k in ("考点", "考频", "题型"):
                    if h.get(k):
                        parts.append(h[k])
                parts.append(f"{n} 字")
                lines.append(" | ".join(parts))

        # 科目根目录的单文件
        singles = [course / n for n in SINGLE if (course / n).exists()]
        if singles:
            lines.append(f"\n-- 单文件（{len(singles)} 个）--")
        for f in singles:
            n = len(f.read_text(encoding="utf-8", errors="replace").strip())
            total_files += 1
            total_chars += n
            lines.append(f"{f.name} | {n} 字")

        for p in artifacts(course):
            extra.append((course.name, p))

    lines.append(f"\n{'=' * 60}")
    lines.append(f"合计：{total_files} 个文件，{total_chars} 字")
    lines.append(f"{'=' * 60}")

    if extra:
        lines.append(f"\n{'=' * 60}")
        lines.append("【附加制品】跨科/跨层映射表（.md，不计入上方合计）")
        lines.append(f"{'=' * 60}")
        for label, p in extra:
            n = len(p.read_text(encoding="utf-8", errors="replace").strip())
            lines.append(f"{label}/{p.name} | {n} 字")

    out = ROOT / "00-总索引.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"写入 {out}")
    print(f"文件 {total_files} 个，合计 {total_chars} 字；附加制品 {len(extra)} 个")


if __name__ == "__main__":
    main()

