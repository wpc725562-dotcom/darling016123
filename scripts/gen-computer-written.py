# -*- coding: utf-8 -*-
"""把真题的手写部分（填空/简答/计算/应用）生成可折叠练习页。
源：历年真题/计算机程序设计/2024.md + docs/posts/computer/2025-真题回忆版.md
产物：docs/posts/题库/计算机手写题.md
"""
import re, pathlib, json
from collections import OrderedDict

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = [
    ("2024", "历年真题/计算机程序设计/2024.md"),
    ("2025", "docs/posts/computer/2025-真题回忆版.md"),
]
WANT = ["三、填空题", "四、简答题", "五、计算题", "六、应用题"]
ORDER = ["填空题", "简答题", "计算题", "应用题"]
PER = {"填空题": "每题 4 分", "简答题": "每题 10 分", "计算题": "每题 10 分", "应用题": "每题 10 分"}

# ---------- 考点 → 笔记链接 ----------
NOTE_DIR = ROOT / "docs/posts/computer/notes"
note_map = {}
for f in NOTE_DIR.glob("*.md"):
    m = re.match(r'^(\d+\.\d+)-(.+)$', f.stem)
    if m:
        note_map[m.group(1)] = f"/posts/computer/notes/{f.stem}"


def wiki_to_link(m):
    """[[2.1 数据结构基本概念]] → markdown 链接（有笔记则链，无则纯文本）"""
    inner = m.group(1)
    label = (m.group(2) or inner).strip()
    num = inner.split(" ")[0].strip()
    url = note_map.get(num)
    return f"[{label}]({url})" if url else label


def conv(s: str) -> str:
    return re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', wiki_to_link, s)


def point_to_md(p: str) -> str:
    """考点统一成 markdown 链接。已是链接/含 [[ ]] 的走 conv()。"""
    if not p:
        return ""
    if '[[' in p:
        return conv(p)
    # 纯文本「1.2 数据的存储与运算」→ 链接
    m = re.match(r'^(\d+\.\d+)\s+(.+)$', p)
    if m and note_map.get(m.group(1)):
        return f'[{p}]({note_map[m.group(1) ]})'
    return p


def hoist_figure(body: str):
    """题干里说「对下图」，图却藏在答案里 → 把开头的非代码图（无 `;` / #include）
    提到答案折叠块之外，否则学习者看不到题。
    ★ 图用 ```text:no-line-numbers —— 站点开了全局 lineNumbers，
      给 ASCII 图编号会被误读成「树的层号」。"""
    m = re.match(r'```[a-z]*\n([\s\S]*?)```\s*', body.strip())
    if not m:
        return None, body
    code = m.group(1)
    if re.search(r'#include|printf|scanf|;', code):
        return None, body
    fig = '```text:no-line-numbers\n' + code.rstrip('\n') + '\n```'
    return fig, body[m.end():].strip()


def clean_title(t: str) -> str:
    t = re.sub(r'[🔄✅⚠️]', '', t).strip()
    t = re.sub(r'^\d+[\.、]\s*', '', t)   # 去掉源里的「1. 」序号（标题里已自带）
    # 裸露的下划线占位符会被 markdown 当成斜体，包进反引号
    t = re.sub(r'(?<![`\w])_{4,}', lambda m: '`' + m.group(0) + '`', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def extract_point(rest: str):
    """把考点从正文里剥出来。源里有三种写法：
    1) 独立行 `**考点** [[2.1 数据结构基本概念]]`
    2) 答案行内联 `> **答案：3** · 考点 **1.2 数据的存储与运算**`
    3) 答案行尾 `**答案：2** · [[1.6 数组]]`
    """
    point = ""

    # 1) 独立行
    m = re.search(r'(?m)^\*\*考点\*\*\s*[：:]?\s*(.+?)\s*$', rest)
    if m:
        line = m.group(1)
        line = re.split(r'\s*·\s*拆练', line)[0]   # 去掉「· 拆练 [[...]]」尾巴
        point = line.strip()
        rest = rest[:m.start()] + rest[m.end():]

    # 2) 内联 `· 考点 **xxx**`
    m2 = re.search(r'\s*·\s*考点\s*\*\*([^*]+)\*\*', rest)
    if m2:
        if not point:
            point = m2.group(1).strip()
        rest = rest[:m2.start()] + rest[m2.end():]

    # 3) 答案行尾的 `· [[x.y …]]`
    m3 = re.search(r'(?m)^(\*\*答案[^\n]*?)\s*·\s*\[\[([^\]|]+)(?:\|[^\]]+)?\]\][^\n]*$', rest)
    if m3:
        if not point:
            point = m3.group(2).strip()
        rest = rest[:m3.start()] + m3.group(1) + rest[m3.end():]

    return point, rest.strip()


def parse_file(year, rel):
    text = (ROOT / rel).read_text(encoding="utf-8")
    out = []
    for seg in re.split(r'(?m)^##\s+', text)[1:]:
        head, _, body = seg.partition("\n")
        head = head.strip()
        kind = next((w for w in WANT if head.startswith(w)), None)
        if not kind:
            continue
        for q in re.split(r'(?m)^###\s+', body)[1:]:
            t, _, rest = q.partition("\n")
            rest = re.sub(r'\n-{3,}\s*$', '', rest.strip()).strip()
            if not rest:
                continue
            point, rest = extract_point(rest)
            fig, rest = hoist_figure(rest)
            out.append({
                "year": year, "kind": kind[2:],
                "title": clean_title(t), "body": rest, "figure": fig,
                "point": point, "src": rel,
            })
    return out


rows = []
for y, f in SRC:
    rows += parse_file(y, f)

# ---------- 生成 markdown ----------
L = []
L.append('---')
L.append('title: "计算机手写题专项（填空 · 简答 · 计算 · 应用）"')
L.append('description: "2024/2025 广东专插本计算机真题的 120 分手写部分，30 题不重复。先自己在纸上做，再展开对答案。"')
L.append('category: "quiz"')
L.append('---')
L.append('')
L.append('# 计算机手写题专项')
L.append('')
L.append('> **选择题刷得再熟，也不会自动变成手写能力。**')
L.append('>')
L.append('> 真卷 200 分里，[选择题 + 判断题](/posts/题库/计算机真题刷题) 只占 **80 分**。')
L.append('> 剩下 **120 分全是手写**：填空 20 + 简答 40 + 计算 30 + 应用 30。')
L.append('> 这一页就是那 120 分 —— **30 道真题，2024 与 2025 完全不重复**。')
L.append('>')
L.append('> 用法：**先在纸上写，写完再点开对答案。** 直接看答案等于没做。')
L.append('')
L.append('## 真卷结构（200 分 / 150 分钟）')
L.append('')
L.append('| 题型 | 题量 × 分值 | 小计 | 在哪练 |')
L.append('|:---|:---|:---:|:---|')
L.append('| 一、单项选择题 | 20 × 3 | 60 | [交互式题库](/posts/题库/计算机真题刷题) |')
L.append('| 二、判断题 | 10 × 2 | 20 | [交互式题库](/posts/题库/计算机真题刷题) |')
L.append('| 三、填空题 | 5 × 4 | 20 | **本页** |')
L.append('| 四、简答题 | 4 × 10 | 40 | **本页** |')
L.append('| 五、计算题 | 3 × 10 | 30 | **本页** |')
L.append('| 六、应用题 | 3 × 10 | 30 | **本页** |')
L.append('| **合计** | | **200** | 手写占 **120 / 200 = 60%** |')
L.append('')
L.append('> ⚠️ **2025 卷标注为「回忆版」**，题干与答案来自考生回忆 + 站内整理，与官方真题可能有出入；2024 卷为完整版。')
L.append('')

kinds = OrderedDict()
for r in rows:
    kinds.setdefault(r["kind"], []).append(r)

CN = {"填空题": "三", "简答题": "四", "计算题": "五", "应用题": "六"}
for kind in ORDER:
    items = kinds.get(kind, [])
    if not items:
        continue
    L.append(f'## {CN[kind]}、{kind}（{len(items)} 题 · {PER[kind]}）')
    L.append('')
    for i, it in enumerate(items, 1):
        pts = point_to_md(it["point"])
        L.append(f'### {kind[0]}{i}｜{it["title"]}')
        L.append('')
        meta = [f'`{it["year"]}`']
        if pts:
            meta.append('考点：' + pts)
        L.append(' · '.join(meta))
        L.append('')
        if it.get("figure"):
            L.append(it["figure"])
            L.append('')
        L.append('<details>')
        L.append('<summary>💡 查看参考答案</summary>')
        L.append('')
        L.append(conv(it["body"]))
        L.append('')
        L.append('</details>')
        L.append('')

L.append('---')
L.append('')
L.append('## 维护方式')
L.append('')
L.append('本页**自动生成，不要手改**。源是真题 md 里的 `## 三/四/五/六、…` 小节：')
L.append('')
L.append('- `历年真题/计算机程序设计/2024.md`')
L.append('- `docs/posts/computer/2025-真题回忆版.md`')
L.append('')
L.append('```bash')
L.append('# 在仓库根目录执行')
L.append('python scripts/gen-computer-written.py')
L.append('```')
L.append('')
L.append('**新增年份的手写题**：在源 md 里加一个 `## 三、填空题（…）` 这样的小节，')
L.append('每题用 `### N. 题干` 起头，答案写成 `**答案：xxx**`（2024 风格）或')
L.append('`> **答案：xxx** · 考点 **1.2 数据的存储与运算**`（2025 风格）都认，重跑脚本即可。')
L.append('')
L.append('> 判断题/选择题**不在本页** —— 那部分在 [计算机真题刷题](/posts/题库/计算机真题刷题)，')
L.append('> 由 `scripts/gen-computer-quiz.py` 生成。两个脚本互不干扰。')
L.append('')
L.append('**相关**：[题库总入口](/posts/题库/) · [🖥️ 计算机真题刷题（80 分那部分）](/posts/题库/计算机真题刷题)')
L.append('')

out = ROOT / "docs/posts/题库/计算机手写题.md"
out.write_text('\n'.join(L), encoding='utf-8')
print("写入:", out)
print("字节:", out.stat().st_size)
from collections import Counter
c = Counter(r["kind"] for r in rows)
for k in ORDER:
    print(f"  {k}: {c.get(k,0)}")
print("合计:", len(rows))
print("带考点:", sum(1 for r in rows if r["point"]))
