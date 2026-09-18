#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把计算机真题 md 解析成 QuizCard 用的题库 TS 文件（单选 + 判断），带考点。"""
import re, json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_TS = ROOT / "docs/.vitepress/theme/components/quiz-computer.ts"

SOURCES = []
for d in [ROOT / "历年真题/计算机程序设计", ROOT / "docs/posts/computer"]:
    if d.is_dir():
        SOURCES += sorted(d.glob("*.md"))

def clean(s: str) -> str:
    s = s.strip()
    s = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', lambda m: (m.group(2) or m.group(1)), s)
    s = s.replace('**', '').replace('`', '')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def is_point_noise(p: str) -> bool:
    """判断一段是不是「只有考点、没有解析」。

    ★ 为什么需要它：判断题的答案行尾常跟一个考点链接，**真解析在它下面一段**：
        **答案：√** · [[2.2 线性表]]
        <空行>
        线性表基本特性（首元无前驱，末元无后继）。
    只取「答案行后的第一段」→ explain 变成考点名。实测 2024 判断题 10/10 中招。
    """
    s = re.sub(r'\[\[[^\]]*\]\]', '', p)            # wiki 链接整体去掉
    s = re.sub(r'\[[^\]]*\]\([^)]*\)', '', s)        # markdown 链接整体去掉
    s = re.sub(r'考点\s*\*\*[^*]*\*\*', '', s)        # 考点 **1.2 数据的存储与运算**
    s = re.sub(r'考点', '', s)
    s = re.sub(r'[·|>#*\s:：]', '', s)
    return len(s) == 0


def clean_block(s: str) -> str:
    """解析用：保留换行（解析里常有编号步骤列表，压成一行就没法读了）"""
    s = s.strip()
    s = s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
    s = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', lambda m: (m.group(2) or m.group(1)), s)
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
    s = s.replace('**', '').replace('`', '')
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

OPT_LINE = re.compile(r'^\s*([A-D])\s*[\.、:：]\s*(.+?)\s*$', re.M)
OPT_INLINE = re.compile(
    r'A\s*[\.、:：]\s*(.+?)\s+B\s*[\.、:：]\s*(.+?)\s+C\s*[\.、:：]\s*(.+?)\s+D\s*[\.、:：]\s*(.+?)\s*$',
    re.M | re.S)

def parse(path: pathlib.Path):
    txt = path.read_text(encoding='utf-8', errors='replace')
    # ★ 只按 ### 切题；题干块在遇到下一个 ## 小节时截止
    chunks = re.split(r'\n#{3,4}[ \t]*(\d+)[ \t]*[\.、][ \t]*', txt)
    out = []
    for k in range(1, len(chunks) - 1, 2):
        num, blk = chunks[k], chunks[k + 1]
        blk = re.split(r'\n##(?!#)', blk)[0]          # 不跨小节
        m_ans = re.search(r'\*\*答案\s*[:：]\s*(.+?)\*\*', blk)
        if not m_ans:
            continue
        raw = m_ans.group(1).strip()
        head, tail = blk[:m_ans.start()], blk[m_ans.end():]

        if re.match(r'^[A-Da-d]$', raw):
            answer = ord(raw.upper()) - 65
            m = OPT_INLINE.search(head)
            if m:
                qtext, options = head[:m.start()], [m.group(x) for x in (1, 2, 3, 4)]
            else:
                opts = OPT_LINE.findall(head)
                if len(opts) < 4:
                    continue
                qtext = re.split(r'\n\s*A\s*[\.、:：]', head)[0]
                options = [o[1] for o in opts[:4]]
            kind = '单选'
        elif raw in ('√', '×', '对', '错', '正确', '错误'):
            answer = 0 if raw in ('√', '对', '正确') else 1
            qtext, options, kind = head, ['正确', '错误'], '判断'
        else:
            continue

        # ★ 解析标记的写法不止一种：`**解析**：` / `**解析**（下标 0…6，已升序）：`
        #   括号可能在冒号前面 —— 只认冒号会漏掉一大批。
        #   终止条件是下一个 ### 小题 / --- 分隔线，且**要保留换行**（解析常有编号步骤）。
        m_exp = re.search(r'\*\*解析\*\*\s*(?:（[^）]*）)?\s*[:：]?\s*(.+?)(?=\n---|\n#{2,4}\s|\Z)', blk, re.S)
        if m_exp and m_exp.group(1).strip():
            explain = clean_block(m_exp.group(1))
        else:
            # 判断题/简写题没有 **解析** 标记，解析 = 答案行之后的正文。
            # ★ 不能只取第一段：答案行尾的考点链接自成一段，真解析在下一段。
            #   逐段跳过「纯考点/纯链接」段，取第一段有实质内容的。
            #   （实测：只取第一段 → 2024 判断题 10/10 的解析变成考点名）
            explain = ''
            for p in re.split(r'\n\s*\n', tail):
                if is_point_noise(p):
                    continue
                cand = clean_block(p)
                if len(cand) > 3:
                    explain = cand
                    break
        if len(explain) > 600:
            explain = explain[:600].rstrip() + '…'

        m_pt = re.search(r'\[\[([^\]|]+)', blk)
        point = clean(m_pt.group(1)) if m_pt else ''
        mc = re.match(r'^([12]\.\d+)', point)
        chapter = mc.group(1) if mc else ''

        q = clean(qtext)
        options = [clean(o) for o in options]
        if not q or len(q) > 260 or any(not o for o in options):
            continue
        out.append({"q": q, "options": options, "answer": answer, "explain": explain,
                    "point": point, "chapter": chapter, "kind": kind, "year": path.stem})
    return out

allq = []
for s in SOURCES:
    got = parse(s)
    if got:
        print(f"  {s.name:32} → {len(got):3} 题")
        allq += got

seen, uniq = set(), []
for q in allq:
    key = re.sub(r'\W', '', q["q"])[:50]
    if key in seen:
        continue
    seen.add(key)
    uniq.append(q)

print(f"\n合计 {len(allq)} → 去重 {len(uniq)} 题")
print(f"  单选 {sum(1 for q in uniq if q['kind']=='单选')} / 判断 {sum(1 for q in uniq if q['kind']=='判断')}")
print(f"  带解析 {sum(1 for q in uniq if q['explain'])}/{len(uniq)}")
print(f"  带考点 {sum(1 for q in uniq if q['point'])}/{len(uniq)}")
print("\n按考点章节:")
for k, v in sorted(Counter(q["chapter"] or "(无)" for q in uniq).items()):
    print(f"   {k:10} {v:3}")

json.dump(uniq, open("C:/tmp/computer-quiz.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

WARMUP = [
 ("关于C语言程序，下列叙述正确的是？", ["C语言本身提供输入输出语句","每条语句末尾可以省略分号","程序总是从第一个定义的函数开始执行","C源程序必须包含一个main函数"], 3, "C程序由函数构成且必须包含main函数，程序从main开始执行；输入输出由库函数完成，语句末尾须有分号。"),
 ("十进制数9对应的二进制数是？", ["1001","1010","1000","0110"], 0, "十进制转二进制用除2取余法，9=8+1，对应二进制1001。"),
 ("表达式 19%4 的值是？", ["4.75","4","0","3"], 3, "%为求余运算符，要求两侧均为整数，19÷4=4余3，结果为3。"),
 ("设 int a=2, b=3; 则表达式 !a||b 的值为？", ["1","0","2","3"], 0, "!优先级最高，!a=!2=0；b非零为真，0||1=1。"),
 ("关于switch语句，下列叙述正确的是？", ["每个case标号后必须使用break语句","case标号只起标记作用，执行完一个case后继续执行后续case，一般用break跳出","执行完一个case后会自动跳出switch结构","各case标号的常量值可以相同"], 1, "case只起标记作用、不再判断，执行后继续后续case，需用break跳出；各case常量必须互不相同。"),
 ("下列关于break和continue语句的叙述，正确的是？", ["continue语句可用于switch语句中","break只结束本次循环而不终止整个循环","break和continue作用完全相同","continue结束本次循环，break结束整个循环"], 3, "continue只结束本次循环继续下一次判断，break结束整个循环；break可用于switch而continue不能。"),
 ("设有定义 int a[10]={1,2,3}; 则 a[5] 的值是？", ["3","0","5","随机值"], 1, "数组部分初始化时，未赋初值的元素自动取0，故a[5]=0。"),
 ("递归函数定义为 age(1)=10, age(n)=age(n-1)+2 (n>1)，则 age(5) 的值是？", ["14","16","20","18"], 3, "age(5)=age(4)+2=…=age(1)+8=10+8=18。"),
 ("设有 int a[5]={1,2,3,4,5}, *p=a; 则 *(p+2) 的值是？", ["1","3","2","4"], 1, "p指向a[0]，p+2指向a[2]，*(p+2)即a[2]=3。"),
 ("关于共用体(union)类型，下列叙述正确的是？", ["共用体变量所占内存长度等于最长成员的长度","共用体变量所占内存长度等于各成员长度之和","共用体各成员分别占有独立的内存单元","共用体与结构体内存分配方式完全相同"], 0, "共用体各成员共享同一段内存，所占长度等于最长成员的长度；结构体则是各成员长度之和。"),
 ("关于链式存储结构(链表)，下列叙述正确的是？", ["逻辑上相邻的元素在物理上也一定相邻","可以随机存取表中任一元素，时间复杂度为O(1)","插入、删除只需修改指针，不必移动大量元素","存储密度等于1"], 2, "链表逻辑相邻物理不一定相邻，采用顺序存取，插入删除仅改指针，但存储密度小于1。"),
 ("栈的运算遵循的原则是？", ["先进先出(FIFO)","随机存取","后进先出(LIFO)","顺序存取"], 2, "栈是只能在栈顶进行插入和删除的线性表，访问结点按后进先出(LIFO)原则；FIFO是队列。"),
 ("若一棵二叉树中度为2的结点数 n2=5，则叶子结点数 n0 为？", ["4","5","6","7"], 2, "二叉树性质3：叶子数 n0 = 度为2的结点数 n2 + 1，故 n0=5+1=6。"),
 ("折半查找(二分查找)要求线性表必须？", ["采用顺序存储结构且元素按关键字有序","采用链式存储结构","元素个数不超过10","关键字为字符型"], 0, "折半查找适用于顺序存储的有序表，不宜用于链式结构，时间复杂度O(log₂n)。"),
 ("下列内部排序算法中，不稳定的是？", ["直接插入排序","快速排序","起泡排序","选择排序"], 1, "快速排序不稳定，平均时间复杂度O(n log₂n)；直接插入、起泡、选择排序均为稳定排序。"),
]

rows = [{"q": q, "options": o, "answer": a, "explain": e, "point": "零基础热身",
         "chapter": "0.0", "kind": "单选", "year": "热身"} for q, o, a, e in WARMUP]
rows += uniq

def ts(s):
    """JS 单引号字符串。★ 解析现在保留换行，必须把 \n 转成 \\n —— 否则生成的 TS 语法错误。"""
    return "'" + (s.replace('\\', '\\\\').replace("'", "\\'")
                   .replace('\r', '').replace('\n', '\\n')) + "'"

L = [
 "// ⚠️ 自动生成，不要手改 —— 改题库请改源 md 后重跑 C:/tmp/gen-quiz-ts.py",
 "// 源：历年真题/计算机程序设计/*.md + docs/posts/computer/*.md（2018–2026 真题）",
 "// 题量：零基础热身 15 + 真题单选/判断（按题干去重）",
 "",
 "export interface QuizQuestion {",
 "  q: string",
 "  options: string[]",
 "  answer: number",
 "  explain: string",
 "  /** 考点名，如「1.2 数据的存储与运算」；热身题为「零基础热身」 */",
 "  point: string",
 "  /** 考点编号前缀，如「1.2」；无考点时为空串 */",
 "  chapter: string",
 "  /** 单选 | 判断 */",
 "  kind: string",
 "  /** 来源年份或「热身」 */",
 "  year: string",
 "}",
 "",
 "export const questions: QuizQuestion[] = [",
]
for r in rows:
    L.append("  { q: %s, options: [%s], answer: %d, explain: %s, point: %s, chapter: %s, kind: %s, year: %s },"
             % (ts(r["q"]), ", ".join(ts(x) for x in r["options"]), r["answer"], ts(r["explain"]),
                ts(r["point"]), ts(r["chapter"]), ts(r["kind"]), ts(r["year"])))
L += ["]", "", "export const TOTAL = questions.length", ""]
OUT_TS.write_text("\n".join(L), encoding="utf-8")
print(f"\n→ {OUT_TS}")
print(f"   写入 {len(rows)} 题（热身 15 + 真题 {len(uniq)}）")
