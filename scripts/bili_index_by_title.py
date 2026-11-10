#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bili_index_by_title.py —— 从分P标题直接解析章节，生成「考点 → 哪一集」索引。

为什么优先用标题而不是模型
    2026-10-24 实测：政治 42 集用免费模型（Groq gpt-oss-120b）打标签，
    41/42 成功，但**准确率不足一半**。原因有两个，都是模型解决不了的：
      ① 毛中特与习概的章节编号撞车（都是 01–08），「01」到底指哪个说不清；
      ② 而分P标题里本来就写着「毛概第3章」「新中特6：推动高质量发展」。
    也就是说：**标题的信息量比模型从字幕里猜出来的更准**。
    所以对「标题有章节」的课，规则解析严格优于模型，且零成本、零限流。

    四科实测后连「英语」也不需要模型：英语标题虽无章节号，但写着
    「词汇 高频词第一课」「第16讲-名词性从句」「第一章 句子结构」，
    足以归到「模块」级（词汇 / 语法 / 阅读 / 完形 / 写作 / 真题）。
    结论：**本考试四科的网课索引全都不需要 LLM**，bili_tag_kaodian.py 仅留作备用。

为什么还要 per-BV 章号对照表（踩坑记录，别删）
    同一个「第三章」，在不同课里指的不是同一件事：
      · BV1X4411J792 是 7 章压缩版 → 它的 6 章才是「微分方程」
      · BV1swAWerEzS 的「第四章 碎知识」其实是点乘叉乘平面方程 = 考纲第 8 章
      · BV1Ye411Y7Ue 的「第三章」是数据类型，而 BV1ajMo6TEBm 的「第3章」是栈
      · BV1RwXvBpE7q 干脆 1–10 章全是 C 语言、11–12 章才进数据结构
    所以：**章号必须先过 per-BV 对照表，不能直接当考纲章号用。**
    对照表全部来自实际分P标题首集文字，不是猜的；查不到就退回关键词，再查不到就记「?」。

用法
    python scripts/bili_index_by_title.py --subject 政治
    python scripts/bili_index_by_title.py --subject 高数 --dry-run
    python scripts/bili_index_by_title.py --all

产出
    备考计划/网课考点索引-<学科>.md
"""
import argparse
import json
import pathlib
import re
import time

ROOT = pathlib.Path('D:/deeepseek/zhuan-sheng-ben-notes')
BILI = ROOT / 'data' / 'bili-analyze'

CN_NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
          '七': 7, '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12,
          '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17}

NAV = '—'   # 导读、资料、大纲：无考点
OUT = '×'   # 非考纲内容（Office / 线性代数 / 已删题型）
LOW = '低'   # 教材有、考纲没列（如预处理），优先级最低
FULL = '全'  # 整门课通讲，标题里没有任何章节信息
SKIP = ('?', NAV, OUT, LOW, FULL)

# 分P标题里的公众号广告词会被关键词误命中（「获取算法资料」→ 算法）
AD_RE = re.compile(r'【[^】]*(?:公众号|微信|QQ|群|资料)[^】]*】|'
                   r'【必听】|【考】|【重点】|【了解】')

CHAPTER_NAME = {
    '毛': {'00': '导论', '01': '毛泽东思想及其历史地位', '02': '新民主主义革命理论',
           '03': '社会主义改造理论', '04': '初步探索的理论成果', '05': '理论体系的形成发展',
           '06': '邓小平理论', '07': '三个代表重要思想', '08': '科学发展观'},
    '习': {'00': '导论', '01': '新时代坚持和发展中国特色社会主义', '02': '中国式现代化',
           '03': '坚持党的全面领导', '04': '坚持以人民为中心', '05': '全面深化改革开放',
           '06': '推动高质量发展', '07': '教育科技人才战略', '08': '全过程人民民主',
           '09': '全面依法治国', '10': '文化强国', '11': '民生与社会建设', '12': '生态文明',
           '13': '国家安全', '14': '国防和军队', '15': '一国两制与祖国统一',
           '16': '大国外交', '17': '全面从严治党'},
    # 与考纲原文《广东专升本考纲-2026-计算机类.md》§4.2 十二章逐字一致
    '高': {f'{i:02d}': n for i, n in enumerate(
        ['函数与极限', '导数与微分', '微分中值定理与导数的应用', '不定积分', '定积分',
         '定积分的应用', '微分方程', '向量代数与空间解析几何', '多元函数微分法及其应用',
         '重积分', '曲线积分与曲面积分', '无穷级数'], start=1)},
}

# 计算机 C1–C10 / D1–D8 —— 名称与《00-真题考点映射表-2021至2026.md》逐字一致
CS_NAME = {
    'C1': '程序设计与C语言基本概念', 'C2': '数据的存储与运算', 'C3': '顺序结构',
    'C4': '选择结构', 'C5': '循环结构', 'C6': '数组（含字符串处理）',
    'C7': '函数', 'C8': '指针', 'C9': '结构体', 'C10': '文件',
    # 考纲 §5.2 第十一项，本库笔记为零 —— 全网课里唯一覆盖它的是鹏哥课的调试 7 集
    'C11': '程序运行环境与代码调试',
    'D1': '数据结构基本概念/算法', 'D2': '线性表', 'D3': '栈和队列',
    'D4': '串、数组和广义表', 'D5': '树和二叉树', 'D6': '图',
    'D7': '查找', 'D8': '排序',
}

# ════════════════════════════════════════════════════════════
# 高数：per-BV 章号 → 考纲章号
#   依据：各课「第X章」首集的章名文字（见文件头「踩坑记录」）
# ════════════════════════════════════════════════════════════
MATH_CH = {
    # 7 章压缩版：1函数 2微分学 3积分学 4多元 5无穷级数 6常微分方程 7向量
    'BV1X4411J792': {1: 1, 2: 2, 3: 4, 4: 9, 5: 12, 6: 7, 7: 8},
    # 1函数 2导数 3不定积分 4向量 5二元函数 6二重积分 7曲线积分 8微分方程 9级数 10单调性
    'BV1husGzwEtZ': {1: 1, 2: 2, 3: 4, 4: 8, 5: 9, 6: 10, 7: 11, 8: 7, 9: 12, 10: 3},
    # 1函数 2导数 3积分 4「碎知识」=点乘叉乘平面方程(实为第8章) 5多元 6微分方程 7无穷级数
    'BV1swAWerEzS': {1: 1, 2: 2, 3: 4, 4: 8, 5: 9, 6: 7, 7: 12},
    # 广东口径 11 章：1函数 2导数 3罗尔/中值 4不定积分 5定积分 6微分方程 7向量 8二元 9二重 10曲线 11级数
    'BV1vm421s7mv': {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12},
    # 1函数 2导数 3不定积分 4向量 5二元函数 6二重积分 7微分方程 8级数
    'BV18CL26WEJ3': {1: 1, 2: 2, 3: 4, 4: 8, 5: 9, 6: 10, 7: 7, 8: 12},
    # 1函数 2导数(含中值/极值/罗尔/拉格朗日) 3积分(不定+定+应用)
    'BV1SnYF6eEcC': {1: 1, 2: 2, 3: 4},
    # 1函数 2导数 3不定积分 4向量 5二重积分(原第五章提前) 6微分方程 7无穷级数
    'BV1Up4y1Y76a': {1: 1, 2: 2, 3: 4, 4: 8, 5: 10, 6: 7, 7: 12},
}

# 高数里出现但考纲没有的内容
MATH_OUT = ['行列式', '线性代数', '逆矩阵', '向量空间', '矩阵概念', '矩阵性质',
            '初等变换', '矩阵公式', '方程组1', '方程组2', '方程组3']


# ════════════════════════════════════════════════════════════
# 计算机：per-BV 章号 → C/D 编号（只给确实需要的 4 个课建表）
# ════════════════════════════════════════════════════════════
CS_CH = {
    # C 语言课，1–7 章：1C语言 2算法 3数据类型 4顺序 5选择 6循环 7数组
    'BV1Ye411Y7Ue': {1: 'C1', 2: 'D1', 3: 'C2', 4: 'C3', 5: 'C4', 6: 'C5', 7: 'C6'},
    # 广东精讲课：1–10 章 C 语言，11 数据结构基本概念，12 线性表
    'BV1RwXvBpE7q': {1: 'C1', 2: 'C2', 11: 'D1', 12: 'D2'},
    # 严蔚敏数据结构（华科大）：1绪论 2线性表 3栈 4串 5数组 6树 7图 9查找 10排序
    #   第8章「动态存储管理」考纲没有，故意不入表 → 落到继承
    'BV11T411q7Qw': {1: 'D1', 2: 'D2', 3: 'D3', 4: 'D4', 5: 'D4',
                     6: 'D5', 7: 'D6', 9: 'D7', 10: 'D8'},
    # 数据结构教程：1绪论 2线性表 3栈 4串 5数组 6树 7图 8查找 9排序
    'BV1ajMo6TEBm': {1: 'D1', 2: 'D2', 3: 'D3', 4: 'D4', 5: 'D4',
                     6: 'D5', 7: 'D6', 8: 'D7', 9: 'D8'},
}

# 按「周」组织的课（浙大翁恺 MOOC：标题前缀 N.M.K 的 N 是第 N 周，不是第 N 章）
CS_WEEK = {
    'BV1dr4y1n7vA': {1: 'C1', 2: 'C2', 3: 'C4', 4: 'C5', 5: 'C5', 6: 'C2',
                     7: 'C7', 8: 'C6', 9: 'C8', 10: 'C6', 11: 'C9', 12: 'C1', 13: 'C10'},
}

# 关键词 → 考纲编号。顺序即优先级，越具体的越靠前（改之前先看文件头踩坑记录）
CS_KP = [
    ('C11', ['调试', 'VS实用', 'VS实⽤', 'bug', '编程常⻅错误', '编程常见错误']),
    ('C3', ['printf', 'scanf', 'putchar', 'getchar', '格式控制', '输入输出']),
    ('C9', ['共用体', '联合', 'union', '共同体', '枚举']),
    ('D6', ['邻接', '深度优先', '广度优先', '最小生成树', '最短路径', '拓扑排序',
            '关键路径', '普里姆', '克鲁斯卡尔', '迪杰斯特拉', 'DFS', 'BFS',
            '连通', '图的基本', '图基本概念', '图的']),
    ('D7', ['查找', '折半', '二分', '二叉排序树', '平衡二叉树', 'B树', 'B+树', '散列', '哈希']),
    ('D8', ['排序', '冒泡', '希尔', '归并', '基数排序', '快速排序']),
    ('D5', ['二叉树', '哈夫曼', '树森林', '线索', '遍历', '树']),
    ('D4', ['串的', '串(', '串（', '串习题', '广义表', '压缩存储', '对称矩阵',
            '三角矩阵', '稀疏矩阵', '矩阵']),
    ('D3', ['栈', '队列', '表达式求值', '汉诺塔', '迷宫']),
    ('D2', ['线性表', '顺序表', '链表', '头结点', '头指针']),
    ('D1', ['数据结构', '抽象数据类型', '时间复杂度', '空间复杂度', '复杂度',
            '5大特性', '五大特性', '数据元素', '数据项', '数据对象', '三要素', '绪论', '算法']),
    ('C10', ['文件']),
    ('C9', ['结构体']),
    ('C8', ['指针', '动态内存', 'malloc']),
    ('C7', ['函数', '形参', '实参', '作用域', '存储类别', '递归']),
    ('C6', ['数组', '字符串', '字符数组']),
    ('C5', ['循环', 'while', 'for', 'do-while', 'break', 'continue']),
    ('C4', ['选择结构', 'if', 'switch', '关系运算', '逻辑运算', '条件表达式',
            '按位', '位运算', '多分支']),
    ('C3', ['顺序结构', '顺序程序', '赋值语句', '控制语句']),
    ('C2', ['数据类型', '常量', '变量', '进制', '运算符', '操作符', '表达式',
            '类型转换', '整型', '整形', '实型', '浮点', '字符型', '标识符',
            '溢出', '内存', '大小端', '补码', 'ASCII', 'ASCll']),
    ('C1', ['C语言', 'C程序', 'main', '注释', '头文件', '编译', '源文件',
            '关键字', '第一个程序', '转义字符', '编程语言', '计算机']),
]

# 广东计算机类考纲 §5.2 只列 21 项（C 语言 1–11 + 数据结构 12–21），
# 不含 Office / Windows / 计算机网络 / 计算机组成 —— 这些课在本考试里是纯噪音
CS_OUT = ['选项卡', 'WORD', 'Word', 'Excel', 'Excle', 'PPT', 'windows',
          'Windows', '控制面板', '虚拟机', '资源管理器', 'office',
          '计算机的诞生', '计算机的分类', '信息安全', '计算机系统组成',
          '计算机工作原理', '计算机硬件', '总线', 'IO接口', '性能指标',
          '软件系统', '多媒体', '网络', 'IP地址', 'DNS', '体系结构',
          '信息的单位', '数值的表示', '信息编码',
          '窗口', '开始菜单', '单元格', '幻灯片', 'Internet',
          'ACLLib', 'Win32API']

# 教材有、考纲十一项没列 —— 不算噪音，但优先级最低
CS_LOW = ['预处理', '#define', '宏替换', '条件编译', '命名约定', '预定义符号',
          '命令行定义', '带副作用']

EN_KP = [
    ('语法填空', ['语法填空']),
    ('选句填空', ['造句', '匹配', '七选五']),
    ('阅读', ['阅读', '篇章']),
    ('完形', ['完形', '完型']),
    ('写作', ['写作', '作文', '范文']),
    ('语法', ['语法', '从句', '时态', '语态', '非谓语', '主谓一致', '句子结构',
              '词性', '名词', '冠词', '代词', '形容词', '副词', '介词', '连词',
              '句型', '成分', '虚拟语气', '情态动词']),
    ('词汇', ['词汇', '单词', '高频词']),
]

# 广东公共英语考纲题型只有：阅读 / 短文造句匹配 / 完形 / 语法填空 / 写作
EN_OUT = ['改错', '选词填空']


def _ch_num(s):
    """从文字里抓「第X章」的 X（支持中文数字与阿拉伯数字）"""
    m = re.search(r'第\s*([一二三四五六七八九十]{1,3}|\d{1,2})\s*章', s)
    if not m:
        return None
    raw = m.group(1)
    return int(raw) if raw.isdigit() else CN_NUM.get(raw)


# ════════════════════════════════════════════════════════════
# 政治
# ════════════════════════════════════════════════════════════
def parse_politics(part, bv_title='', ctx=None):
    s = part.replace('《', '').replace('》', '').replace(' ', '')

    m = re.search(r'单选题|多选题|辨析题|简答题|论述题|材料分析', s)
    if m:
        return (f'题·{m.group(0)}', m.group(0))
    if re.search(r'真题', s):
        return ('题·真题', '真题解析')
    if re.search(r'导学|导读|必听|大纲|押题', s):
        return (NAV, '导读/资料')

    m = re.search(r'(?:新中特|新思想|习概)(\d{1,2}|[一二三四五六七八九十]{1,3})', s)
    if m:
        raw = m.group(1)
        n = int(raw) if raw.isdigit() else CN_NUM.get(raw, 0)
        if 0 <= n <= 17:
            return (f'习{n:02d}', CHAPTER_NAME['习'].get(f'{n:02d}', ''))
    if re.search(r'新中特|新思想|习概', s) and '导论' in s:
        return ('习00', '导论')

    m = re.search(r'毛概(?:第)?(\d|导论|[一二三四五六七八九十]{1,2})', s)
    if m:
        raw = m.group(1)
        if raw == '导论':
            return ('毛00', '导论')
        n = int(raw) if raw.isdigit() else CN_NUM.get(raw, 0)
        if 0 <= n <= 8:
            return (f'毛{n:02d}', CHAPTER_NAME['毛'].get(f'{n:02d}', ''))
    if re.search(r'毛概', s) and '导论' in s:
        return ('毛00', '导论')

    return ('?', '')


# ════════════════════════════════════════════════════════════
# 高数：章号过 per-BV 对照表，后续集继承当前章
# ════════════════════════════════════════════════════════════
def parse_math(part, bv_title='', ctx=None):
    ctx = ctx if ctx is not None else {}

    if any(k in part for k in MATH_OUT):
        return (OUT, '线性代数·考纲无此章')

    n = _ch_num(part)
    if n is not None:
        official = MATH_CH.get(ctx.get('bv'), {}).get(n)
        if official:
            ctx['ch'] = (f'高{official:02d}', CHAPTER_NAME['高'][f'{official:02d}'])
            return ctx['ch']
        # 章号不在对照表里（多半是超纲章），退回继承
        ctx['ch'] = None

    if ctx.get('ch'):
        return ctx['ch']

    if re.search(r'导学|考情|讲义|真题|规划|为什么|宣导|概要|开篇|欢迎进入', part):
        return (NAV, '导学/资料')
    return ('?', '')


# ════════════════════════════════════════════════════════════
# 计算机：章号过 per-BV 对照表 → 关键词 → 继承
# ════════════════════════════════════════════════════════════
def parse_cs(part, bv_title='', ctx=None):
    ctx = ctx if ctx is not None else {}
    part = AD_RE.sub('', part)   # 再洗一遍，防止调用方没洗

    if re.search(r'真题|押题|模拟卷', part):
        return ('题·真题', '真题解析')
    if re.search(r'导读|导学|大纲|简介|必听|开课|环境准备|讲在最后|补充说明'
                 r'|课程讲解范围|欢迎进入|开篇|概述|PAT|复习要点|寄语', part):
        return (NAV, '导读/资料')
    # 考纲第十一项：程序运行环境与代码调试 —— 必须排在「预处理」之前判
    if re.search(r'翻译环境|运行环境|编译和链接|调试', part):
        return ('C11', CS_NAME['C11'])
    if any(k in part for k in CS_OUT):
        return (OUT, 'Office/网络/组成·非考纲')
    if any(k in part for k in CS_LOW):
        return (LOW, '预处理·考纲十一项未列')
    # 「【严蔚敏本人讲解】数据结构07」这类只有序号、没有章节的通讲
    if re.fullmatch(r'.*数据结构\s*\d{1,3}\s*', part) and _ch_num(part) is None:
        return (FULL, '全片通讲·无章节')
    # 这三个词同时是 C1 与 C10/C7 的诱饵，必须先判
    if re.search(r'头文件|源文件|源程序|注释|main|入口', part):
        return ('C1', CS_NAME['C1'])

    n = _ch_num(part)
    if n is not None:
        code = CS_CH.get(ctx.get('bv'), {}).get(n)
        if code:
            ctx['ch'] = (code, CS_NAME[code])
            return ctx['ch']

    # 「周」组织的课：N.M.K 前缀的 N 是第 N 周
    wk = CS_WEEK.get(ctx.get('bv'))
    if wk:
        m = re.match(r'^\s*(\d{1,2})\.\d', part)
        if m and int(m.group(1)) in wk:
            code = wk[int(m.group(1))]
            return (code, CS_NAME[code])

    # 关键词（去掉「N.数据结构课程-」这类 BV 名前缀，避免误命中「数据结构」）
    s = re.sub(r'\d+\.\s*数据结构课程[-－]?', '', part)
    for code, kws in CS_KP:
        for kw in kws:
            if kw in s:
                return (code, CS_NAME[code])

    if ctx.get('ch'):
        return ctx['ch']
    return ('?', '')


# ════════════════════════════════════════════════════════════
# 英语：只归到模块级，不假装能归到 E1–E18
# ════════════════════════════════════════════════════════════
def parse_english(part, bv_title='', ctx=None):
    s = part + ' ' + bv_title
    if not part.strip():
        return (NAV, '无标题')
    if re.search(r'真题', s):
        return ('题·真题', '真题解析')
    if re.search(r'导学|规划|介绍|导入|大家好|评论区', part):
        return (NAV, '导学/资料')
    if re.search(r'翻译', s):
        return (OUT, '翻译·已删不考')
    if any(k in part for k in EN_OUT):
        return (OUT, '考纲无此题型')
    for mod, kws in EN_KP:
        for kw in kws:
            if kw in part:
                return (f'英·{mod}', f'{mod}模块')
    return ('?', '')


PARSERS = {'政治': parse_politics, '高数': parse_math,
           '计算机': parse_cs, '英语': parse_english}

# 考纲全量考点清单 —— 用来算「哪些考点一集网课都没有」
ALL_CODES = {
    '政治': [f'毛{i:02d}' for i in range(9)] + [f'习{i:02d}' for i in range(18)],
    '高数': [f'高{i:02d}' for i in range(1, 13)],
    '计算机': [f'C{i}' for i in range(1, 12)] + [f'D{i}' for i in range(1, 9)],
    '英语': ['英·词汇', '英·语法', '英·语法填空', '英·选句填空',
             '英·阅读', '英·完形', '英·写作'],
}


# 缺口核查用的内容关键词 —— 只用来回答「这个考点到底有没有课」，
# 不参与归章。有些考点没有独立章节（高06 定积分的应用就是这样，
# 20 多集全挂在「第三章/第五章/第六章」下面），只看章号会误报「零网课」。
TOPIC_HINT = {
    ('高数', '高06'): ['定积分的应用', '旋转体', '平面图形', '求面积', '求体积', '弧长'],
    ('高数', '高03'): ['中值定理', '罗尔', '拉格朗日', '洛必达', '单调性', '极值', '凹凸'],
    ('英语', '英·选句填空'): ['造句', '选句', '匹配', '七选五'],
    ('英语', '英·语法填空'): ['语法填空'],
}


def code_name(subject, code):
    if subject == '政治':
        return CHAPTER_NAME[code[0]].get(code[1:], '')
    if subject == '高数':
        return CHAPTER_NAME['高'].get(code[1:], '')
    if subject == '计算机':
        return CS_NAME.get(code, '')
    return code.replace('英·', '') + '模块'

# 反查排序：政治/高数按章号，计算机按考纲顺序
def sort_key(code):
    if code.startswith('毛'):
        return (0, 0, code)
    if code.startswith('习'):
        return (0, 1, code)
    if code.startswith('高'):
        return (0, 0, code)
    if code.startswith('题'):
        return (3, 0, code)
    m = re.match(r'C(\d+)$', code)
    if m:
        return (1, int(m.group(1)), '')
    m = re.match(r'D(\d+)$', code)
    if m:
        return (2, int(m.group(1)), '')
    return (3, 0, code)


def build(subject):
    """返回 (rows, nosub)。

    rows   —— 有字幕的集（索引正文用）
    nosub  —— 有分P标题但没有字幕的集。**必须单独算**：
              否则会把「有课但下不到字幕」误报成「零网课」，
              2026-10-24 就在这里错过一次（毛05/毛06/习03 其实都有课）。
    """
    smap = json.loads((BILI / '_subject-map.json').read_text(encoding='utf-8'))
    ptitles = json.loads((BILI / '_part_titles_all.json').read_text(encoding='utf-8'))
    parser = PARSERS[subject]

    rows, nosub = [], []
    for bv, subj in smap.items():
        if subj != subject:
            continue
        d = BILI / bv
        if not d.is_dir():
            continue
        info = ptitles.get(bv, {})
        title = info.get('title', bv)
        pages = {p['p']: p.get('part', '') for p in info.get('pages', [])}

        have = set()
        for f in d.glob('subtitle_p*.txt'):
            m = re.search(r'p(\d+)', f.name)
            if m:
                have.add(int(m.group(1)))
        # 分P表里有的全走一遍（含没字幕的），保证 ctx 章号状态连贯
        order = sorted(set(pages) | have)

        # 整门课都没有「第X章」时，才允许用 BV 标题里的章号兜底
        bv_ch = _ch_num(title)
        has_any_ch = any(_ch_num(t) is not None for t in pages.values())

        ctx = {'bv': bv}
        if bv_ch and not has_any_ch:
            official = MATH_CH.get(bv, {}).get(bv_ch) or (bv_ch if subject == '高数' else None)
            if official:
                ctx['ch'] = (f'高{official:02d}', CHAPTER_NAME['高'].get(f'{official:02d}', ''))

        for p in order:
            part = AD_RE.sub('', pages.get(p, ''))
            code, name = parser(part, title, ctx)
            rec = {'bv': bv, 'p': p, 'title': title,
                   'part': part, 'code': code, 'name': name}
            (rows if p in have else nosub).append(rec)
    return rows, nosub


def write(subject, rows, nosub=()):
    cnt = lambda c: sum(1 for r in rows if r['code'] == c)
    hit = sum(1 for r in rows if r['code'] not in SKIP)
    nav, out, unk, full = cnt(NAV), cnt(OUT), cnt('?'), cnt(FULL)

    print(f'[{subject}] {len(rows)} 集 | 归章 {hit} · 导读 {nav} · 非考纲 {out} '
          f'· 考纲外 {cnt(LOW)} · 通讲 {full} · 未识别 {unk}')
    for r in rows:
        if r['code'] == '?':
            print(f'    ? {r["bv"]} P{r["p"]} {r["part"][:46]}')

    path = ROOT / '备考计划' / f'网课考点索引-{subject}.md'
    L = [
        f'# 📺 网课考点索引 · {subject}',
        '',
        f'> 生成：{time.strftime("%Y-%m-%d %H:%M")}　｜　**来源：分P标题规则解析**（非模型推断）',
        f'> 覆盖：**{len(rows)} 集**　｜　归到考点 {hit} 集 · 导读/资料 {nav} 集 · '
        f'非考纲 {out} 集 · 考纲外 {cnt(LOW)} 集 · 通讲无章节 {full} 集 · 未识别 {unk} 集',
        '> ⚠️ 字幕无时间戳，**只能定位到「集」，不能到「第几分钟」**。',
        '> ✅ 不用 AI 猜 —— 分P标题里已写明章节，规则解析比模型更准（见脚本 docstring）。',
        '> ⚠️ 章号已按**各课自己的章表**折算成考纲章号（同名「第三章」在不同课里不是同一件事），'
        '折算表见脚本 `MATH_CH` / `CS_CH`。',
        '> ⚠️ 一集跨多章时只记第一个命中，**只作导航用**。',
        '> 标记：`×` = 考纲没有的内容（不必看）　`低` = 教材有但考纲没列（预处理等，最后再看）'
        '　`—` = 导读/资料　`全` = 整门课通讲，无章节可拆',
        '',
        '---',
        '',
        '## 按 BV 排列（看课时用）',
        '',
    ]
    by_bv = {}
    for r in rows:
        by_bv.setdefault(r['bv'], []).append(r)
    for bv in sorted(by_bv):
        rs = sorted(by_bv[bv], key=lambda x: x['p'])
        L.append(f'### `{bv}` {rs[0]["title"][:60]}')
        L.append('')
        L.append('| 集 | 分P标题 | 考点 | 考点名 |')
        L.append('|:--:|:--|:--:|:--|')
        for r in rs:
            code = r['code']
            if code == NAV:
                kp = '—'
            elif code == OUT:
                kp = '×'
            elif code == FULL:
                kp = '全'
            elif code == LOW:
                kp = '低'
            elif code == '?':
                kp = '?'
            else:
                kp = f'**{code}**'
            nm = r['name'] or ('—' if code in (NAV, OUT, LOW) else '')
            L.append(f'| P{r["p"]} | {r["part"][:34]} | {kp} | {nm} |')
        L.append('')

    L += ['---', '', '## 按考点反查（卡住时用）', '',
          '| 考点 | 考点名 | 集数 | 在哪些集 |', '|:--:|:--|--:|:--|']
    by_kp = {}
    for r in rows:
        if r['code'] in SKIP:
            continue
        by_kp.setdefault(r['code'], []).append(r)
    for code in sorted(by_kp, key=lambda c: sort_key(c)):
        rs = by_kp[code]
        nm = rs[0]['name']
        locs = [f'{r["bv"][-4:]}P{r["p"]}'
                for r in sorted(rs, key=lambda x: (x['bv'], x['p']))]
        shown = '、'.join(locs[:12]) + (f' …等 {len(locs)} 集' if len(locs) > 12 else '')
        L.append(f'| **{code}** | {nm} | {len(rs)} | {shown} |')
    L.append('')
    L.append('> 集数后的编号是 BV 号后 4 位 + 分P序号，如 `Y7UeP5` = `BV1Ye411Y7Ue` 第 5 集。')
    L.append('')

    # ── 缺口：区分「真的没课」和「有课但没字幕」──
    allc = ALL_CODES.get(subject, [])
    nosub_kp = {}
    for r in nosub:
        if r['code'] not in SKIP:
            nosub_kp.setdefault(r['code'], []).append(r)
    miss = [c for c in allc if c not in by_kp and c not in nosub_kp]
    only_nosub = [c for c in allc if c not in by_kp and c in nosub_kp]
    thin = [(c, len(by_kp[c])) for c in allc if c in by_kp and len(by_kp[c]) <= 2]

    # 对「按章号判为缺失」的考点，再按内容关键词扫一遍标题
    pool = rows + list(nosub)
    def topic_hits(c):
        kws = TOPIC_HINT.get((subject, c)) or [code_name(subject, c)]
        out = []
        for r in pool:
            if r['code'] == c:
                continue
            if any(k and k in r['part'] for k in kws):
                out.append(r)
        return out

    scattered, really_miss = {}, []
    for c in miss:
        h = topic_hits(c)
        if h:
            scattered[c] = h
        else:
            really_miss.append(c)

    L += ['---', '', '## 网课缺口', '']
    if only_nosub:
        L.append('### ⚠️ 有课，但下不到字幕（能看视频，索引里取不到文字）')
        L.append('')
        L.append('| 考点 | 考点名 | 无字幕集数 | 在哪 |')
        L.append('|:--:|:--|--:|:--|')
        for c in only_nosub:
            rs = nosub_kp[c]
            L.append(f'| **{c}** | {code_name(subject, c)} | {len(rs)} | '
                     + '、'.join(f'{r["bv"][-4:]}P{r["p"]}' for r in rs[:10])
                     + ('…' if len(rs) > 10 else '') + ' |')
        L.append('')
    if scattered:
        L.append('### ⚠️ 没有独立章节，内容散在别章（要按标题自己挑）')
        L.append('')
        L.append('| 考点 | 考点名 | 相关集数 | 在哪 |')
        L.append('|:--:|:--|--:|:--|')
        for c, h in scattered.items():
            L.append(f'| **{c}** | {code_name(subject, c)} | {len(h)} | '
                     + '、'.join(f'{r["bv"][-4:]}P{r["p"]}' for r in h[:10])
                     + ('…' if len(h) > 10 else '') + ' |')
        L.append('')
    if really_miss:
        L.append('### ❌ 真的没有课（标题里连关键词都搜不到，只能靠笔记/教材）')
        L.append('')
        L.append('| 考点 | 考点名 | 状态 |')
        L.append('|:--:|:--|:--|')
        for c in really_miss:
            L.append(f'| **{c}** | {code_name(subject, c)} | ❌ 零网课 |')
        L.append('')
    if not really_miss and not only_nosub and not scattered:
        L.append('考纲全部考点都有带字幕的网课覆盖。')
        L.append('')
    if thin:
        head = '、'.join(f'**{c}** {code_name(subject, c)}（{n} 集）' for c, n in thin[:8])
        tail = f'　…另有 {len(thin)-8} 个' if len(thin) > 8 else ''
        L.append(f'**覆盖极薄（有字幕的 ≤2 集，共 {len(thin)} 个考点）**：{head}{tail}')
        L.append('')

    path.write_text('\n'.join(L) + '\n', encoding='utf-8')
    print(f'    ✅ {path.relative_to(ROOT)}')
    return hit, unk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--subject', choices=list(PARSERS))
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if not a.subject and not a.all:
        ap.error('需要 --subject 或 --all')

    subs = list(PARSERS) if a.all else [a.subject]
    for s in subs:
        rows, nosub = build(s)
        if a.dry_run:
            cnt = lambda c: sum(1 for r in rows if r['code'] == c)
            hit = sum(1 for r in rows if r['code'] not in SKIP)
            print(f'[{s}] {len(rows)} 集 | 归章 {hit} · 导读 {cnt(NAV)} · '
                  f'非考纲 {cnt(OUT)} · 考纲外 {cnt(LOW)} · 通讲 {cnt(FULL)} '
                  f'· 未识别 {cnt("?")}')
            for r in rows:
                if r['code'] == '?':
                    print(f'    ? {r["bv"]} P{r["p"]} {r["part"][:46]}')
        else:
            write(s, rows, nosub)
        print()


if __name__ == '__main__':
    main()
