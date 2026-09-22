# -*- coding: utf-8 -*-
"""Generate English exam notes from extracted PDF text."""
from pathlib import Path
import re

ROOT = Path(r"D:/专升本/专升本")
BY = ROOT / "资料/英语真题原卷/_by_year"
NOTES = ROOT / "历年真题/公共英语"
EXTRACT = ROOT / "资料/英语真题原卷/_extract"
BY.mkdir(parents=True, exist_ok=True)
NOTES.mkdir(parents=True, exist_ok=True)

WRITING = {
    2024: {
        "genre": "邀请邮件（写作竞赛）",
        "prompt": (
            "假定你是李华。你校英文报面向交换生举办主题为 “China in My Eyes” 的写作比赛，"
            "请给交换生 Mark 写一封邮件邀请他参赛。需包含：比赛主题与对象；字数要求（500 词内）；"
            "截止日期（11 月 10 日）；鼓励参赛。"
        ),
        "sample": (
            "Dear Mark,\n\n"
            "I'm Li Hua. Our school English newspaper is holding a writing contest named "
            '"China in My Eyes" for exchange students. You need to write about your view of China '
            "within 500 words. The deadline is November 10th. It's a great chance to share your "
            "thoughts. I believe you have unique insights. So come and join it!\n\n"
            "Best regards,\nLi Hua"
        ),
    },
    2023: {
        "genre": "应用文（以当年卷面为准）",
        "prompt": "以当年正式试卷写作题为准。本库已收录该年客观题与答案解析；写作请对照本地 PDF《英语真题和答案_2013-2023》。近年稳为书信/通知类约 100 词。",
        "sample": "",
    },
    2022: {
        "genre": "应用文（以当年卷面为准）",
        "prompt": "以当年正式试卷写作题为准。近年常见：通知/书信，约 100 词。对照本地 PDF。",
        "sample": "",
    },
    2021: {
        "genre": "回复邮件",
        "prompt": (
            "假定你是李华。留学生 Tom 发邮件询问你校健身房情况，请写邮件回复，包含："
            "(1) 健身房基本信息（开放时间、位置、教练/培训等）；(2) 预约方式与收费。"
            "参考词：gym / coach。约 100–120 词。"
        ),
        "sample": (
            "Dear Tom,\n\n"
            "I'm glad to hear from you. Here is some information about our school gym.\n\n"
            "The gym is next to the library and opens from 8:00 a.m. to 9:00 p.m. every day. "
            "There are many kinds of equipment, and professional coaches can provide personal training.\n\n"
            "If you want to use the gym, you need to make a reservation online or at the front desk. "
            "The monthly fee is about 100 yuan for students.\n\n"
            "I hope you will enjoy working out there. Looking forward to seeing you!\n\n"
            "Best wishes,\nLi Hua"
        ),
    },
    2020: {
        "genre": "NOTICE（讲座通知）",
        "prompt": (
            "校图书馆将为经济学院学生举办讲座，请以图书馆名义写英语通知："
            "时间 2020-06-15 下午 2 点；地点 教学楼演讲厅；主题“一带一路与中国经济”；"
            "主讲人为王博士（经济学）。约 ≥100 词。"
        ),
        "sample": (
            "                    NOTICE\n\n"
            "To help students better understand China's economy, the library will hold a lecture "
            "for the School of Economics.\n"
            "Time: 2:00 p.m., June 15th, 2020\n"
            "Place: the Lecture Hall in the Teaching Building\n"
            "Topic: The Belt and Road Initiative and China's Economy\n"
            "Speaker: Dr. Wang\n\n"
            "Anyone who is interested is welcome to attend. Please arrive on time.\n"
            "If you have any questions, please contact the library.\n\n"
            "                                          The Library\n"
            "                                          June 10th, 2020"
        ),
    },
    2019: {
        "genre": "NOTICE（招聘会）",
        "prompt": (
            "一家跨国公司将于 2019-03-11 下午 2:30 在学校体育馆举办招聘会。"
            "请为学生会写英语通知：参加对象；时间地点；需携带材料"
            "（身份证、学生证、个人简历、英语应用能力考试合格证等）。约 ≥100 词。"
        ),
        "sample": (
            "                    NOTICE\n\n"
            "A multinational company will hold a job fair in our school gym at 2:30 p.m. "
            "on March 11th, 2019.\n"
            "All graduates who are looking for a job are welcome.\n"
            "Please bring your ID card, student card, resume, and the certificate of PRETCO "
            "if you have one.\n"
            "For more information, please contact the Student Union.\n\n"
            "                                          The Student Union\n"
            "                                          March 5th, 2019"
        ),
    },
    2018: {
        "genre": "邀请信（毕业晚会）",
        "prompt": (
            "你校将举办毕业晚会，节目丰富（唱歌、跳舞、游戏等）。"
            "时间 5 月 28 日 19:30，地点教学楼 502，约两小时。"
            "欢迎老师和全体同学参加。请写信邀请外教 Robert 出席并致辞。"
        ),
        "sample": (
            "Dear Robert,\n\n"
            "I'm writing to invite you to our graduation party.\n"
            "It will be held in Room 502 of the Teaching Building at 7:30 p.m. on May 28th "
            "and will last about two hours.\n"
            "There will be singing, dancing, games and many other activities. "
            "All teachers and students are welcome.\n"
            "We sincerely hope you can come and give a short speech. "
            "We are looking forward to your reply.\n\n"
            "Yours sincerely,\nLi Hua"
        ),
    },
    2017: {
        "genre": "投诉信",
        "prompt": (
            "你参加了某旅行社组织的旅游，过程中有诸多问题。"
            "请给客服写投诉信：说明问题（酒店/饮食/交通/导游等）并提出希望的解决办法。约 100 词。"
        ),
        "sample": (
            "Dear Sir or Madam,\n\n"
            "I am writing to complain about the trip organized by your travel agency last week.\n"
            "First, the hotel was dirty and noisy. Second, the food was terrible and the bus was "
            "always late. What is more, the guide was impatient.\n"
            "I hope you can improve your service and give me a partial refund.\n"
            "I am looking forward to your early reply.\n\n"
            "Yours faithfully,\nLi Hua"
        ),
    },
    2016: {
        "genre": "求职信",
        "prompt": "根据自己的经历写一封应聘某校英语教师的求职信，可包含教育背景、获奖、特长等。约 100 词。",
        "sample": (
            "Dear Sir or Madam,\n\n"
            "I am writing to apply for the position of English teacher in your school.\n"
            "I graduated from Guangdong University with a bachelor's degree in English. "
            "I have won several awards in speech contests and I am good at handwriting and office software.\n"
            "I am patient, responsible and love teaching. "
            "I would be grateful if you could offer me an interview.\n\n"
            "Yours sincerely,\nLi Hua"
        ),
    },
    2015: {
        "genre": "NOTICE（演讲比赛）",
        "prompt": "为外国学生写一则举办英语演讲比赛的通知，包含：比赛主题、参加人员、时间、地点等。",
        "sample": (
            "                    NOTICE\n\n"
            "An English Speech Contest will be held for international students.\n"
            "Theme: My Life in China\n"
            "Time: 2:00 p.m., next Friday\n"
            "Place: the Lecture Hall\n"
            "Anyone who is interested is welcome to join us. "
            "Please sign up at the Student Union office before Wednesday.\n\n"
            "                                          The Student Union\n"
            "                                          April 10th, 2015"
        ),
    },
    2014: {
        "genre": "劝说信",
        "prompt": "你的好友沉迷网络游戏影响学习，多门课不及格。写一封信说明沉迷网游的危害，劝他珍惜学习时间、学好专业知识。",
        "sample": (
            "Dear friend,\n\n"
            "I am worried about you because you indulge in online games and have failed several courses.\n"
            "Playing games too much not only wastes time but also harms your health and future.\n"
            "I hope you can give up the games, treasure your school years and work hard on your major.\n"
            "I believe you can make it. I am always here to help you.\n\n"
            "Yours,\nLi Hua"
        ),
    },
    2013: {
        "genre": "介绍校园社团",
        "prompt": "外国留学生对中国校园社团活动很感兴趣。请写一封信介绍某一个校园社团：加入原因、组织结构、目前活动、你喜欢什么。",
        "sample": (
            "Dear friend,\n\n"
            "I'm glad to introduce our English Club to you.\n"
            "I joined it because I want to practice spoken English. "
            "The club has a president and several departments. "
            "We hold speech contests, movie nights and free talks every week.\n"
            "I especially like the free talk sessions, where I can make friends and improve my English.\n"
            "You are welcome to join us!\n\n"
            "Yours,\nLi Hua"
        ),
    },
}


def load_text(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def extract_answer_letters(ans: str) -> str:
    keys = []
    for m in re.finditer(r"(?m)^\s*(\d{1,2})[\.、．\)]\s*([A-Da-d])\b", ans):
        keys.append((int(m.group(1)), m.group(2).upper()))
    if not keys:
        return ""
    seen = {}
    for n, a in keys:
        if n not in seen:
            seen[n] = a
    items = [f"{n}.{seen[n]}" for n in sorted(seen)]
    lines = []
    for i in range(0, len(items), 10):
        lines.append(" ".join(items[i : i + 10]))
    return "\n".join(lines)


def structure_hint(year: int) -> str:
    if year >= 2021:
        return (
            "| 题型（近年常见） | 约分 | 说明 |\n"
            "|:---|---:|:---|\n"
            "| 阅读理解 | ~30 | 多篇短文 / 信息匹配 |\n"
            "| 完形填空 | ~20–30 | 词汇+语法+语篇 |\n"
            "| 语法 / 词汇 | ~15–30 | 单选或语法填空 |\n"
            "| 写作 | 15 | 应用文约 100 词 |"
        )
    return (
        "| 题型（较早年份常见） | 约分 | 说明 |\n"
        "|:---|---:|:---|\n"
        "| Vocabulary and Structure | 30–35 | 词汇语法单选 |\n"
        "| Reading Comprehension | ~40 | 多篇阅读 |\n"
        "| Cloze | ~10–20 | 完形 |\n"
        "| Writing | 15 | 应用文 |"
    )


def gen_note(year: int, paper: str, answers: str) -> str:
    w = WRITING.get(
        year,
        {
            "genre": "应用文",
            "prompt": "见本地 PDF 原卷写作部分",
            "sample": "",
        },
    )
    key_table = extract_answer_letters(answers)

    paper_preview = re.sub(r"(?m)^专插本资讯.*$", "", paper)
    paper_preview = re.sub(r"(?m)^公众号：.*$", "", paper_preview)
    paper_preview = re.sub(r"\n{3,}", "\n\n", paper_preview).strip()
    if len(paper_preview) > 14000:
        paper_preview = paper_preview[:14000] + "\n\n…（全文见本地 PDF / `_by_year` 抽取文本）\n"

    ans_preview = answers
    if len(ans_preview) > 10000:
        ans_preview = ans_preview[:10000] + "\n\n…（完整解析见本地 PDF）\n"

    if w.get("sample"):
        sample_block = (
            "### 参考范文\n\n"
            "```\n"
            f"{w['sample']}\n"
            "```\n\n"
            "**得分点：** 格式正确 · 要点齐全 · 约 100 词 · 少语法硬伤\n"
        )
    else:
        sample_block = "### 参考范文\n\n> 范文请对照本地 PDF 或使用 [[作文模板与高分句型]] 自行套写。\n"

    if answers:
        key_body = key_table or "（字母速查未完整识别时，请看下方解析摘录 / 本地 PDF）"
        key_block = f"## 客观题答案速查\n\n```\n{key_body}\n```\n"
    else:
        key_block = "## 客观题答案\n\n> 本年份答案请对照本地 PDF，或见下方解析摘录。\n"

    if paper and answers:
        status = "完整卷面+解析（OCR 抽取，个别空格/标点可能有误）"
    elif paper:
        status = "有卷面抽取"
    elif answers:
        status = "有部分解析"
    else:
        status = "骨架+写作"

    md = f"""# 公共英语 · {year} 年真题详解

> **资料层级：A/B** · 来自主人提供的广东专插本英语真题 PDF 抽取整理
> 写作体裁：**{w['genre']}** · 状态：**{status}**
> 本地原卷：`资料/英语真题原卷/` · 见 [[00-资料来源与使用说明]] · [[_索引]]

---

## 试卷结构（备考用）

{structure_hint(year)}

> 具体题量/分值以当次正式卷为准；OCR 可能漏题号，刷题时以 PDF 为准。

---

## 写作（必背）

**题目方向：** {w['prompt']}

{sample_block}
### 审题清单
- [ ] 体裁（书信 / NOTICE）与称呼落款
- [ ] 时间 / 地点 / 对象 / 目的 信息齐全
- [ ] 90–120 词，分段清楚
- [ ] 无中式英语硬伤

---

{key_block}

## 答案解析摘录

> 以下从 PDF 抽取，中文解析保留；英文题干若粘连，可对照 `资料/英语真题原卷/_by_year/{year}-*.txt` 或原 PDF。

```
{ans_preview if ans_preview else '（暂无独立答案页抽取）'}
```

---

## 卷面正文（OCR）

<details>
<summary>点击展开 {year} 年试卷抽取文本（较长）</summary>

```
{paper_preview if paper_preview else '（扫描件或未收录卷面文本；请打开本地 PDF）'}
```

</details>

---

## 复盘法（本年通用）

1. **阅读**：题干关键词 → 回原文定位 → 排除绝对化选项
2. **完形**：先通读 → 搭配优先 → 语法兜底
3. **词汇语法**：时态语态 / 非谓语 / 从句 / 固定搭配
4. **写作**：每周默写 1 篇同体裁
5. **错题登记**：单词 | 错因 | 正确搭配

---

## 资料文件

| 文件 | 说明 |
|:---|:---|
| `资料/英语真题原卷/` | 主人上传的 PDF 原件（本地，默认不进 Git 大文件） |
| `资料/英语真题原卷/_by_year/{year}-paper.txt` | 本年卷面抽取 |
| `资料/英语真题原卷/_by_year/{year}-answers.txt` | 本年答案/解析抽取 |

---

返回：[[_索引]] · [[总索引]] · [[作文模板与高分句型]] · [[英语知识库]]
"""
    return md


def split_old_2008_2012():
    old_txt = None
    old_path = None
    for p in EXTRACT.glob("*.txt"):
        t = p.read_text(encoding="utf-8")
        parts = re.split(r"\n===== PAGE (\d+)/\d+ =====\n", t)
        n_pages = (len(parts) - 1) // 2
        if n_pages == 50:
            old_txt = t
            old_path = p
            break
    if not old_txt:
        print("no 50-page extract for 2008-2012")
        return []

    print("old papers file:", old_path.name)
    parts = re.split(r"\n===== PAGE (\d+)/\d+ =====\n", old_txt)
    page_map = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}

    starts = {}
    for n, c in sorted(page_map.items()):
        head = "\n".join(c.splitlines()[:10])
        m = re.search(r"广东省\s*(200[8-9]|201[0-2])\s*年", head)
        if m:
            y = int(m.group(1))
            if y not in starts:
                starts[y] = n
                print(f"  {y} starts page {n}")

    if 2012 not in starts:
        # page 1 was 2012 in earlier inspection
        starts[2012] = 1
    # fill missing years with approximate page ranges if needed
    if len(starts) < 5:
        # known from earlier: 2012@1, 2011@10, 2009@31
        defaults = {2012: 1, 2011: 10, 2010: 20, 2009: 31, 2008: 41}
        for y, st in defaults.items():
            starts.setdefault(y, st)
        print("filled defaults:", starts)

    generated = []
    ys = sorted(starts.items())
    for i, (y, st) in enumerate(ys):
        en = ys[i + 1][1] - 1 if i + 1 < len(ys) else max(page_map)
        if st > en:
            continue
        paper = "\n\n".join(page_map[n] for n in range(st, en + 1) if n in page_map)
        (BY / f"{y}-paper.txt").write_text(paper, encoding="utf-8", newline="\n")
        md = gen_note(y, paper, "")
        (NOTES / f"{y}.md").write_text(md, encoding="utf-8", newline="\n")
        generated.append(y)
        print(f"wrote early {y}.md pages {st}-{en} chars={len(paper)}")
    return generated


def main():
    generated = []
    for y in range(2013, 2025):
        paper = load_text(BY / f"{y}-paper.txt")
        answers = load_text(BY / f"{y}-answers.txt")
        if y == 2024:
            answers = load_text(BY / "2024-answers-partial.txt") or answers
        md = gen_note(y, paper, answers)
        path = NOTES / f"{y}.md"
        path.write_text(md, encoding="utf-8", newline="\n")
        generated.append(y)
        print(f"wrote {y}.md md={len(md)} paper={len(paper)} ans={len(answers)}")

    early = split_old_2008_2012()
    print("main years:", generated)
    print("early years:", early)


if __name__ == "__main__":
    main()
