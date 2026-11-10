"""蒸馏产物体检：扫盘重算文件数、空文件、格式头、题号对齐、字数。
不做任何写入，只报告。退出码 1 表示有问题。

支持五科，各科字数下限与必备字段按科配置。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "资料" / "电子书蒸馏"

LAYERS = ["章节", "考点笔记", "配套题", "答案解析"]
# 英语的导览层叫「模块」，其余三科叫「章节」
LAYERS_EN = ["模块", "考点笔记", "配套题", "答案解析"]

# 各科目录名 -> 配置
COURSES = {
    "01-毛中特": {"章节": 500, "考点笔记": 900, "配套题": 1200, "答案解析": 1200},
    "02-习概":   {"章节": 500, "考点笔记": 900, "配套题": 1200, "答案解析": 1200},
    "03-计算机": {"章节": 600, "考点笔记": 600, "配套题": 1200, "答案解析": 1200},
    "04-高数":   {"章节": 600, "考点笔记": 400, "配套题": 1000, "答案解析": 1200},
    "05-英语":   {"模块": 600, "考点笔记": 500, "配套题": 1000, "答案解析": 1000},
}

HEADER_RULES = {
    "章节": ["【课程】", "【章节】", "【考点】"],
    "模块": ["【课程】", "【章节】", "【考点】"],
    "考点笔记": ["【课程】", "【章节】", "【节】", "【考点】", "【考频】", "【题型】"],
    "配套题": ["【课程】", "【章节】", "【题组】"],
    "答案解析": ["【课程】", "【章节】", "【解析】"],
}

# 全科单文件（放在科目根目录，不在四层里）
SINGLE_FILES = {
    "01-毛中特": [("错题本.txt", 200)],
    "02-习概": [("错题本.txt", 200)],
    "03-计算机": [("错题本.txt", 200)],
    "04-高数": [("错题本.txt", 200), ("公式速查.txt", 3000)],
    "05-英语": [("错题本.txt", 200), ("词汇表.txt", 4000), ("范文库.txt", 3000)],
}


def read(p):
    return p.read_text(encoding="utf-8", errors="replace")


def check_layer(course, layer, min_chars):
    d = ROOT / course / layer
    if not d.is_dir():
        return [f"缺目录 {course}/{layer}"], 0
    issues = []
    files = sorted(d.glob("*.txt"))
    for f in files:
        text = read(f)
        size = len(text.strip())
        if size == 0:
            issues.append(f"空文件 {course}/{layer}/{f.name}")
            continue
        if size < min_chars:
            issues.append(f"字数偏少 {course}/{layer}/{f.name} ({size} < {min_chars})")
        head = text[:400]
        for tag in HEADER_RULES[layer]:
            if tag not in head:
                issues.append(f"缺字段 {tag} {course}/{layer}/{f.name}")
    return issues, len(files)


def check_single_files(course):
    issues = []
    for name, minimum in SINGLE_FILES.get(course, []):
        p = ROOT / course / name
        if not p.exists():
            issues.append(f"缺文件 {course}/{name}")
            continue
        size = len(read(p).strip())
        if size < minimum:
            issues.append(f"字数偏少 {course}/{name} ({size} < {minimum})")
    return issues


def check_question_alignment(course):
    """题号必须从 1 连续；解析里的答案数必须等于题目数。"""
    issues = []
    qdir = ROOT / course / "配套题"
    adir = ROOT / course / "答案解析"
    if not qdir.is_dir() or not adir.is_dir():
        return issues
    for q in sorted(qdir.glob("*.txt")):
        if q.stem.endswith("-配套题"):
            base = q.stem[: -len("-配套题")]
        else:
            base = q.stem.split("-")[0]
        a = adir / f"{base}-答案解析.txt"
        if not a.exists():
            issues.append(f"缺解析 {course}/{a.name}")
            continue
        qtext, atext = read(q), read(a)
        qnums = [int(m.group(1)) for m in re.finditer(r"^\s*(\d{1,2})\.\s", qtext, re.M)]
        # 客观题写「N.【答案】」，主观题写「N.【答案要点】」「N.（1）【答案要点】」，
        # 编程/证明题写「N.【参考代码】」「N.【证明】」「N.【解】」
        anums = [
            int(m.group(1))
            for m in re.finditer(
                r"^\s*(\d{1,2})\.\s*(?:（1）)?【(?:答案|参考代码|证明|解|解答)", atext, re.M
            )
        ]
        if qnums != list(range(1, len(qnums) + 1)):
            issues.append(f"题号不连续 {course}/{q.name}: {qnums}")
        if sorted(set(anums)) != sorted(set(qnums)):
            issues.append(
                f"题解不对齐 {course}/{q.name}: 题 {len(set(qnums))} 道 / 解析 {len(set(anums))} 道"
            )
    return issues


def main():
    if not ROOT.is_dir():
        print(f"找不到目录：{ROOT}")
        return 1

    total_issues = []
    print("=" * 60)
    print("电子书蒸馏 · 体检报告")
    print("=" * 60)

    grand = 0
    for course, mins in COURSES.items():
        if not (ROOT / course).is_dir():
            continue
        print(f"\n[{course}]")
        layers = LAYERS_EN if course == "05-英语" else LAYERS
        for layer in layers:
            issues, n = check_layer(course, layer, mins[layer])
            grand += n
            flag = "OK" if not issues else f"{len(issues)} 处问题"
            print(f"  {layer:<8} {n:>3} 个文件   {flag}")
            total_issues.extend(issues)
        total_issues.extend(check_single_files(course))
        total_issues.extend(check_question_alignment(course))

    print(f"\n合计文件：{grand}")
    if total_issues:
        print(f"\n问题清单（{len(total_issues)} 条）：")
        for i in total_issues:
            print("  -", i)
        return 1
    print("\n全部通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
