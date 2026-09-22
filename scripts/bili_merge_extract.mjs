#!/usr/bin/env node
/**
 * bili_merge_extract.mjs —— 把 data/bili-analyze/_extract/*.md 跨视频合并成考点库
 *
 * 为什么需要它：_extract/ 是**按单元（视频×分P 区间）**切的产出，60+ 份，各自独立。
 * 想知道「某个考点被几支视频讲过」「哪个考纲模块没人讲」，靠人翻是翻不出来的。
 *
 * 用法：
 *   node scripts/bili_merge_extract.mjs                    # 输出汇总到 stdout
 *   node scripts/bili_merge_extract.mjs --json <path>      # 额外写机器可读 JSON（全量，~1MB）
 *   node scripts/bili_merge_extract.mjs --md <path>        # 额外写人读的合并报告
 *   node scripts/bili_merge_extract.mjs --coverage <path>  # 额外写**精简**覆盖度 JSON（供 Studio 读，数十 KB）
 *
 * `--coverage` 是给 Studio（D:/studio）用的：
 *   它把「视频讲了多少」和「真题考了多少」并排放到**同一张模块表**里，
 *   是 `_merged.json`（1MB，全量）的**降采样**，只保留模块级聚合 + 视频分层 + 快照新鲜度。
 *   Studio 绝不能整份发 _merged.json —— 1MB 每请求发一次会把端口打满。
 *
 * 口径（重要，别把估算当精确值）：
 *   - 「知识点」= 产出里的一个 `###` 小节。同一知识点被多支视频分别讲，会算多条。
 *   - 「跨视频重复」= 同一 `###` 标题出现在 ≥2 支视频 → 多源印证，可信度更高。
 *   - 考纲模块归属靠**关键词规则**，一个主题可能同时命中多个模块（会全部列出）。
 *     规则可错，命中不到任何模块的会归入「未归位」，**不要把未归位读成超纲**。
 */

import fs from 'node:fs';
import path from 'node:path';

const EXTRACT_DIR = 'data/bili-analyze/_extract';
const ANALYZE_DIR = 'data/bili-analyze';

// ── 快照状态：_extract 可能仍在被写入，报告是移动靶 ──
/* 数一数某个视频目录里 _verify*.jsonl 有多少段判为 ok:true。
   校验器（bili_reverify_probe.py 那一套）负责判断「这段字幕到底是不是专升本内容」，
   它的结论是提取步骤的唯一准入条件 —— 提取只做 ok:true 的段。
   于是「ok:true > 0」就是「这支视频值得提取」的准确判据。 */
function verifiedSegments(bv) {
  let n = 0;
  for (const name of ['_verify.jsonl', '_verify2.jsonl']) {
    const p = path.join(ANALYZE_DIR, bv, name);
    let text;
    try { text = fs.readFileSync(p, 'utf8'); } catch { continue; }
    for (const line of text.split('\n')) {
      if (!line.trim()) continue;
      try { if (JSON.parse(line).ok === true) n++; } catch { /* 半行/坏行忽略 */ }
    }
  }
  return n;
}

function snapshotState() {
  const allBv = fs.existsSync(ANALYZE_DIR)
    ? fs.readdirSync(ANALYZE_DIR).filter(d => /^BV/.test(d) && fs.statSync(path.join(ANALYZE_DIR, d)).isDirectory())
    : [];
  const doneBv = new Set(files.map(f => (f.match(/^(BV[0-9A-Za-z]+)/) || [])[1]).filter(Boolean));

  /* ⚠️ 分母不能用 allBv.length。
     2026-09-19 实查：24 个目录里有 6 个**每一段都是 ok:false** ——
     BV176gY6nEb3(蚂蝗纪录片) / BV1gh9MBkEEC(音乐视频) / BV1PRM26hEbk(漫威票房解说) /
     BV1TDj36dEdc(VIVO 手机测评) / BV1xzBCBFExz(电影解说) / BV1rg411h7Z1(惠普笔记本维修合集)。
     它们是被抓错的垃圾，校验器早已拒绝，提取步骤正确地跳过了它们。
     把它们算进分母会凭空造出「还差 6 支、提取没跑完」的假缺口，
     让人对着一个不存在的缺口干活（甚至去提取蚂蝗纪录片的知识点）。
     所以分母 = 至少有一段 ok:true 的视频数；被拒的单独列出来，是**结论**不是待办。 */
  const verifiedBv = [];
  const rejectedBv = [];
  for (const d of allBv) {
    (verifiedSegments(d) > 0 ? verifiedBv : rejectedBv).push(d);
  }

  // 最后写入时间（判断是否还在跑）
  let latest = 0, latestFile = '';
  for (const f of files) {
    const m = fs.statSync(path.join(EXTRACT_DIR, f)).mtimeMs;
    if (m > latest) { latest = m; latestFile = f; }
  }
  return { allBv, verifiedBv, rejectedBv, doneBv, latest, latestFile, staleMs: Date.now() - latest };
}

// ── 官方考纲模块（来源：docs/guide/2026考纲全解.md，已对考试院原文核实）──
const COMPUTER_MODULES = {
  '①程序设计与C语言的基本概念': ['概述', '程序构成', '程序结构', '程序入口', '第一个C程序', '关键字', '语句与注释', '算法及其特性', '算法入门', 'C语言与', '语言与开发环境', 'C程序'],
  '②数据的存储与运算': ['数据类型', '常量', '变量', '运算符', '操作符', '表达式', '进制', '二进制', '移位', '位运算', '位操作', '字符与编码', '数值与进制', '数据表现形式'],
  '③顺序程序设计': ['顺序', '输入输出', 'printf', 'scanf', '格式化', '库函数', '字符输入输出', '数据在内存中的存储'],
  '④选择结构程序设计': ['if 语句', 'switch', '选择结构', '关系运算', '逻辑运算', '逻辑操作符', '条件运算符', '条件操作符', '分支语句', 'goto'],
  '⑤循环结构程序设计': ['循环', 'for 循环', 'while', 'do-while', 'break', 'continue', '嵌套'],
  '⑥数组': ['一维数组', '二维数组', '变长数组', '数组应用', '数组名', '字符串与字符数组', 'strcpy', 'strcat', 'strcmp', 'strstr', 'strtok', 'strlen', '字符分类'],
  '⑦函数': ['函数基础', '函数递归', '函数调用', '函数声明', '函数的参数', '函数参数', '数组做函数参数', '回调函数', 'qsort', '递归', '作用域', '生命周期', 'static'],
  '⑧指针': ['指针', '地址', '内存与地址', '野指针', '数组传参', '数组降级', 'const 与指针', '动态内存', '柔性数组'],
  '⑨结构体': ['结构体', '共用体', '联合体', '枚举', '位段', 'typedef'],
  '⑩文件': ['文件操作', '文件顺序读写', '文件随机读写', '文件缓冲区'],
  '⑪运行环境与代码调试': ['调试', 'debug', 'release', '预处理', '宏', '条件编译', '头文件', '命令行定义', '内存区域划分', '常见错误', '编译和链接', '程序内存'],
  '⑫数据结构基本概念': ['数据结构', '绪论', '三要素', '逻辑结构', '存储结构'],
  '⑬线性表': ['线性表', '链表', '单链表', '双向链表', '循环链表', '顺序表'],
  '⑭栈和队列': ['栈', '队列'],
  '⑮串、数组和广义表': ['串', 'KMP', '广义表', '数组与矩阵', '稀疏矩阵'],
  '⑯树和二叉树': ['树', '二叉树', '遍历', '线索二叉树', '哈夫曼', '森林'],
  '⑰图': ['图的基本概念', '图的存储', '图的遍历', '邻接', '最小生成树', '最短路径', '拓扑', '关键路径', 'DFS', 'BFS'],
  '⑱查找': ['查找', '折半', '判定树', '二叉排序树', '平衡二叉树', 'AVL', '散列表', '哈希'],
  '⑲排序': ['排序', '堆', '归并', '冒泡', '快速排序', '外部排序', '插入排序', '选择排序'],
  '⑳算法的基本概念': ['算法及其特性', '算法入门', '算法与程序', '算法的基本概念', '数据结构与算法总览'],
  '㉑算法分析初步': ['复杂度', '算法分析'],
};

// ── 疑似超纲：计算机基础（已核实 2026 官方 21 模块里没有）──
// 核实来源：https://www.zjielts.com/newsinfo/8905126.html （考试院原文转载，2026-01-05）
//   (一)~(二十一) 全部是 C 语言 + 数据结构，无硬件/OS/Office/网络/多媒体/信息安全。
// ⚠️ 只匹配「主题名」，不匹配知识点名 —— 否则 Word 里的「查找」「排序」会误命中 ⑱查找 / ⑲排序。
const OFF_SYLLABUS = ['计算机发展史', '计算机的分类', '计算机的特点', '信息安全', '病毒', '数据单位', '信息编码',
  '计算机系统组成', '计算机硬件', '外存储器', '输入输出设备', '总线', 'IO 接口', '性能指标', '计算机软件系统',
  '多媒体', '操作系统', 'Windows', 'Word', 'Excel', 'PowerPoint', '计算机网络', '网络基础', '网络体系',
  'Internet', 'IP 地址', '域名', 'URL', 'IPv6', '网络安全', '计算机的分类',
  // Office 子主题（不含这些会让「单元格/工作表/选项卡」类主题漏判）
  '单元格', '工作表', '选项卡', '幻灯片', '资源管理器', '控制面板', '开始菜单', '公式复制'];

// 泛化小节名 —— 这些名字本身不携带知识，出现在「跨视频重复」表里是噪声
const GENERIC_NAMES = new Set(['解题步骤', '易错点', '常见题型', '小结', '概述', '定义', '基本概念', '总结',
  '例题', '题型', '注意事项', '解题套路', '计算步骤', '解题思路']);

// ── 高数官方 12 章（来源：备考计划/考纲核实-高数12模块-2026-09-17.md）──
const MATH_MODULES = {
  '一、函数与极限': ['函数', '极限', '无穷小', '无穷大', '连续', '间断', '数列'],
  '二、导数与微分': ['导数', '微分', '求导', '高阶导数', '隐函数', '参数方程'],
  '三、微分中值定理与导数的应用': ['中值定理', '洛必达', '单调', '极值', '最值', '凹凸', '拐点', '渐近线', '曲率', '罗尔', '拉格朗日', '柯西'],
  '四、不定积分': ['不定积分', '原函数', '换元积分', '分部积分', '有理函数'],
  '五、定积分': ['定积分', '牛顿', '莱布尼茨', '变限积分', '反常积分', '广义积分'],
  '六、定积分的应用': ['面积', '体积', '旋转体', '弧长', '平均值'],
  '七、微分方程': ['微分方程', '通解', '特解', '可降阶', '常系数'],
  '八、向量代数与空间解析几何': ['向量', '平面方程', '直线方程', '空间', '数量积', '向量积', '曲面'],
  '九、多元函数微分法及其应用': ['偏导', '全微分', '多元函数', '方向导数'],
  '十、重积分': ['二重积分', '三重积分', '极坐标'],
  '十一、曲线积分与曲面积分': ['曲线积分', '曲面积分', '格林', '高斯', '斯托克斯'],
  '十二、无穷级数': ['级数', '收敛', '发散', '幂级数', '傅里叶', '泰勒'],
};

// ── 英语：按题型（考纲未列模块，按用途分类）──
const ENGLISH_MODULES = {
  '语法填空': ['题型框架', '有提示词', '无提示词'],
  '语法体系': ['句型', '谓语', '时态', '语态', '被动', '情态', '否定与疑问', '句子主干'],
  '词法': ['形容词', '副词', '名词', '代词', '冠词', '介词'],
  '阅读/写作': ['阅读', '写作', '完形', '翻译'],
};

// ══════════════════════════════════════════════════════════════════════
// 真题侧常量表 —— 来源：docs/posts/computer/notes/真题考点分布.md
//   （该文由人工逐题审计 + 真题自带标签两套口径汇总，本站自建，非官方）
//
// ⚠️⚠️ 两套口径**不能相加、不能混读**：
//   audit（人工逐题审计）2021–2024 · 全题型 · 带估分 · **只覆盖 10 章**
//   tags （真题自带标签） 2021/2022/2024/2026 · 偏选择题 · **覆盖全部 20 章**
//   null = **该口径没有数据**，绝不等于 0。审计缺的章不代表没考。
//
// 为什么把真题数字**硬编码**在脚本里而不是每次去解析那个 md：
//   ① 那个 md 是给人读的，表格格式随时会被重排，正则解析脆得一碰就碎；
//   ② 这些数字变动频率极低（一次人工审计管一年），抄录一次 + 注明出处更可靠。
//   ③ 一旦改动，`真题考点分布.md` 的 `审计数 / 标签数` 就是唯一事实源，回那里核。
// ══════════════════════════════════════════════════════════════════════

// 真题文档用「1.6 数组」式 20 章编号；考纲用「⑥数组」式 21 模块。此表做 1:1 对齐。
const EXAM_CHAPTER_TO_MODULE = {
  '1.1': '①程序设计与C语言的基本概念',
  '1.2': '②数据的存储与运算',
  '1.3': '③顺序程序设计',
  '1.4': '④选择结构程序设计',
  '1.5': '⑤循环结构程序设计',
  '1.6': '⑥数组',
  '1.7': '⑦函数',
  '1.8': '⑧指针',
  '1.9': '⑨结构体',
  '1.10': '⑩文件',
  '1.11': '⑪运行环境与代码调试',
  '2.1': '⑫数据结构基本概念',
  '2.2': '⑬线性表',
  '2.3': '⑭栈和队列',
  '2.4': '⑮串、数组和广义表',
  '2.5': '⑯树和二叉树',
  '2.6': '⑰图',
  '2.7': '⑱查找',
  '2.8': '⑲排序',
  '2.9': '⑳算法的基本概念',   // 真题的「2.9 算法基本概念与分析」同时对应 ⑳ 与 ㉑
};

// 人工逐题审计（71 条 · 2021–2024 · 全题型）。score 为**估算**分值，非官方。
const EXAM_AUDIT = {
  '2.2':  { n: 15, score: 18, note: '年均3.75题' },
  '2.6':  { n: 11, score: 20, note: '年均2.75题' },
  '2.5':  { n: 10, score: 28, note: '年均2.5题，单章分值最高' },
  '1.8':  { n: 8,  score: 15, note: '年均2题' },
  '1.10': { n: 6,  score: 15, note: '年均1.5题' },
  '2.8':  { n: 4,  score: 15, note: '年均1题' },
  '1.9':  { n: 3,  score: null, note: '全部来自2023年' },
  '1.11': { n: 0,  score: null, note: '四年审计 0 题' },
};

// 真题自带标签机械统计（105 处 · 2021/2022/2024/2026 · 偏选择题）
const EXAM_TAGS = {
  '1.6': 14, '1.2': 12, '2.2': 12, '1.5': 7, '2.3': 7, '2.4': 7, '1.7': 6,
  '2.5': 6, '1.8': 5, '2.6': 5, '2.1': 4, '2.7': 4, '1.1': 3, '1.9': 3,
  '2.9': 3, '1.10': 2, '2.8': 2, '1.3': 1, '1.4': 1, '1.11': 1,
};

// 缺口判据 —— 必须显式写出来，否则「缺口」是我拍脑袋说的。
//
// ⚠️ 设计教训（v1 判据是错的，已改）：
//   第一版只看「知识点条数」，结果把 ⑭栈和队列（23 条 / 真题 7）也判成缺口 —— 假阳性。
//   真正区分「脆弱」的不是条数多少，而是**覆盖来源数**：
//     ⑰图   20 条 · **1 支视频** · 真题 11 题 → 单源扛高权重，最脆弱 ✅
//     ⑭栈队列 23 条 · 4 支视频 · 真题 7 处 → 四条独立来源互相印证，不脆弱 ❌
//   所以判据以「覆盖视频数」为主，「知识点条数」只用来抓「量本身极少」。
const GAP_RULES = [
  { label: 'gap',   desc: '真题 ≥6 题 且 覆盖视频 ≤1 支 → 高权重模块却只有单源覆盖，最脆弱' },
  { label: 'thin',  desc: '真题 ≥6 题 且 覆盖视频 ≤2 支；或 真题 ≥3 题 且 视频知识点 ≤10 条 → 来源少或量太少' },
  { label: 'thick', desc: '视频知识点 ≥45 条 且 覆盖视频 ≥2 支 且 真题 ≤4 处 → 视频讲得远比真题考的细，注意投入产出' },
  { label: 'ok',    desc: '其余 → 供需大致匹配' },
  { label: 'na',    desc: '真题侧无任何数据 → 无法判定（**不是「没问题」**）' },
];

function gapLabel(videoN, videoCount, examN) {
  if (examN == null) return 'na';
  if (examN >= 6 && videoCount <= 1) return 'gap';
  if (examN >= 6 && videoCount <= 2) return 'thin';
  if (examN >= 3 && videoN <= 10) return 'thin';
  if (videoN >= 45 && videoCount >= 2 && examN <= 4) return 'thick';
  return 'ok';
}

// 把「真题侧两套口径」折成模块键
function examForModule(mod) {
  const chapters = Object.entries(EXAM_CHAPTER_TO_MODULE).filter(([, m]) => m === mod).map(([c]) => c);
  if (!chapters.length) return { chapters: [], audit: null, tags: null };
  let audit = null, tags = 0, hasTags = false;
  for (const c of chapters) {
    if (EXAM_AUDIT[c]) {
      audit = audit || { n: 0, score: 0, hasScore: false, note: '' };
      audit.n += EXAM_AUDIT[c].n;
      if (EXAM_AUDIT[c].score != null) { audit.score += EXAM_AUDIT[c].score; audit.hasScore = true; }
      if (EXAM_AUDIT[c].note) audit.note = audit.note ? audit.note + '；' + EXAM_AUDIT[c].note : EXAM_AUDIT[c].note;
    }
    if (EXAM_TAGS[c] != null) { tags += EXAM_TAGS[c]; hasTags = true; }
  }
  return { chapters, audit, tags: hasTags ? tags : null };
}

// ── 解析 ──
function parseFile(file) {
  const text = fs.readFileSync(path.join(EXTRACT_DIR, file), 'utf8');
  const lines = text.split(/\r?\n/);
  const header = lines[0] || '';
  // # <单元> · <学科> · <视频名>（<UP>）
  const hp = header.replace(/^#\s*/, '').split('·').map(s => s.trim());
  const unit = hp[0] || file.replace(/\.md$/, '');
  const subject = (hp[1] || '未标').replace(/（.*$/, '').trim();
  const video = (hp[2] || '').replace(/（[^）]*）\s*$/, '').trim();
  const bv = (unit.match(/^(BV[0-9A-Za-z]+)/) || [])[1] || '?';

  let range = '';
  const rm = text.match(/^>\s*覆盖：(.+)$/m);
  if (rm) range = rm[1].trim();

  const sections = [];
  let topic = null, cur = null;
  for (const line of lines) {
    const h2 = line.match(/^##\s+(.+)$/);
    if (h2) { topic = h2[1].trim(); cur = null; continue; }
    const h3 = line.match(/^###\s+(.+)$/);
    if (h3) {
      cur = { unit, bv, subject, video, range, topic: topic || '（未分主题）', name: h3[1].trim(), concepts: [], pages: [], hasRelation: false };
      sections.push(cur);
      continue;
    }
    if (!cur) continue;
    const m = line.match(/^-\s*\*\*(要点|关键概念|相互关系|出处)\*\*[：:]\s*(.*)$/);
    if (!m) continue;
    if (m[1] === '关键概念') {
      for (const t of m[2].matchAll(/`([^`]+)`/g)) cur.concepts.push(t[1].trim());
    } else if (m[1] === '出处') {
      for (const t of m[2].matchAll(/P(\d+)/g)) cur.pages.push(Number(t[1]));
    } else if (m[1] === '相互关系') {
      cur.hasRelation = true;
    }
  }
  return { file, unit, bv, subject, video, range, sections };
}

/**
 * 归属判定。顺序很重要：
 *   1. 单元级超纲（见 OFF_UNIT_RATIO）—— 整单元排除
 *   2. 主题名命中超纲关键词 —— 单条排除
 *   3. 按**主题名**匹配模块（主题名是产出作者给的分类，比小节名可靠）
 *   4. 主题名没命中，才退到**小节名**
 * 教训：早期版本只看「主题名+小节名」混合串，导致 Word 的「查找」小节被归进 ⑱查找。
 */


function pct(a, b) { return b ? (a / b * 100).toFixed(1) + '%' : '—'; }
// 归一化：去掉空格 —— ASR 产出里「C 语言」和「C语言」并存，不归一化会漏匹配
function norm(s) { return String(s).replace(/\s+/g, ''); }
function pad(s, n) { s = String(s); let w = 0; for (const c of s) w += /[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/.test(c) ? 2 : 1; return s + ' '.repeat(Math.max(0, n - w)); }

// ── 主流程 ──
const files = fs.readdirSync(EXTRACT_DIR).filter(f => f.endsWith('.md') && !f.startsWith('_')).sort();
const units = files.map(parseFile);
const all = units.flatMap(u => u.sections);

const subjects = [...new Set(all.map(s => s.subject))];
const bySubject = {};
for (const s of subjects) bySubject[s] = all.filter(x => x.subject === s);

const videoIndex = new Map();       // bv -> {video, subject, units, sections}
for (const u of units) {
  if (!videoIndex.has(u.bv)) videoIndex.set(u.bv, { bv: u.bv, video: u.video, subject: u.subject, units: 0, sections: 0 });
  const v = videoIndex.get(u.bv);
  v.units++; v.sections += u.sections.length;
}

// 跨视频重复：同一知识点标题出现在几支视频
const nameToVideos = new Map();
for (const s of all) {
  if (!nameToVideos.has(s.name)) nameToVideos.set(s.name, new Set());
  nameToVideos.get(s.name).add(s.bv);
}
const repeated = [...nameToVideos.entries()].filter(([n, v]) => v.size >= 2 && !GENERIC_NAMES.has(n))
  .sort((a, b) => b[1].size - a[1].size || a[0].localeCompare(b[0]));
const genericRepeated = [...nameToVideos.entries()].filter(([n, v]) => v.size >= 2 && GENERIC_NAMES.has(n));

// 概念索引
const conceptToVideos = new Map();
for (const s of all) for (const c of s.concepts) {
  if (!conceptToVideos.has(c)) conceptToVideos.set(c, new Set());
  conceptToVideos.get(c).add(s.bv);
}
const topConcepts = [...conceptToVideos.entries()].sort((a, b) => b[1].size - a[1].size || a[0].localeCompare(b[0]));

// ── 单元级「整单元超纲」判定 ──
// 为什么要在单元级别判：逐条打关键词补丁会漏（Word 的「查找」小节 vs ⑱查找模块），
// 但一个**单元**（视频×分P 区间）的主题构成是稳定的 —— 全是 Office/OS/网络 的单元，
// 它的所有小节都该整块排除，不参与模块归位。
const OFF_UNIT_RATIO = 0.6;
const unitOff = new Map();          // unit -> {ratio, topics}
for (const u of units) {
  const topics = [...new Set(u.sections.map(s => s.topic))];
  const offTopics = topics.filter(t => OFF_SYLLABUS.some(k => t.includes(k)));
  const ratio = topics.length ? offTopics.length / topics.length : 0;
  unitOff.set(u.unit, { ratio, isOff: ratio >= OFF_UNIT_RATIO, topics: offTopics, nTopics: topics.length });
}

// 模块归位
function moduleReport(subject, table) {
  const secs = bySubject[subject] || [];
  const m = {};
  for (const mod of Object.keys(table)) m[mod] = { n: 0, videos: new Set(), topics: new Set() };
  const unplaced = [], off = [];
  for (const s of secs) {
    const uo = unitOff.get(s.unit);
    if (uo && uo.isOff) { off.push(s); continue; }
    if (OFF_SYLLABUS.some(k => s.topic.includes(k))) { off.push(s); continue; }
    const byTopic = Object.entries(table).filter(([, kws]) => kws.some(k => norm(s.topic).includes(norm(k)))).map(([mm]) => mm);
    const mods = byTopic.length ? byTopic
      : Object.entries(table).filter(([, kws]) => kws.some(k => norm(s.name).includes(norm(k)))).map(([mm]) => mm);
    if (!mods.length) { unplaced.push(s); continue; }
    for (const h of mods) { m[h].n++; m[h].videos.add(s.bv); m[h].topics.add(s.topic); }
  }
  return { m, unplaced, off, total: secs.length };
}

const lines = [];
const W = (s = '') => lines.push(s);

const snap = snapshotState();
const running = snap.staleMs < 5 * 60 * 1000;

W('# 考点库 · 跨视频合并 · 2026-09-19');
W('');
W('> 由 `scripts/bili_merge_extract.mjs` 从 `data/bili-analyze/_extract/*.md` 自动汇总生成。');
W('> 数据源是 B 站课程字幕经 AI 结构化后的知识点卡片，**不是官方考纲**。');
W('');
if (running) {
  W('> ## ⚠️ 这是**移动靶** —— 提取任务此刻仍在运行');
  W('>');
  W(`> 最后一次写入：**${new Date(snap.latest).toLocaleString('zh-CN')}**（${Math.round(snap.staleMs / 1000)} 秒前，文件 \`${snap.latestFile}\`）。`);
  W(`> 已提取 **${snap.doneBv.size} / ${snap.verifiedBv.length}** 支视频，**还有 ${snap.verifiedBv.length - snap.doneBv.size} 支没提取完**。`);
  W(`> （另有 ${snap.rejectedBv.length} 支被校验器判为离题、不计入分母，见文末「被拒视频」一节。）`);
  W('>');
  W('> **所以下面的数字会继续涨。** 等提取跑完，重跑一次本脚本即可刷新：');
  W('> ```bash');
  W('> node scripts/bili_merge_extract.mjs --md 备考计划/考点库-跨视频合并-2026-09-19.md --json data/bili-analyze/_extract/_merged.json --coverage data/bili-analyze/_extract/_coverage.json');
  W('> ```');
  W('>');
  W('> ⚠️ **三个 flag 必须一起给**。`--json`（全量，供搜索）与 `--coverage`（精简，供门户面板）');
  W('> 分两次跑会得到两个不同时刻的快照 —— 门户上「面板总数」与「搜索结果数」会对不上。');
  W('> 前端已加漂移检测（生成时间相差 > 60 秒即报警），但不如一开始就跑对。');
  W('');
}
W('## 一、口径与数据规模');
W('');
W('| 项 | 值 |');
W('|:---|---:|');
W(`| **快照时间** | ${new Date().toLocaleString('zh-CN')} |`);
W(`| 已提取视频 | **${snap.doneBv.size} / ${snap.verifiedBv.length}**${running ? '（⚠️ 仍在跑）' : '（已完成）'} |`);
if (snap.rejectedBv.length) {
  W(`| 校验拒收 | ${snap.rejectedBv.length} 支（**离题，非待办**）—— 见文末 |`);
}
W(`| 单元产出文件 | ${units.length} |`);
W(`| 知识点（\`###\` 小节） | ${all.length} |`);
W(`| 独立知识点名 | ${nameToVideos.size} |`);
W(`| 独立概念（\`关键概念\`） | ${conceptToVideos.size} |`);
W(`| 跨视频重复的知识点名 | ${repeated.length} |`);
W('');
W('**已核对**：`_extract` 引用的 754 处分P 出处，**junk 0 处**（详见 `B站视频管道诊断与内容可信度-2026-09-19.md` §4.2.1）。');
W('');
W('## 二、按科目');
W('');
W('| 科目 | 单元 | 视频 | 知识点 | 独立知识点名 |');
W('|:---|---:|---:|---:|---:|');
for (const s of subjects) {
  const secs = bySubject[s];
  const vs = new Set(secs.map(x => x.bv)).size;
  const un = new Set(secs.map(x => x.unit)).size;
  const names = new Set(secs.map(x => x.name)).size;
  W(`| ${s} | ${un} | ${vs} | ${secs.length} | ${names} |`);
}
W('');

W('## 三、按视频（单元数 / 知识点数）');
W('');
W('| BV | 科目 | 单元 | 知识点 | 视频名 |');
W('|:---|:---|---:|---:|:---|');
for (const v of [...videoIndex.values()].sort((a, b) => b.sections - a.sections)) {
  W(`| ${v.bv} | ${v.subject} | ${v.units} | ${v.sections} | ${v.video.slice(0, 40)} |`);
}
W('');

// ── 视频可信度分层（★ 本报告最重要的发现）──
if (bySubject['计算机']) {
  W('## 四、计算机视频 · 考纲对齐度分层 ★');
  W('');
  W('> **为什么单列这一节**：`_extract` 是按 BV 抓的，抓之前**没有校验「这支视频讲的是不是广东的考纲」**。');
  W('> 结果混进了整支讲「计算机基础」的课程 —— 标题写着「紧扣考纲」，但那是**别的考纲**。');
  W('');
  W('| BV | 考纲内 | 不在考纲内 | 考纲内率 | 视频名 |');
  W('|:---|---:|---:|:---|:---|');
  const rows = [];
  for (const v of videoIndex.values()) {
    if (v.subject !== '计算机') continue;
    const secs = all.filter(s => s.bv === v.bv);
    const offN = secs.filter(s => (unitOff.get(s.unit) || {}).isOff || OFF_SYLLABUS.some(k => s.topic.includes(k))).length;
    rows.push({ bv: v.bv, ok: secs.length - offN, off: offN, rate: secs.length ? (secs.length - offN) / secs.length : 0, video: v.video, units: v.units });
  }
  for (const r of rows.sort((a, b) => a.rate - b.rate)) {
    W(`| ${r.bv} | ${r.ok} | ${r.off} | ${(r.rate * 100).toFixed(1)}% | ${(r.video || '').slice(0, 34)} |`);
  }
  W('');
  W('**判读**：');
  W('');
  W('- 考纲内率 **< 30%** 的视频 → **整支不要看**，它讲的是另一个考纲。');
  W('- 考纲内率 **> 80%** → 可以用。');
  W('');
  W('### 4.1 交叉验证：真题里有没有计算机基础？');
  W('');
  W('只凭考纲文本下判断不够 —— 万一是考纲没写但真题在考。做了一次实证：');
  W('');
  W('在 `历年真题/计算机程序设计/` 的 **14 份真题（2018–2026）** 里检索：');
  W('');
  W('| 关键词组 | 命中 |');
  W('|:---|---:|');
  W('| 计算机基础（操作系统 / Word / Excel / 网络 / IP地址 / 多媒体 / 信息安全 / 病毒 / 总线 / 外存 / 计算机发展 / 冯诺依曼） | **0** |');
  W('| 对照组：C 语言 + 数据结构（指针 / 数组 / 结构体 / 二叉树 / 排序 / 线性表 / 时间复杂度） | 正常命中（指针 10 行、数组 24 行、线性表 12 行…） |');
  W('');
  W('**对照组是关键**：如果 C 语言关键词也 0 命中，说明是「搜法错了」（项目在高数 OCR 上踩过这个坑）。');
  W('对照组正常命中 → 证明检索有效 → **计算机基础确实不在真题里**。');
  W('');
  W('### 4.2 涉及的整单元超纲清单');
  W('');
  W('（单元级判定，阈值：≥60% 主题属计算机基础）');
  W('');
  W('| 单元 | 主题数 | 基础类主题 | 比例 | 判定 |');
  W('|:---|---:|---:|:---|:---|');
  for (const [unit, uo] of [...unitOff.entries()].filter(([, v]) => v.isOff).sort()) {
    W(`| ${unit} | ${uo.nTopics} | ${uo.topics.length} | ${(uo.ratio * 100).toFixed(0)}% | 🔴 整单元排除 |`);
  }
  W('');
}

// ── 计算机归位 ──
if (bySubject['计算机']) {
  const { m, unplaced, off, total } = moduleReport('计算机', COMPUTER_MODULES);
  W('## 五、计算机 · 按官方 21 模块归位');
  W('');
  W('> 来源：`docs/guide/2026考纲全解.md` §二（已对考试院原文核实）。');
  W('> ⚠️ 归属规则：**先判超纲 → 再按主题名 → 最后按小节名**。一个知识点可能同时命中多个模块，故各行之和 > 总数。');
  W('');
  W('| 官方模块 | 知识点 | 覆盖视频数 | 主要主题 |');
  W('|:---|---:|---:|:---|');
  for (const [mod, d] of Object.entries(m)) {
    const tp = [...d.topics].slice(0, 4).join('、');
    W(`| ${mod} | ${d.n} | ${d.videos.size} | ${tp}${d.topics.size > 4 ? ' …' : ''} |`);
  }
  W(`| **考纲内合计** | **${total - unplaced.length - off.length} / ${total}** | | |`);
  W('');
  W(`### 5.1 不在 2026 考纲内（计算机基础）：${off.length} 条（占 ${pct(off.length, total)}）`);
  W('');
  W('已核实官方原文：2026 考纲 21 个模块 **(一)~(二十一) 全部是 C 语言 + 数据结构**，');
  W('**没有**硬件 / 操作系统 / Office / 网络 / 多媒体 / 信息安全。');
  W('（来源：考试院原文转载 https://www.zjielts.com/newsinfo/8905126.html ，2026-01-05）');
  W('');
  W('| BV | 不在考纲内的知识点 | 占该视频 | 视频名 |');
  W('|:---|---:|:---|:---|');
  const offByVideo = {};
  for (const s of off) (offByVideo[s.bv] = offByVideo[s.bv] || []).push(s);
  for (const [bv, arr] of Object.entries(offByVideo).sort((a, b) => b[1].length - a[1].length)) {
    const v = videoIndex.get(bv);
    W(`| ${bv} | ${arr.length} | ${pct(arr.length, v.sections)} | ${(v.video || '').slice(0, 36)} |`);
  }
  W('');
  W('**涉及的计算机基础主题**：');
  W('');
  const offTopics = {};
  for (const s of off) offTopics[s.topic] = (offTopics[s.topic] || 0) + 1;
  for (const [t, n] of Object.entries(offTopics).sort((a, b) => b[1] - a[1]).slice(0, 30)) W(`- ${t}（${n}）`);
  W('');
  W('⚠️ **两条保留意见**：');
  W('1. 2027 考纲预计 2026-12 发布，**尚未发布**。若 2027 恢复考计算机基础，这批内容会重新有价值。');
  W('2. 部分视频是 **2023 年老课**，可能如实反映的是**当年**考纲 —— 不是 UP 主讲错，是考纲变了。');
  W('');
  W(`### 5.2 未命中任何模块：${unplaced.length} 条（占 ${pct(unplaced.length, total)}）`);
  W('');
  W('⚠️ **不要把「未归位」读成「超纲」** —— 多数是关键词规则没覆盖到。');
  W('');
  const unpTopics = {};
  for (const s of unplaced) unpTopics[s.topic] = (unpTopics[s.topic] || 0) + 1;
  for (const [t, n] of Object.entries(unpTopics).sort((a, b) => b[1] - a[1]).slice(0, 25)) W(`- ${t}（${n}）`);
  W('');
}

// ── 高数归位 ──
if (bySubject['高数']) {
  const { m, unplaced, total } = moduleReport('高数', MATH_MODULES);
  W('## 六、高数 · 按官方 12 章归位');
  W('');
  W('> 来源：`备考计划/考纲核实-高数12模块-2026-09-17.md`（考试院 + 新东方两源逐字一致）。');
  W('> ⚠️ 官方只到章节级，**没有子考点清单**。');
  W('');
  W('| 官方章节 | 知识点 | 覆盖视频数 | 主要主题 |');
  W('|:---|---:|---:|:---|');
  for (const [mod, d] of Object.entries(m)) {
    const tp = [...d.topics].slice(0, 4).join('、');
    W(`| ${mod} | ${d.n} | ${d.videos.size} | ${tp}${d.topics.size > 4 ? ' …' : ''} |`);
  }
  W(`| **归位合计** | **${total - unplaced.length} / ${total}** | | |`);
  W('');
  W(`### 6.1 未命中任何章节：${unplaced.length} 条（占 ${pct(unplaced.length, total)}）`);
  W('');
  const unpTopics = {};
  for (const s of unplaced) unpTopics[s.topic] = (unpTopics[s.topic] || 0) + 1;
  for (const [t, n] of Object.entries(unpTopics).sort((a, b) => b[1] - a[1]).slice(0, 25)) W(`- ${t}（${n}）`);
  W('');
}

// ── 英语 ──
if (bySubject['英语']) {
  const { m, unplaced, total } = moduleReport('英语', ENGLISH_MODULES);
  W('## 七、英语 · 按题型/语法域归位');
  W('');
  W('> ⚠️ 英语考纲没列模块，此表是**按用途自建**，不是官方口径。');
  W('');
  W('| 分类 | 知识点 | 覆盖视频数 | 主要主题 |');
  W('|:---|---:|---:|:---|');
  for (const [mod, d] of Object.entries(m)) W(`| ${mod} | ${d.n} | ${d.videos.size} | ${[...d.topics].slice(0, 4).join('、')} |`);
  W(`| **归位合计** | **${total - unplaced.length} / ${total}** | | |`);
  W('');
  if (unplaced.length) {
    W(`### 7.1 未归位：${unplaced.length} 条`);
    W('');
    const unpTopics = {};
    for (const s of unplaced) unpTopics[s.topic] = (unpTopics[s.topic] || 0) + 1;
    for (const [t, n] of Object.entries(unpTopics).sort((a, b) => b[1] - a[1])) W(`- ${t}（${n}）`);
    W('');
  }
}

// ── 跨视频重复 ──
W('## 八、跨视频重复的知识点（多源印证 = 可信度更高）');
W('');
W(`共 **${repeated.length}** 个知识点被 ≥2 支视频讲过（已剔除 ${genericRepeated.length} 个「解题步骤 / 易错点」这类泛化小节名）。`);
W('');
W('> **怎么用**：被多支视频独立讲到 → ① 内容更可能是真的（多源印证）② 更可能是重点。');
W('> 反之，只被 1 支视频讲到的，**可信度和重要性都待考**。');
W('');
W('| 知识点 | 视频数 |');
W('|:---|---:|');
for (const [n, v] of repeated.slice(0, 60)) W(`| ${n} | ${v.size} |`);
if (repeated.length > 60) W(`| …（还有 ${repeated.length - 60} 条） | |`);
W('');
W(`> 📌 **反向读数同样重要**：${all.length} 个知识点里，**只有 ${repeated.length} 个（${pct(repeated.length, all.length)}）有第二支视频印证**。`);
W('> 换句话说，**绝大多数考点目前是「单源」的** —— 单源不等于错，但**没有交叉验证**。');
W('> 这是这份数据最大的可信度缺口，也是 §十 第 2 条要强调的。');
W('');

W('## 九、跨视频高频概念 Top 60');
W('');
W('| 概念 | 视频数 |');
W('|:---|---:|');
for (const [c, v] of topConcepts.slice(0, 60)) W(`| \`${c}\` | ${v.size} |`);
W('');

W('## 十、这份表能回答 / 不能回答什么');
W('');
W('**能回答**：');
W('- 某个考纲模块，B 站课程覆盖了多少 → 缺口一目了然');
W('- 哪些知识点被多支视频重复讲 → 重点候选');
W('- 哪些视频混进了 2026 考纲没有的内容 → 避免白学');
W('');
W('**不能回答**（必须另外做）：');
W('- ❌ **考频**。视频讲得多 ≠ 真题考得多。要考频必须做真题逐题归类。');
W('- ❌ **正确性**。字幕是 ASR 产物，UP 主自己可能讲错。**多源印证能降低但不能消除**。');
W('- ❌ **题目**。产出规范明确要求「只提炼题型+套路+易错点，不抄题面」，所以这里**没有一道题**。');
W('  要题目得回到 `历年真题/` 和 `资料/*题库*.md`。');
W('');
/* ── 被拒视频：写出来，否则它们会以「还差 6 支」的形态反复回到待办列表 ── */
if (snap.rejectedBv.length) {
  W('## 十一、被校验器拒收的视频（**离题，不是待办**）');
  W('');
  W(`\`data/bili-analyze/\` 下有 ${snap.allBv.length} 个视频目录，但只有 ${snap.verifiedBv.length} 个是专升本内容。`);
  W('下面这些目录里 `_verify.jsonl` / `_verify2.jsonl` 的**每一段都是 `ok: false`** ——');
  W('即校验器判定字幕与专升本无关，提取步骤因此正确地跳过了它们。');
  W('');
  W('| 视频 | 实际内容（首段字幕） | 判定 |');
  W('|:---|:---|:---|');
  for (const bv of snap.rejectedBv.slice().sort()) {
    let first = '';
    try {
      const t = fs.readFileSync(path.join(ANALYZE_DIR, bv, 'subtitle_p01.txt'), 'utf8');
      first = t.split('\n').filter((l) => l.trim()).slice(0, 2).join(' / ').slice(0, 46);
    } catch { first = '(无字幕)'; }
    W(`| \`${bv}\` | ${first} | 全段 ok:false |`);
  }
  W('');
  W('**它们不需要被提取。** 把它们算进分母会造出一个不存在的缺口 ——');
  W('`freshness.knownBv` 因此只数「至少有一段 ok:true」的视频。');
  W('');
}
W('---');
W('');
W(`_生成时间：${new Date().toISOString().slice(0, 19).replace('T', ' ')}_`);

const out = lines.join('\n');

// ══════════════════════════════════════════════════════════════════════
// --coverage 产出（Studio 用，精简）
// ══════════════════════════════════════════════════════════════════════
function buildCoverage() {
  const reportFor = (subject, table) => {
    const { m, unplaced, off, total } = moduleReport(subject, table);
    const mods = Object.entries(m).map(([mod, d]) => {
      const ex = examForModule(mod);
      const examN = ex.audit ? ex.audit.n : ex.tags;
      return {
        mod,
        sections: d.n,
        videos: d.videos.size,
        videoList: [...d.videos].sort(),
        topics: [...d.topics].sort().slice(0, 6),
        topicCount: d.topics.size,
        exam: ex,
        gap: subject === '计算机' ? gapLabel(d.n, d.videos.size, examN) : null,
      };
    });
    return {
      total,
      placed: total - unplaced.length - off.length,
      unplaced: { n: unplaced.length, topics: topTopics(unplaced, 12) },
      offSyllabus: { n: off.length, topics: topTopics(off, 12) },
      modules: mods,
    };
  };

  // 视频层：考纲内率（计算机才判 —— 高数/英语没有「超纲」这个概念）
  const videoRows = [...videoIndex.values()].map(v => {
    const secs = all.filter(s => s.bv === v.bv);
    const offN = secs.filter(s => (unitOff.get(s.unit) || {}).isOff || OFF_SYLLABUS.some(k => s.topic.includes(k))).length;
    const onN = secs.length - offN;
    return {
      bv: v.bv, subject: v.subject, video: v.video,
      units: v.units, sections: secs.length,
      onSyllabus: onN, offSyllabus: offN,
      onRate: secs.length ? +(onN / secs.length).toFixed(3) : null,
      verdict: v.subject !== '计算机' ? 'na'
        : (onN / Math.max(secs.length, 1)) < 0.3 ? 'skip'
        : (onN / Math.max(secs.length, 1)) > 0.8 ? 'usable' : 'mixed',
    };
  }).sort((a, b) => b.sections - a.sections);

  // 跨模块缺口排行（只对计算机 —— 只有它有真题侧数据）
  // 排序：严重度优先（gap > thin > thick > ok > na），同档按「真题热度 / 覆盖来源数」降序
  const comp = reportFor('计算机', COMPUTER_MODULES);
  const SEV = { gap: 0, thin: 1, thick: 2, ok: 3, na: 4 };
  const ranked = comp.modules
    .filter(m => m.exam.audit || m.exam.tags != null)
    .map(m => {
      const examN = m.exam.audit ? m.exam.audit.n : m.exam.tags;
      return { mod: m.mod, videoN: m.sections, videoCount: m.videos, examN, gap: m.gap };
    })
    .sort((a, b) => (SEV[a.gap] - SEV[b.gap]) || (b.examN / Math.max(b.videoCount, 1)) - (a.examN / Math.max(a.videoCount, 1)));

  return {
    generatedAt: new Date().toISOString(),
    schema: 'studio-kaodian-coverage/1',
    sources: {
      extract: EXTRACT_DIR,
      merged: 'data/bili-analyze/_extract/_merged.json',
      exam: 'docs/posts/computer/notes/真题考点分布.md',
      syllabus: 'docs/guide/2026考纲全解.md',
    },
    freshness: {
      units: units.length,
      videos: videoIndex.size,
      sections: all.length,
      concepts: conceptToVideos.size,
      repeatedNames: repeated.length,
      latestWrite: snap.latest ? new Date(snap.latest).toISOString() : null,
      latestFile: snap.latestFile,
      /* ⚠️ staleMs / stillRunning 是**生成这一刻**的读数，写进文件就成了陈旧值。
         消费方（D:/studio 的 /api/kaodian）必须用 latestWrite 现算，别直接信这两个字段 ——
         否则门户会一直显示「提取仍在跑」，哪怕提取早在几十分钟前就停了。
         （2026-09-19 实际踩到：02:28 生成时按 231 秒判为 true，02:37 看时真实已 14.2 分钟。） */
      staleMs: snap.staleMs,
      stillRunning: running,
      extractedBv: snap.doneBv.size,
      /* 分母 = 至少有一段 ok:true 的视频（不是目录数）。见 snapshotState 注释。 */
      knownBv: snap.verifiedBv.length,
      allBvDirs: snap.allBv.length,
      rejectedBv: snap.rejectedBv.slice().sort(),
    },
    subjects: subjects.map(s => {
      const secs = bySubject[s];
      return {
        subject: s,
        units: new Set(secs.map(x => x.unit)).size,
        videos: new Set(secs.map(x => x.bv)).size,
        sections: secs.length,
        names: new Set(secs.map(x => x.name)).size,
      };
    }),
    computer: comp,
    math: bySubject['高数'] ? reportFor('高数', MATH_MODULES) : null,
    english: bySubject['英语'] ? reportFor('英语', ENGLISH_MODULES) : null,
    videos: videoRows,
    examGapRanking: ranked,
    gapRules: GAP_RULES,
    topRepeated: repeated.slice(0, 60).map(([n, v]) => ({ name: n, videos: [...v].sort(), n: v.size })),
    topConcepts: topConcepts.slice(0, 60).map(([c, v]) => ({ concept: c, videos: [...v].sort(), n: v.size })),
    // 诚实边界：Studio 面板要原样展示这几条，不能只显示好看的数字
    caveats: [
      '视频侧数字来自 B 站字幕 ASR → AI 结构化，**不是官方考纲**，UP 主可能讲错。',
      '「知识点条数」是产出里 `###` 小节数，同一知识点被多支视频讲会算多条 → 不能当「知识量」直接比大小。',
      '真题侧两套口径（人工逐题审计 / 真题自带标签）**不能相加**；审计只覆盖 10 章，缺的章不代表没考。',
      '缺口判据见 gapRules，是**启发式阈值**，不是统计检验。',
      '缺口 ≠ 现在就该学：算法层内容要先修完前置（如 1.6 数组）才谈得上。',
      running ? `⚠️ 提取任务此刻仍在跑（${snap.doneBv.size}/${snap.verifiedBv.length} 支），本快照是**移动靶**，数字会继续涨。` : `提取任务已完成（${snap.doneBv.size}/${snap.verifiedBv.length} 支），本快照稳定。`,
      snap.rejectedBv.length
        ? `另有 ${snap.rejectedBv.length} 支视频被校验器判为**离题**（每段 _verify 都是 ok:false），不计入上面的分母 —— 它们是抓错的数据，**不是待办**。`
        : null,
    ].filter(Boolean),
  };
}

function topTopics(secs, n) {
  const c = {};
  for (const s of secs) c[s.topic] = (c[s.topic] || 0) + 1;
  return Object.entries(c).sort((a, b) => b[1] - a[1]).slice(0, n).map(([t, k]) => ({ topic: t, n: k }));
}

const args = process.argv.slice(2);
const jsonIdx = args.indexOf('--json');
const mdIdx = args.indexOf('--md');
const covIdx = args.indexOf('--coverage');
if (jsonIdx >= 0 && args[jsonIdx + 1]) {
  fs.writeFileSync(args[jsonIdx + 1], JSON.stringify({
    generatedAt: new Date().toISOString(),
    units: units.map(u => ({ unit: u.unit, bv: u.bv, subject: u.subject, video: u.video, range: u.range, n: u.sections.length })),
    sections: all.map(s => ({ unit: s.unit, bv: s.bv, subject: s.subject, topic: s.topic, name: s.name, concepts: s.concepts, pages: s.pages, hasRelation: s.hasRelation })),
    repeated: repeated.map(([n, v]) => ({ name: n, videos: [...v] })),
    concepts: topConcepts.map(([c, v]) => ({ concept: c, videos: [...v] })),
  }, null, 1), 'utf8');
  console.log('JSON 已写：' + args[jsonIdx + 1]);
}
if (mdIdx >= 0 && args[mdIdx + 1]) {
  fs.mkdirSync(path.dirname(args[mdIdx + 1]), { recursive: true });
  fs.writeFileSync(args[mdIdx + 1], out, 'utf8');
  console.log('Markdown 已写：' + args[mdIdx + 1]);
}
if (covIdx >= 0 && args[covIdx + 1]) {
  const cov = buildCoverage();
  fs.mkdirSync(path.dirname(args[covIdx + 1]), { recursive: true });
  const text = JSON.stringify(cov, null, 1);
  fs.writeFileSync(args[covIdx + 1], text, 'utf8');
  console.log('覆盖度 JSON 已写：' + args[covIdx + 1] + `（${(Buffer.byteLength(text) / 1024).toFixed(1)} KB）`);
  const g = cov.examGapRanking.filter(x => x.gap === 'gap' || x.gap === 'thin');
  if (g.length) console.log('  缺口模块：' + g.map(x => `${x.mod}(视频${x.videoN}/真题${x.examN})`).join(' · '));
}
if (jsonIdx < 0 && mdIdx < 0 && covIdx < 0) console.log(out);
