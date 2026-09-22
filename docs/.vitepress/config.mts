import { defineConfig } from 'vitepress'

// GitHub Pages 项目站固定 base
const base = process.env.VITEPRESS_BASE || '/darling016123/'

export default defineConfig({
  title: '专升本笔记 · Sakiko 风',
  description: 'Obsidian 全库 + 历年真题详解 · 公共课 + 计算机',
  lang: 'zh-CN',
  base,
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: false,

  // ── 从公开站排除「非备考内容」────────────────────────────
  // 这些文件仍保留在仓库里（AI/开发者自用），只是不发布到站点。
  // 排除理由：它们是开发文档或内部审计产物，不是给考生看的内容；
  // 且它们此前「未进任何导航」——用户从任何入口都到不了，属隐形页。
  srcExclude: [
    '**/README.md',                          // 项目维基等
    'guide/bili-scraping.md',                // B站爬取技术笔记
    'guide/ai-assisted-reverse-engineering.md', // AI 辅助逆向方法论（开发者自用，非备考内容）
    'guide/bili-subtitle-pipeline-perf.md',  // 字幕抓取链路效率分析（开发者自用）
    'guide/ai-learning-assistant.md',        // 个人项目方案文档
    'dependency-graph.md',                   // 项目依赖全景图
    'wiki-repo/**',                          // 仓库模块维基
    'posts/computer/notes/audit-*.md',       // 10 份章节审计报告（内部 QA 产物）
    '_templates/**',                         // 真题页模板规范（作者自用，不是备考内容）
  ],

  head: [
    ['link', { rel: 'icon', href: `${base}favicon.svg` }],
    ['meta', { name: 'theme-color', content: '#e4596f' }],
    // PWA
    ['link', { rel: 'manifest', href: `${base}manifest.json` }],
    ['link', { rel: 'apple-touch-icon', href: `${base}icon-192.png` }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'default' }],
    ['script', {}, `if ('serviceWorker' in navigator) { window.addEventListener('load', () => navigator.serviceWorker.register('${base}sw.js').catch(() => {})); }`],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { href: 'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@600;700&display=swap', rel: 'stylesheet' }],
  ],

  markdown: {
    math: true,
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark',
    },
  },

  themeConfig: {
    logo: '/favicon.svg',
    siteTitle: '专升本笔记',
    outline: {
      level: [2, 3],
      label: '本页目录',
    },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
          modal: {
            noResultsText: '没有结果',
            resetButtonTitle: '清空',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },
    nav: [
      { text: '首页', link: '/' },
      { text: '🗂 真题索引', link: '/posts/真题索引' },
      {
        text: '高数',
        items: [
          { text: '📖 学习手册 ⭐', link: '/posts/math/学习手册' },
          { text: '📖 全程班笔记 ⭐', link: '/posts/math/全程班笔记/' },
          { text: '章节笔记', link: '/posts/math/notes/' },
          { text: '真题总览', link: '/posts/math/' },
          { text: '2026 全卷', link: '/posts/math/2026' },
          { text: '2024 全卷', link: '/posts/math/2024' },
        ],
      },
      {
        text: '计算机',
        items: [
          { text: '📖 学习手册 ⭐', link: '/posts/computer/学习手册' },
          { text: '2027 备考指南 ⭐', link: '/posts/computer/2027-备考指南' },
          { text: '知识点', link: '/posts/computer/notes/' },
          { text: '2024 全卷', link: '/posts/computer/2024' },
          { text: '考点拆分', link: '/posts/computer/topics/' },
          { text: '📊 真题考点分布', link: '/posts/computer/notes/真题考点分布' },
          { text: '真题总览', link: '/posts/computer/' },
        ],
      },
      {
        text: '英语',
        items: [
          { text: '📖 学习手册 ⭐', link: '/posts/english/学习手册' },
          { text: '学习笔记', link: '/posts/english/notes/' },
          { text: '真题总览', link: '/posts/english/' },
          { text: '2024', link: '/posts/english/2024' },
          { text: '2023', link: '/posts/english/2023' },
        ],
      },
      {
        text: '政治',
        items: [
          { text: '📖 学习手册 ⭐', link: '/posts/politics/学习手册' },
          { text: '系统笔记', link: '/posts/politics/notes/' },
          { text: '真题总览', link: '/posts/politics/' },
          { text: '大纲题型', link: '/posts/politics/notes/00-考试大纲与题型' },
        ],
      },
      { text: '🎯 0 基础', link: '/guide/零基础总入口' },
      {
        text: '📝 刷题',
        items: [
          { text: '📚 题库', link: '/posts/题库/' },
          { text: '🧪 模拟卷', link: '/posts/模拟卷/' },
        ],
      },
      {
        text: '🇯🇵 日语',
        items: [
          { text: '学习路线', link: '/learn/' },
          {
            text: '🎯 入门与工具',
            items: [
              { text: '零基础五十音入门', link: '/learn/zero-baseline' },
              { text: '从零开始学日语（24 周路线）', link: '/learn/systematic-japanese-learning-guide' },
              { text: '🗺️ 0→N1 执行手册', link: '/learn/japanese-video-route-plan' },
              { text: '✅ 核心知识点清单', link: '/learn/japanese-core-checklist' },
              { text: '📝 JLPT 真题用法', link: '/learn/japanese-jlpt-past-papers' },
            ],
          },
          {
            text: '📚 深度笔记 · 逐条语法详解（最详细）',
            items: [
              { text: '总纲 · 七卷目录（0→N1 共 104 课）', link: '/course/japanese/deep/' },
            ],
          },
          {
            text: '🎧 跟课笔记 · 老师怎么讲、哪里容易错',
            items: [
              { text: '课程总纲 · 六卷（跟阿飞老师 0→N1）', link: '/course/japanese/' },
            ],
          },
          {
            text: '📖 同步手册 · 浓缩（每课 4 行）⚠️ 中高级语法点待修正',
            items: [
              { text: '三卷总目录', link: '/learn/standard-japanese/' },
              { text: '词类与变形总览', link: '/learn/standard-japanese/conjugation-guide' },
              { text: '第一卷 · 初级篇（1–48 课）· 已核对无误', link: '/learn/standard-japanese/elementary' },
              { text: '第二卷 · 中级篇（1–32 课）⚠️ 语法点错位', link: '/learn/standard-japanese/intermediate' },
              { text: '第三卷 · 高级篇（1–24 课）⚠️ 语法点错位', link: '/learn/standard-japanese/advanced' },
            ],
          },
        ],
      },
      {
        text: '🎬 B站视频调研',
        items: [
          { text: '日语 0 基础 → N1', link: '/learn/bili-japanese-n1-videos' },
          { text: '英语雅思', link: '/learn/bili-ielts-videos' },
          { text: '📚 历年真题调研', link: '/learn/bili-past-papers' },
        ],
      },
      {
        text: '📖 指南',
        items: [
          { text: '使用说明', link: '/guide/' },
          { text: '🎯 四科备考总纲', link: '/guide/四科备考总纲' },
          { text: '🗺️ 知识地图', link: '/guide/knowledge-map/' },
          { text: '🎬 B站资源', link: '/guide/bili-resources' },
          { text: '🎬 B站吸收规划', link: '/guide/bili-plan/' },
          { text: '🎯 公办院校与录取', link: '/guide/公办院校与录取' },
          { text: '💻 计算机专业报考', link: '/guide/计算机专业-报考指南' },
          { text: '📊 投档与招生数据', link: '/guide/投档与招生数据' },
          { text: '📈 2026 省控线', link: '/guide/省控线-录取分数线' },
        ],
      },
      {
        text: '📊 高频考点',
        items: [
          { text: '总览', link: '/posts/高频考点/' },
          { text: '★ 真题考点总析（2018–2026）', link: '/posts/高频考点/真题考点总析' },
          { text: '计算机 TOP20（已归档）', link: '/posts/高频考点/计算机-高频考点TOP20' },
          { text: '政治 TOP20（已归档）', link: '/posts/高频考点/政治-高频考点TOP20' },
          { text: '高数 TOP20（已归档）', link: '/posts/高频考点/高数-高频考点TOP20' },
          { text: '英语 TOP20（已归档）', link: '/posts/高频考点/英语-高频考点TOP20' },
        ],
      },
    ],
    sidebar: {
      '/course/': [
        {
          text: '🎧 日语跟课笔记（新标日 0→N1）',
          items: [
            { text: '课程总纲', link: '/course/japanese/' },
            { text: '入门篇 · 五十音到声调', link: '/course/japanese/00-入门篇' },
            { text: '初级上 · 第 1–24 课', link: '/course/japanese/01-初级上' },
            { text: '初级下 · 第 25–48 课', link: '/course/japanese/02-初级下' },
            { text: '中级上 · 第 1–11 课', link: '/course/japanese/03-中级上' },
            { text: '中级下 · 第 12–21 课', link: '/course/japanese/04-中级下' },
            { text: '复习总表', link: '/course/japanese/05-复习总表' },
            { text: '知识点四类索引', link: '/course/japanese/06-知识点四类索引' },
          ],
        },
        {
          text: '📚 标日深度笔记（0→N1 逐课详解）',
          items: [
            { text: '总纲 · 来源与用法', link: '/course/japanese/deep/' },
            { text: '第一卷 · 初级上（第 1–24 课）', link: '/course/japanese/deep/01-初级上' },
            { text: '第二卷 · 初级下（第 25–48 课）', link: '/course/japanese/deep/02-初级下' },
            { text: '第三卷 · 中级上（第 1–16 课）', link: '/course/japanese/deep/03-中级上' },
            { text: '第四卷 · 中级下（第 17–32 课）', link: '/course/japanese/deep/04-中级下' },
            { text: '第五卷 · 高级上（第 1–12 课）', link: '/course/japanese/deep/05-高级上' },
            { text: '第六卷 · 高级下（第 13–24 课）', link: '/course/japanese/deep/06-高级下' },
            { text: '第七卷 · N1 体系总览', link: '/course/japanese/deep/07-N1体系总览' },
          ],
        },
      ],
      '/learn/': [
        {
          text: '🇯🇵 日语学习',
          items: [
            { text: '学习路线', link: '/learn/' },
            { text: '🎯 零基础五十音入门', link: '/learn/zero-baseline' },
            { text: '从零开始学日语 📖', link: '/learn/systematic-japanese-learning-guide' },
            { text: '🗺️ 0→N1 执行手册', link: '/learn/japanese-video-route-plan' },
            { text: '✅ 核心知识点清单', link: '/learn/japanese-core-checklist' },
            { text: '📝 JLPT 真题用法', link: '/learn/japanese-jlpt-past-papers' },
          ],
        },
        {
          text: '📚 深度笔记 · 逐条语法详解（最详细）',
          items: [
            { text: '总纲 · 七卷目录（0→N1 共 104 课）', link: '/course/japanese/deep/' },
          ],
        },
        {
          text: '🎧 跟课笔记 · 老师怎么讲、哪里容易错',
          items: [
            { text: '课程总纲 · 六卷（跟阿飞老师 0→N1）', link: '/course/japanese/' },
          ],
        },
        {
          text: '📖 同步手册 · 浓缩（每课 4 行）⚠️ 中高级语法点待修正',
          items: [
            { text: '三卷总目录', link: '/learn/standard-japanese/' },
            { text: '词类与变形总览', link: '/learn/standard-japanese/conjugation-guide' },
            { text: '第一卷：初级篇 · 已核对无误', link: '/learn/standard-japanese/elementary' },
            { text: '第二卷：中级篇 ⚠️ 语法点错位', link: '/learn/standard-japanese/intermediate' },
            { text: '第三卷：高级篇 ⚠️ 语法点错位', link: '/learn/standard-japanese/advanced' },
          ],
        },
        {
          text: '🎬 B站视频调研',
          items: [
            { text: '日语 0 基础 → N1', link: '/learn/bili-japanese-n1-videos' },
            { text: '英语雅思', link: '/learn/bili-ielts-videos' },
            { text: '📚 历年真题调研', link: '/learn/bili-past-papers' },
          ],
        },
      ],
      '/posts/math/': [
        {
          text: '高等数学 · 真题',
          items: [
                    {
                              "text": "📖 学习手册（零基础版）",
                              "link": "/posts/math/学习手册"
                    },
                    {
                              "text": "📖 全程班笔记 · 总目录",
                              "link": "/posts/math/全程班笔记/"
                    },
                    {
                              "text": "真题总览",
                              "link": "/posts/math/"
                    },
                    {
                              "text": "高频考点 TOP20 📊",
                              "link": "/posts/高频考点/高数-高频考点TOP20"
                    },
                    {
                              "text": "章节笔记总览",
                              "link": "/posts/math/notes/"
                    },
                    {
                              "text": "教材目录基准 📗",
                              "link": "/posts/math/教材目录基准"
                    },
                    {
                              "text": "考试大纲与考情 📋",
                              "link": "/posts/math/notes/syllabus"
                    },
                    {
                              "text": "真题章节对照表 🎯",
                              "link": "/posts/math/真题章节对照表"
                    },
                    {
                              "text": "2026 黄金知识汇编 ⭐",
                              "link": "/posts/math/2026-黄金知识汇编"
                    },
                    {
                              "text": "公式速查卡 📐",
                              "link": "/posts/math/公式速查卡"
                    },
                    {
                              "text": "黄金汇编刷题 ✍️",
                              "link": "/posts/math/2026-黄金知识汇编-刷题"
                    },
                    {
                              "text": "2026 全卷",
                              "link": "/posts/math/2026"
                    },
                    {
                              "text": "2025 全卷",
                              "link": "/posts/math/2025"
                    },
                    {
                              "text": "2025 真题回忆版 📷",
                              "link": "/posts/math/notes/2025-真题回忆版"
                    },
                    {
                              "text": "2024 全卷",
                              "link": "/posts/math/2024"
                    },
                    {
                              "text": "2023 演练",
                              "link": "/posts/math/2023"
                    },
                    {
                              "text": "2022 演练",
                              "link": "/posts/math/2022"
                    },
                    {
                              "text": "2021 演练",
                              "link": "/posts/math/2021"
                    },
                    {
                              "text": "2020 演练",
                              "link": "/posts/math/2020"
                    },
                    {
                              "text": "2020 原卷文字版 📄",
                              "link": "/posts/math/2020-原卷文字版"
                    },
                    {
                              "text": "2019 演练",
                              "link": "/posts/math/2019"
                    },
                    {
                              "text": "2018 演练",
                              "link": "/posts/math/2018"
                    }
          ],
        },
        {
          text: "📖 全程班笔记（10 章 · 751 例题）",
          collapsed: true,
          items: [
            { text: "1上 函数", link: "/posts/math/全程班笔记/01-第一章上-函数" },
            { text: "1下 极限与连续", link: "/posts/math/全程班笔记/02-第一章下-极限与连续" },
            { text: "2 导数与微分", link: "/posts/math/全程班笔记/03-第二章-导数与微分" },
            { text: "3一 不定积分", link: "/posts/math/全程班笔记/04-第三章一-不定积分" },
            { text: "3二 换元法与分部积分", link: "/posts/math/全程班笔记/05-第三章二-换元法与分部积分" },
            { text: "3三 定积分及其应用", link: "/posts/math/全程班笔记/06-第三章三-定积分及其应用" },
            { text: "4 向量代数与空间解析几何", link: "/posts/math/全程班笔记/07-第四章-向量代数与空间解析几何" },
            { text: "5 多元函数微分学", link: "/posts/math/全程班笔记/08-第五章-多元函数微分学" },
            { text: "6 二重积分", link: "/posts/math/全程班笔记/09-第六章-二重积分" },
            { text: "7 曲线积分", link: "/posts/math/全程班笔记/10-第七章-曲线积分" },
            { text: "8 微分方程", link: "/posts/math/全程班笔记/11-第八章-微分方程" },
            { text: "9 级数", link: "/posts/math/全程班笔记/12-第九章-级数" },
            { text: "10 中值定理与证明题", link: "/posts/math/全程班笔记/13-第十章-中值定理与证明" },
          ],
        },
        {
          text: "笔记 · 一章 函数与极限",
          collapsed: true,
          items: [
            { text: "1.1 函数的概念", link: "/posts/math/notes/1.1-函数的概念" },
            { text: "1.2 数列的极限", link: "/posts/math/notes/1.2-数列的极限" },
            { text: "1.3 函数的极限", link: "/posts/math/notes/1.3-函数的极限" },
            { text: "1.4 等价无穷小替换原理", link: "/posts/math/notes/1.4-等价无穷小替换原理" },
            { text: "1.5 极限运算法则", link: "/posts/math/notes/1.5-极限运算法则" },
            { text: "1.6 两个重要极限", link: "/posts/math/notes/1.6-两个重要极限" },
            { text: "1.7 左右极限与极限存在判定", link: "/posts/math/notes/1.7-左右极限与极限存在判定" },
            { text: "1.8 极限界限之“抓大头”法则", link: "/posts/math/notes/1.8-极限界限之“抓大头”法则" },
            { text: "1.9 初等函数的连续性", link: "/posts/math/notes/1.9-初等函数的连续性" },
            { text: "1.10 极限计算三法决策树 ⭐", link: "/posts/math/notes/1.10-极限计算三法决策树" },
            { text: "1.11 极限求值零基础·抓大头 ⭐", link: "/posts/math/notes/1.11-极限求值零基础-抓大头" },
            { text: "1.12 函数的连续性与间断点分类", link: "/posts/math/notes/1.12-函数的连续性与间断点分类" },
            { text: "1.13 函数的连续性", link: "/posts/math/notes/1.13-函数的连续性" },
            { text: "1.14 闭区间上连续函数的性质", link: "/posts/math/notes/1.14-闭区间上连续函数的性质" },
          ],
        },
        {
          text: "笔记 · 二章 一元函数微分学",
          collapsed: true,
          items: [
                    {
                              "text": "2.1 导数的定义",
                              "link": "/posts/math/notes/2.1-导数的定义"
                    },
                    {
                              "text": "2.2 单侧导数以及可导与连续的关系",
                              "link": "/posts/math/notes/2.2-单侧导数以及可导与连续的关系"
                    },
                    {
                              "text": "2.3 基本导数公式和四则运算求导法…",
                              "link": "/posts/math/notes/2.3-基本导数公式和四则运算求导法则"
                    },
                    {
                              "text": "2.4 复合函数的求导方法（链式法则…",
                              "link": "/posts/math/notes/2.4-复合函数的求导方法（链式法则）"
                    },
                    {
                              "text": "2.5 隐函数与参数方程求导方法",
                              "link": "/posts/math/notes/2.5-隐函数与参数方程求导方法"
                    },
                    {
                              "text": "2.6 高阶导数",
                              "link": "/posts/math/notes/2.6-高阶导数"
                    },
                    {
                              "text": "2.7 微分",
                              "link": "/posts/math/notes/2.7-微分"
                    },
                    {
                              "text": "2.8 微分中值定理（罗尔与拉格朗日…",
                              "link": "/posts/math/notes/2.8-微分中值定理（罗尔与拉格朗日）"
                    },
                    {
                              "text": "2.9 洛必达法则",
                              "link": "/posts/math/notes/2.9-洛必达法则"
                    },
                    {
                              "text": "2.10 导数的几何应用（切线与单调…",
                              "link": "/posts/math/notes/2.10-导数的几何应用（切线与单调性）"
                    },
                    {
                              "text": "2.11 函数的极值与曲线凹凸性",
                              "link": "/posts/math/notes/2.11-函数的极值与曲线凹凸性"
                    },
                    {
                              "text": "2.12 函数曲线的渐近线",
                              "link": "/posts/math/notes/2.12-函数曲线的渐近线"
                    },
                    {
                              "text": "2.13 泰勒公式与麦克劳林公式",
                              "link": "/posts/math/notes/2.13-泰勒公式与麦克劳林公式"
                    },
                    {
                              "text": "2.14 曲率",
                              "link": "/posts/math/notes/2.14-曲率"
                    }
          ],
        },
        {
          text: "笔记 · 三章 一元函数积分学",
          collapsed: true,
          items: [
                    {
                              "text": "3.1 原函数与不定积分的概念及性质",
                              "link": "/posts/math/notes/3.1-原函数与不定积分的概念及性质"
                    },
                    {
                              "text": "3.2 直接积分法",
                              "link": "/posts/math/notes/3.2-直接积分法"
                    },
                    {
                              "text": "3.3 第一类换元法（凑微分法）",
                              "link": "/posts/math/notes/3.3-第一类换元法（凑微分法）"
                    },
                    {
                              "text": "3.4 第二类换元法之根式代换",
                              "link": "/posts/math/notes/3.4-第二类换元法之根式代换"
                    },
                    {
                              "text": "3.5 第二类换元法之三角代换",
                              "link": "/posts/math/notes/3.5-第二类换元法之三角代换"
                    },
                    {
                              "text": "3.6 分部积分法",
                              "link": "/posts/math/notes/3.6-分部积分法"
                    },
                    {
                              "text": "3.7 定积分的概念",
                              "link": "/posts/math/notes/3.7-定积分的概念"
                    },
                    {
                              "text": "3.8 牛顿-莱布尼兹公式及定积分的…",
                              "link": "/posts/math/notes/3.8-牛顿-莱布尼兹公式及定积分的性质"
                    },
                    {
                              "text": "3.9 定积分的换元法",
                              "link": "/posts/math/notes/3.9-定积分的换元法"
                    },
                    {
                              "text": "3.10 定积分的分部积分法",
                              "link": "/posts/math/notes/3.10-定积分的分部积分法"
                    },
                    {
                              "text": "3.11 积分变限函数及其导数",
                              "link": "/posts/math/notes/3.11-积分变限函数及其导数"
                    },
                    {
                              "text": "3.12 反常积分（广义积分）",
                              "link": "/posts/math/notes/3.12-反常积分（广义积分）"
                    },
                    {
                              "text": "3.13 求平面图形的面积",
                              "link": "/posts/math/notes/3.13-求平面图形的面积"
                    },
                    {
                              "text": "3.14 求旋转体的体积",
                              "link": "/posts/math/notes/3.14-求旋转体的体积"
                    },
                    {
                              "text": "3.15 有理函数的积分",
                              "link": "/posts/math/notes/3.15-有理函数的积分"
                    },
                    {
                              "text": "3.16 定积分的元素法（微元法）",
                              "link": "/posts/math/notes/3.16-定积分的元素法"
                    },
                    {
                              "text": "3.17 定积分在物理学上的应用",
                              "link": "/posts/math/notes/3.17-定积分在物理学上的应用"
                    }
          ],
        },
        {
          text: "笔记 · 四章 向量与空间几何",
          collapsed: true,
          items: [
                    {
                              "text": "4.1 空间直角坐标系与向量的线性运…",
                              "link": "/posts/math/notes/4.1-空间直角坐标系与向量的线性运算"
                    },
                    {
                              "text": "4.2 向量的数量积与向量积",
                              "link": "/posts/math/notes/4.2-向量的数量积与向量积"
                    },
                    {
                              "text": "4.3 平面及其方程",
                              "link": "/posts/math/notes/4.3-平面及其方程"
                    },
                    {
                              "text": "4.4 空间直线及其方程",
                              "link": "/posts/math/notes/4.4-空间直线及其方程"
                    },
                    {
                              "text": "4.5 曲面与空间曲线",
                              "link": "/posts/math/notes/4.5-曲面与空间曲线"
                    }
          ],
        },
        {
          text: "笔记 · 五章 多元函数",
          collapsed: true,
          items: [
                    {
                              "text": "5.1 多元函数的基本概念",
                              "link": "/posts/math/notes/5.1-多元函数的基本概念"
                    },
                    {
                              "text": "5.2 偏导数与全微分",
                              "link": "/posts/math/notes/5.2-偏导数与全微分"
                    },
                    {
                              "text": "5.3 多元复合函数与隐函数求导法",
                              "link": "/posts/math/notes/5.3-多元复合函数与隐函数求导法"
                    },
                    {
                              "text": "5.4 多元函数的极值",
                              "link": "/posts/math/notes/5.4-多元函数的极值"
                    },
                    {
                              "text": "5.5 多元函数微分学的几何应用",
                              "link": "/posts/math/notes/5.5-多元函数微分学的几何应用"
                    },
                    {
                              "text": "5.6 方向导数与梯度",
                              "link": "/posts/math/notes/5.6-方向导数与梯度"
                    },
          ],
        },
        {
          text: "笔记 · 六章 重积分与曲线积分",
          collapsed: true,
          items: [
                    {
                              "text": "6.1 二重积分的概念与性质",
                              "link": "/posts/math/notes/6.1-二重积分的概念与性质"
                    },
                    {
                              "text": "6.2 二重积分的计算",
                              "link": "/posts/math/notes/6.2-二重积分的计算"
                    },
                    {
                              "text": "6.3 三重积分",
                              "link": "/posts/math/notes/6.3-三重积分"
                    },
                    {
                              "text": "6.4 曲线积分",
                              "link": "/posts/math/notes/6.4-曲线积分"
                    },
                    {
                              "text": "6.5 重积分的应用",
                              "link": "/posts/math/notes/6.5-重积分的应用"
                    },
                    {
                              "text": "6.6 曲面积分（选学）",
                              "link": "/posts/math/notes/6.6-曲面积分"
                    },
          ],
        },
        {
          text: "笔记 · 七章 常微分方程",
          collapsed: true,
          items: [
                    {
                              "text": "7.1 微分方程的基本概念",
                              "link": "/posts/math/notes/7.1-微分方程的基本概念"
                    },
                    {
                              "text": "7.2 一阶微分方程",
                              "link": "/posts/math/notes/7.2-一阶微分方程"
                    },
                    {
                              "text": "7.3 高阶线性微分方程",
                              "link": "/posts/math/notes/7.3-高阶线性微分方程"
                    }
          ],
        },
        {
          text: "笔记 · 八章 无穷级数",
          collapsed: true,
          items: [
                    {
                              "text": "8.1 常数项级数的概念与性质",
                              "link": "/posts/math/notes/8.1-常数项级数的概念与性质"
                    },
                    {
                              "text": "8.2 正项级数审敛法",
                              "link": "/posts/math/notes/8.2-正项级数审敛法"
                    },
                    {
                              "text": "8.3 幂级数",
                              "link": "/posts/math/notes/8.3-幂级数"
                    },
                    {
                              "text": "8.4 傅里叶级数",
                              "link": "/posts/math/notes/8.4-傅里叶级数"
                    }
          ],
        },
      ],
      '/posts/computer/': [
        {
          text: '计算机 · 真题',
          items: [
                    {
                              "text": "📖 学习手册（零基础版）",
                              "link": "/posts/computer/学习手册"
                    },
                    {
                              "text": "2027 备考指南 ⭐",
                              "link": "/posts/computer/2027-备考指南"
                    },
                    {
                              "text": "真题总览",
                              "link": "/posts/computer/"
                    },
                    {
                              "text": "真题章节对照表 🎯",
                              "link": "/posts/computer/真题章节对照表"
                    },
                    {
                              "text": "真题考点分布 📊",
                              "link": "/posts/computer/notes/真题考点分布"
                    },
                    {
                              "text": "高频考点 TOP20 📊",
                              "link": "/posts/高频考点/计算机-高频考点TOP20"
                    },
                    {
                              "text": "知识点总览",
                              "link": "/posts/computer/notes/"
                    },
                    {
                              "text": "教材目录基准 📗",
                              "link": "/posts/computer/教材目录基准"
                    },
                    {
                              "text": "考试大纲与试卷结构 📋",
                              "link": "/posts/computer/notes/syllabus"
                    },
                    {
                              "text": "全书索引目录",
                              "link": "/posts/computer/notes/全书索引目录"
                    },
                    {
                              "text": "2026 黄金知识汇编 ⭐",
                              "link": "/posts/computer/2026-黄金知识汇编"
                    },
                    {
                              "text": "黄金汇编刷题 ✍️",
                              "link": "/posts/computer/2026-黄金知识汇编-刷题"
                    },
                    {
                              "text": "2026 题型变化",
                              "link": "/posts/computer/2026"
                    },
                    {
                              "text": "2026 回忆版详解 📝",
                              "link": "/posts/computer/2026-回忆版详解"
                    },
                    {
                              "text": "2025 真题回忆版",
                              "link": "/posts/computer/2025-真题回忆版"
                    },
                    {
                              "text": "2025 题型确认",
                              "link": "/posts/computer/2025"
                    },
                    {
                              "text": "2024 全卷",
                              "link": "/posts/computer/2024"
                    },
                    {
                              "text": "原卷文字版 2021-2024 📄",
                              "link": "/posts/computer/原卷文字版"
                    },
                    {
                              "text": "2023 演练",
                              "link": "/posts/computer/2023"
                    },
                    {
                              "text": "2022 演练",
                              "link": "/posts/computer/2022"
                    },
                    {
                              "text": "2021 演练",
                              "link": "/posts/computer/2021"
                    },
                    {
                              "text": "2020 演练",
                              "link": "/posts/computer/2020"
                    },
                    {
                              "text": "2019 演练",
                              "link": "/posts/computer/2019"
                    },
                    {
                              "text": "2018 演练",
                              "link": "/posts/computer/2018"
                    }
          ],
        },
        {
          text: 'C 语言知识点',
          collapsed: false,
          items: [
                    {
                              "text": "0.0 计算机基础理论",
                              "link": "/posts/computer/notes/0.0-计算机基础理论"
                    },
                    {
                              "text": "1.1 C语言概述与基本概念",
                              "link": "/posts/computer/notes/1.1-C语言概述与基本概念"
                    },
                    {
                              "text": "1.2 数据的存储与运算",
                              "link": "/posts/computer/notes/1.2-数据的存储与运算"
                    },
                    {
                              "text": "1.3 顺序程序设计",
                              "link": "/posts/computer/notes/1.3-顺序程序设计"
                    },
                    {
                              "text": "1.4 选择结构程序设计",
                              "link": "/posts/computer/notes/1.4-选择结构程序设计"
                    },
                    {
                              "text": "1.5 循环结构程序设计",
                              "link": "/posts/computer/notes/1.5-循环结构程序设计"
                    },
                    {
                              "text": "1.3a 变量与赋值·零基础 ⭐",
                              "link": "/posts/computer/notes/1.3a-变量与赋值-零基础"
                    },
                    {
                              "text": "1.3b 格式化输入输出·零基础 ⭐",
                              "link": "/posts/computer/notes/1.3b-格式化输入输出-零基础"
                    },
                    {
                              "text": "1.4a 选择结构 if·零基础 ⭐",
                              "link": "/posts/computer/notes/1.4a-选择结构-if语句-零基础"
                    },
                    {
                              "text": "1.4b 嵌套 if / switch / 条件表达式·零基础 ⭐",
                              "link": "/posts/computer/notes/1.4b-嵌套if与switch-零基础"
                    },
                    {
                              "text": "1.6 数组",
                              "link": "/posts/computer/notes/1.6-数组"
                    },
                    {
                              "text": "1.6a 数组·零基础 ⭐",
                              "link": "/posts/computer/notes/1.6a-数组-零基础"
                    },
                    {
                              "text": "1.7 函数",
                              "link": "/posts/computer/notes/1.7-函数"
                    },
                    {
                              "text": "1.7a 函数·零基础 ⭐",
                              "link": "/posts/computer/notes/1.7a-函数-零基础"
                    },
                    {
                              "text": "1.8 指针",
                              "link": "/posts/computer/notes/1.8-指针"
                    },
                    {
                              "text": "1.8a 指针·零基础 ⭐",
                              "link": "/posts/computer/notes/1.8a-指针-零基础"
                    },
                    {
                              "text": "鹏哥 C · 指针与二维数组传参",
                              "link": "/posts/computer/notes/pengge-C-指针-二维数组传参"
                    },
                    {
                              "text": "1.9 结构体与共用体",
                              "link": "/posts/computer/notes/1.9-结构体与共用体"
                    },
                    {
                              "text": "1.10 文件操作",
                              "link": "/posts/computer/notes/1.10-文件操作"
                    },
                    {
                              "text": "1.11 程序运行环境与调试",
                              "link": "/posts/computer/notes/1.11-程序运行环境与调试"
                    }
          ],
        },
        {
          text: '数据结构知识点',
          collapsed: false,
          items: [
                    {
                              "text": "2.1 数据结构基本概念",
                              "link": "/posts/computer/notes/2.1-数据结构基本概念"
                    },
                    {
                              "text": "2.2 线性表",
                              "link": "/posts/computer/notes/2.2-线性表"
                    },
                    {
                              "text": "2.3 栈和队列",
                              "link": "/posts/computer/notes/2.3-栈和队列"
                    },
                    {
                              "text": "2.4 串、数组和广义表",
                              "link": "/posts/computer/notes/2.4-串、数组和广义表"
                    },
                    {
                              "text": "2.4a 串与KMP",
                              "link": "/posts/computer/notes/2.4a-串与KMP"
                    },
                    {
                              "text": "2.5 树和二叉树",
                              "link": "/posts/computer/notes/2.5-树和二叉树"
                    },
                    {
                              "text": "2.5a 二叉树遍历与建树模板 🔴",
                              "link": "/posts/computer/notes/2.5a-二叉树遍历与建树模板"
                    },
                    {
                              "text": "2.6 图",
                              "link": "/posts/computer/notes/2.6-图"
                    },
                    {
                              "text": "2.7 查找",
                              "link": "/posts/computer/notes/2.7-查找"
                    },
                    {
                              "text": "2.8 排序",
                              "link": "/posts/computer/notes/2.8-排序"
                    },
                    {
                              "text": "2.9 算法基本概念与分析",
                              "link": "/posts/computer/notes/2.9-算法基本概念与分析"
                    }
          ],
        },
        {
          text: '专项训练（2027）',
          collapsed: false,
          items: [
                    {
                              "text": "3.0 改错题专项训练 ⭐",
                              "link": "/posts/computer/notes/3.0-改错题专项训练"
                    },
                    {
                              "text": "3.1 高频考点强化练习 ⭐",
                              "link": "/posts/computer/notes/3.1-高频考点强化练习"
                    },
                    {
                              "text": "3.2 更多同型练习题",
                              "link": "/posts/computer/notes/3.2-更多同型练习题"
                    },
                    {
                              "text": "3.3 编程题做题策略",
                              "link": "/posts/computer/notes/3.3-编程题做题策略"
                    },
                    {
                              "text": "3.4 循环与数组综合编程专项 🔴",
                              "link": "/posts/computer/notes/3.4-循环与数组综合编程专项"
                    },
                    {
                              "text": "3.5 指针专项（函数/结构体） 🔴",
                              "link": "/posts/computer/notes/3.5-指针专项·指针与函数结构体"
                    },
                    {
                              "text": "3.6 递归与函数设计专项 🔴",
                              "link": "/posts/computer/notes/3.6-递归与函数设计专项"
                    },
                    {
                              "text": "高频错题汇总 ⚠️",
                              "link": "/posts/computer/notes/高频错题汇总"
                    }
          ],
        },
        {
          text: '2024 考点拆分',
          items: [
            { text: '拆分索引', link: '/posts/computer/topics/' },
            { text: '01 C 语言基础', link: '/posts/computer/topics/01-c-basics' },
            { text: '02 数组指针', link: '/posts/computer/topics/02-array-pointer' },
            { text: '03 链表栈队列', link: '/posts/computer/topics/03-list-stack-queue' },
            { text: '04 树图与查找', link: '/posts/computer/topics/04-tree-graph' },
            { text: '05 手写编程', link: '/posts/computer/topics/05-coding' },
          ],
        },
      ],
      '/posts/english/': [
        {
          text: '英语 · 学习笔记',
          items: [
            { text: '📖 学习手册（零基础版）', link: '/posts/english/学习手册' },
            { text: '笔记总览', link: '/posts/english/notes/' },
            { text: '教材目录基准 📗', link: '/posts/english/教材目录基准' },
            { text: "2026 黄金知识汇编 ⭐", link: '/posts/english/2026-黄金知识汇编' },
            { text: "黄金汇编刷题 ✍️", link: '/posts/english/2026-黄金知识汇编-刷题' },
            { text: "考试大纲与题型补强", link: '/posts/english/notes/syllabus' },
            { text: "考试概述与题型分析", link: '/posts/english/notes/overview' },
            { text: "作文模板与高分句型", link: '/posts/english/notes/writing' },
            { text: "完形填空高分技巧", link: '/posts/english/notes/cloze' },
            { text: "短文匹配（五选五）技巧", link: '/posts/english/notes/matching' },
            { text: "历年真题分类与讲解", link: '/posts/english/notes/past-papers-guide' },
            { text: "语法考点精讲", link: '/posts/english/notes/grammar' },
            { text: '📝 主谓一致 · 真题专项', link: '/posts/english/notes/agreement-exercises' },
            { text: "阅读理解高分技巧", link: '/posts/english/notes/reading' },
            { text: "高频词汇速记", link: '/posts/english/notes/vocabulary' },
          ],
        },
        {
          text: '公共英语 · 真题',
          items: [
            { text: '真题总览', link: '/posts/english/' },
            { text: '真题题型对照表 🎯', link: '/posts/english/真题题型对照表' },
            { text: '2026 刷题版 ✍️', link: '/posts/english/2026-英语-刷题版' },
            { text: '2025 刷题版 ✍️', link: '/posts/english/2025-英语-刷题版' },
            { text: '2024 刷题版 ✍️', link: '/posts/english/2024-英语-刷题版' },
            { text: '2023 刷题版 ✍️', link: '/posts/english/2023-英语-刷题版' },
            { text: '2022 刷题版 ✍️', link: '/posts/english/2022-英语-刷题版' },
            { text: '2021 刷题版 ✍️', link: '/posts/english/2021-英语-刷题版' },
            { text: '2020 刷题版 ✍️', link: '/posts/english/2020-英语-刷题版' },
            { text: '2020 精析版 📖', link: '/posts/english/2020-英语-精析版' },
            { text: '2019 刷题版 ✍️', link: '/posts/english/2019-英语-刷题版' },
            { text: '2018 刷题版 ✍️', link: '/posts/english/2018-英语-刷题版' },
            { text: '2017 刷题版 ✍️', link: '/posts/english/2017-英语-刷题版' },
            { text: '2016 刷题版 ✍️', link: '/posts/english/2016-英语-刷题版' },
            { text: '2015 刷题版 ✍️', link: '/posts/english/2015-英语-刷题版' },
            { text: '2014 刷题版 ✍️', link: '/posts/english/2014-英语-刷题版' },
            { text: '2013 刷题版 ✍️', link: '/posts/english/2013-英语-刷题版' },
            { text: '2012 刷题版 ✍️', link: '/posts/english/2012-英语-刷题版' },
            { text: '2011 刷题版 ✍️', link: '/posts/english/2011-英语-刷题版' },
            { text: '2010 刷题版 ✍️', link: '/posts/english/2010-英语-刷题版' },
            { text: '2009 刷题版 ✍️', link: '/posts/english/2009-英语-刷题版' },
            { text: '2008 刷题版 ✍️', link: '/posts/english/2008-英语-刷题版' },
            { text: "高频考点 TOP20 📊", link: '/posts/高频考点/英语-高频考点TOP20' },
            { text: "2025", link: '/posts/english/2025' },
            { text: "2024", link: '/posts/english/2024' },
            { text: "2023", link: '/posts/english/2023' },
            { text: "2022", link: '/posts/english/2022' },
            { text: "2021", link: '/posts/english/2021' },
            { text: "2020", link: '/posts/english/2020' },
            { text: "2019", link: '/posts/english/2019' },
            { text: "2018", link: '/posts/english/2018' },
            { text: "2017", link: '/posts/english/2017' },
            { text: "2016", link: '/posts/english/2016' },
            { text: "2015", link: '/posts/english/2015' },
            { text: "2014", link: '/posts/english/2014' },
            { text: "2013", link: '/posts/english/2013' },
            { text: "2012", link: '/posts/english/2012' },
            { text: "2011", link: '/posts/english/2011' },
            { text: "2010", link: '/posts/english/2010' },
            { text: "2009", link: '/posts/english/2009' },
            { text: "2008", link: '/posts/english/2008' },
            { text: "2007", link: '/posts/english/2007' },
            { text: "2006", link: '/posts/english/2006' },
            { text: "2005", link: '/posts/english/2005' },
          ],
        },
      ],
      '/posts/politics/': [
        {
          text: '政治 · 系统笔记',
          items: [
            { text: '📖 学习手册（零基础版）', link: '/posts/politics/学习手册' },
            { text: '笔记总览', link: '/posts/politics/notes/' },
            { text: '教材目录基准 📗', link: '/posts/politics/教材目录基准' },
            { text: "00 考试大纲与题型", link: '/posts/politics/notes/00-考试大纲与题型' },
            { text: "01 马克思主义中国化时代化", link: '/posts/politics/notes/01-马克思主义中国化时代化' },
            { text: "02 毛泽东思想", link: '/posts/politics/notes/02-毛泽东思想' },
            { text: "03 新民主主义革命", link: '/posts/politics/notes/03-新民主主义革命' },
            { text: "04 社会主义改造", link: '/posts/politics/notes/04-社会主义改造' },
            { text: "05 建设道路初步探索", link: '/posts/politics/notes/05-建设道路初步探索' },
            { text: "06 中国特色社会主义理论体系", link: '/posts/politics/notes/06-中国特色社会主义理论体系' },
            { text: "07 邓小平理论", link: '/posts/politics/notes/07-邓小平理论' },
            { text: "08 三个代表与科学发展观", link: '/posts/politics/notes/08-三个代表与科学发展观' },
            { text: "09 习思想形成与历史地位", link: '/posts/politics/notes/09-习思想形成与历史地位' },
            { text: "10 中国式现代化", link: '/posts/politics/notes/10-中国式现代化' },
            { text: "11 党的领导与以人民为中心", link: '/posts/politics/notes/11-党的领导与以人民为中心' },
            { text: "12 改革发展与五位一体", link: '/posts/politics/notes/12-改革发展与五位一体' },
            { text: "13 民主法治文化民生", link: '/posts/politics/notes/13-民主法治文化民生' },
            { text: "14 生态安全国防统一外交", link: '/posts/politics/notes/14-生态安全国防统一外交' },
            { text: "15 全面从严治党", link: '/posts/politics/notes/15-全面从严治党' },
            { text: "16 时事政治备考", link: '/posts/politics/notes/16-时事政治备考' },
            { text: "17 辨析论述材料题模板", link: '/posts/politics/notes/17-辨析论述材料题模板' },
            { text: "18 必背金句与名词", link: '/posts/politics/notes/18-必背金句与名词' },
            { text: '冲刺资料 · 2025 欢姐大题笔记', link: '/posts/politics/冲刺资料-2025欢姐政治大题笔记' },
            { text: '冲刺资料 · 2026 欢姐大题笔记', link: '/posts/politics/冲刺资料-2026欢姐政治大题笔记' },
          ],
        },
        {
          text: '政治 · 真题演练',
          items: [
            { text: '真题总览', link: '/posts/politics/' },
            { text: '真题章节对照表 🎯', link: '/posts/politics/真题章节对照表' },
            { text: '2020 刷题版 ✍️', link: '/posts/politics/2020-政治-刷题版' },
            { text: '高频考点 TOP20 📊', link: '/posts/高频考点/政治-高频考点TOP20' },
            { text: '2020 原卷文字版 📄', link: '/posts/politics/2020-原卷文字版' },
            { text: '2026', link: '/posts/politics/2026' },
            { text: '2025', link: '/posts/politics/2025' },
            { text: '2024', link: '/posts/politics/2024' },
            { text: '2023', link: '/posts/politics/2023' },
            { text: '2022', link: '/posts/politics/2022' },
            { text: '2022 政治大题通关手册 📕', link: '/posts/politics/2022-政治大题通关手册' },
            { text: '2021', link: '/posts/politics/2021' },
            { text: '2020', link: '/posts/politics/2020' },
            { text: '2019', link: '/posts/politics/2019' },
            { text: '2018', link: '/posts/politics/2018' },
            { text: '真题 · 政治历年 2012–2019', link: '/posts/politics/notes/真题-政治历年2012-2019' },
          ],
        },
      ],
      '/guide/': [
        {
          text: '考情速查',
          items: [
            { text: '🎯 四科备考总纲（500 分全景）', link: '/guide/四科备考总纲' },
            { text: '🎯 0 基础总入口', link: '/guide/零基础总入口' },
            { text: '🎓 0基础学习路线', link: '/guide/零基础学习路线' },
            { text: '📋 考纲覆盖 × 练习对照表', link: '/guide/考纲覆盖与练习对照表' },
            { text: '📖 2026 考纲全解', link: '/guide/2026考纲全解' },
            { text: '📗 官方教材对照教程', link: '/guide/官方教材对照教程' },
            { text: '💻 计算机零基础课程大纲', link: '/guide/计算机零基础课程大纲' },
            { text: '💻 计算机专业报考', link: '/guide/计算机专业-报考指南' },
            { text: '📊 投档与招生数据', link: '/guide/投档与招生数据' },
            { text: '🎯 公办院校与录取', link: '/guide/公办院校与录取' },
            { text: '📊 2026 省控线', link: '/guide/省控线-录取分数线' },
            { text: '🎬 B站吸收规划（总纲）', link: '/guide/bili-plan/' },
            { text: '　└ 💻 计算机 200分', link: '/guide/bili-plan/computer' },
            { text: '　└ 📐 高等数学 100分', link: '/guide/bili-plan/math' },
            { text: '　└ 🏛️ 政治理论 100分', link: '/guide/bili-plan/politics' },
            { text: '　└ 🇬🇧 英语 100分', link: '/guide/bili-plan/english' },
            { text: '🎬 B站学习资源', link: '/guide/bili-resources' },
            { text: '🎬 B站学习资源库（速查表）', link: '/guide/B站学习资源库' },
            { text: '🎥 考纲↔视频对照', link: '/guide/video-ka-map' },
          ],
        },
        {
          text: '🗺️ 知识地图（字幕提炼）',
          items: [
            { text: '总览与可信度说明', link: '/guide/knowledge-map/' },
            { text: '💻 计算机 · 基础与 Office', link: '/guide/knowledge-map/computer/basics' },
            { text: '　└ C 语言基础', link: '/guide/knowledge-map/computer/c-language' },
            { text: '　└ C 语言进阶与工程', link: '/guide/knowledge-map/computer/c-advanced' },
            { text: '　└ 数据结构与真题题型', link: '/guide/knowledge-map/computer/data-structures' },
            { text: '📐 高数 · 极限导数微分学', link: '/guide/knowledge-map/math/limits-derivatives' },
            { text: '　└ 积分与微分方程', link: '/guide/knowledge-map/math/integrals' },
            { text: '　└ 多元·级数·线代·证明', link: '/guide/knowledge-map/math/advanced' },
            { text: '🇬🇧 英语 · 语法与题型', link: '/guide/knowledge-map/english' },
          ],
        },
        {
          text: '使用说明',
          items: [
            { text: '站点说明', link: '/guide/' },
            { text: '资料边界', link: '/guide/sources' },
            // ⚠️ 别把 '/guide/bili-scraping' 加回来：它在上面 srcExclude 里，
            //    页面不进构建 ⇒ 挂在这里就是 404。文件仍在仓库里（用编辑器看）。
            //    2026-09-21 由 check-links.mjs 新增的 srcExclude 检查抓出。
            { text: '🧰 B站/抖音解析项目调研', link: '/guide/bili-mcp-projects' },
            { text: '🧾 仓库完整性审计（168 文件）', link: '/guide/仓库完整性审计-2026-09-21' },
          ],
        },
        {
          text: '📚 备考资料',
          items: [
            { text: '📚 题库总入口（6 个题库）', link: '/posts/题库/' },
            { text: '🖥️ 计算机真题刷题（133 题·可交互）', link: '/posts/题库/计算机真题刷题' },
            { text: '✍️ 计算机手写题（30 题·填空/简答/计算/应用）', link: '/posts/题库/计算机手写题' },
            { text: '🧪 模拟卷总入口（11 套）', link: '/posts/模拟卷/' },
            { text: '🗺️ 考点资源图谱（计算机）', link: '/posts/resources/考点资源图谱-计算机' },
            { text: '考试概况与科目结构', link: '/posts/resources/考试概况与科目结构' },
            { text: '官方教材与参考书清单', link: '/posts/resources/官方教材与参考书清单' },
            { text: '零基础学习路线图', link: '/posts/resources/零基础学习路线图' },
            { text: '考纲↔本库对照导航', link: '/posts/resources/考纲与本库对照导航' },
            { text: '科学学习方法', link: '/posts/resources/科学学习方法' },
            { text: '每日备考打卡表', link: '/posts/resources/每日备考打卡表' },
            { text: '错题记录模板 📝', link: '/posts/resources/错题记录模板' },
            { text: '开源学习工具推荐 🧰', link: '/posts/resources/开源学习工具推荐' },
          ],
        },
      ],
      // 题库自成一段：这 7 页此前不属于任何 sidebar 键 ⇒ 打开后没有侧栏，只能在页内互相跳。
      // 加了这个键，6 个题库之间可以随时切换。
      '/posts/题库/': [
        {
          text: '📚 题库总入口',
          items: [
            { text: '全部题库一览（398 题）', link: '/posts/题库/' },
          ],
        },
        {
          text: '计算机',
          items: [
            { text: '🖥️ 真题刷题 133 题 · 可交互', link: '/posts/题库/计算机真题刷题' },
            { text: '✍️ 手写题 30 题 · 填空/简答/计算/应用', link: '/posts/题库/计算机手写题' },
            { text: '📝 高频简答题 45 题', link: '/posts/题库/高频简答题库' },
          ],
        },
        {
          text: '数学',
          items: [
            { text: '🔢 计算题专项训练 50 题', link: '/posts/题库/高数计算题专项训练' },
            { text: '🌱 零基础扫盲 40 题 · 符号读法', link: '/posts/题库/零基础扫盲题库' },
          ],
        },
        {
          text: '政治',
          items: [
            { text: '🏛️ 选择题 100 题', link: '/posts/题库/政治选择题题库' },
          ],
        },
        {
          text: '使用方式',
          items: [
            { text: '🗺️ 计算机考点资源图谱', link: '/posts/resources/考点资源图谱-计算机' },
          ],
        },
      ],
      // 模拟卷 / 高频考点 / 备考资料 三个目录此前没有 sidebar 键 ⇒
      // 打开后左侧栏空白，无法在同类页面间切换。2026-09-22 补齐（沿用题库键的修法）。
      '/posts/模拟卷/': [
        {
          text: '🧪 模拟卷总入口',
          items: [
            { text: '总览（11 套 · 自编）', link: '/posts/模拟卷/' },
          ],
        },
        {
          text: '高数',
          items: [
            { text: '卷一 · 基础巩固', link: '/posts/math/模拟卷/卷一-基础巩固卷' },

            { text: '📄 卷一 · 基础巩固 · 答案', link: '/posts/math/模拟卷/卷一-基础巩固卷-答案' },
            { text: '卷二 · 综合中档', link: '/posts/math/模拟卷/卷二-综合中档卷' },

            { text: '📄 卷二 · 综合中档 · 答案', link: '/posts/math/模拟卷/卷二-综合中档卷-答案' },
            { text: '卷三 · 拔高冲刺', link: '/posts/math/模拟卷/卷三-拔高冲刺卷' },

            { text: '📄 卷三 · 拔高冲刺 · 答案', link: '/posts/math/模拟卷/卷三-拔高冲刺卷-答案' },
          ],
        },
        {
          text: '计算机',
          items: [
            { text: '卷一 · 基础巩固', link: '/posts/computer/模拟卷/卷一-基础巩固卷' },

            { text: '📄 卷一 · 基础巩固 · 答案', link: '/posts/computer/模拟卷/卷一-基础巩固卷-答案' },
            { text: '卷二 · 综合中档', link: '/posts/computer/模拟卷/卷二-综合中档卷' },

            { text: '📄 卷二 · 综合中档 · 答案', link: '/posts/computer/模拟卷/卷二-综合中档卷-答案' },
            { text: '卷三 · 拔高冲刺', link: '/posts/computer/模拟卷/卷三-拔高冲刺卷' },

            { text: '📄 卷三 · 拔高冲刺 · 答案', link: '/posts/computer/模拟卷/卷三-拔高冲刺卷-答案' },
          ],
        },
        {
          text: '政治',
          items: [
            { text: '卷一 · 基础巩固', link: '/posts/politics/模拟卷/卷一-基础巩固卷' },

            { text: '📄 卷一 · 基础巩固 · 答案', link: '/posts/politics/模拟卷/卷一-基础巩固卷-答案' },
            { text: '卷二 · 综合中档', link: '/posts/politics/模拟卷/卷二-综合中档卷' },

            { text: '📄 卷二 · 综合中档 · 答案', link: '/posts/politics/模拟卷/卷二-综合中档卷-答案' },
            { text: '卷三 · 拔高冲刺', link: '/posts/politics/模拟卷/卷三-拔高冲刺卷' },

            { text: '📄 卷三 · 拔高冲刺 · 答案', link: '/posts/politics/模拟卷/卷三-拔高冲刺卷-答案' },
          ],
        },
        {
          text: '英语',
          items: [
            { text: '卷二 · 综合中档', link: '/posts/english/模拟卷/卷二-综合中档卷' },

            { text: '📄 卷二 · 综合中档 · 答案', link: '/posts/english/模拟卷/卷二-综合中档卷-答案' },
            { text: '卷三 · 拔高冲刺', link: '/posts/english/模拟卷/卷三-拔高冲刺卷' },

            { text: '📄 卷三 · 拔高冲刺 · 答案', link: '/posts/english/模拟卷/卷三-拔高冲刺卷-答案' },
          ],
        },
      ],
      '/posts/高频考点/': [
        {
          text: '📊 高频考点',
          items: [
            { text: '总览', link: '/posts/高频考点/' },
            { text: '★ 真题考点总析（2018–2026）', link: '/posts/高频考点/真题考点总析' },
            { text: '计算机 TOP20（已归档）', link: '/posts/高频考点/计算机-高频考点TOP20' },
            { text: '政治 TOP20（已归档）', link: '/posts/高频考点/政治-高频考点TOP20' },
            { text: '高数 TOP20（已归档）', link: '/posts/高频考点/高数-高频考点TOP20' },
            { text: '英语 TOP20（已归档）', link: '/posts/高频考点/英语-高频考点TOP20' },
          ],
        },
      ],
      '/posts/resources/': [
        {
          text: '📚 备考资料',
          items: [
            { text: '考试概况与科目结构', link: '/posts/resources/考试概况与科目结构' },
            { text: '官方教材与参考书清单', link: '/posts/resources/官方教材与参考书清单' },
            { text: '零基础学习路线图', link: '/posts/resources/零基础学习路线图' },
            { text: '考纲↔本库对照导航', link: '/posts/resources/考纲与本库对照导航' },
            { text: '🗺️ 考点资源图谱（计算机）', link: '/posts/resources/考点资源图谱-计算机' },
            { text: '科学学习方法', link: '/posts/resources/科学学习方法' },
            { text: '每日备考打卡表', link: '/posts/resources/每日备考打卡表' },
            { text: '错题记录模板 📝', link: '/posts/resources/错题记录模板' },
            { text: '开源学习工具推荐 🧰', link: '/posts/resources/开源学习工具推荐' },
            { text: '外部资源索引', link: '/posts/resources/外部资源索引' },
          ],
        },
      ],
    },
    socialLinks: [
      {
        icon: 'github',
        link: 'https://github.com/wpc725562-dotcom/darling016123',
      },
    ],
    footer: {
      message: '仅供个人学习 · 考生回忆版 · 非考试院原卷',
      copyright: '内容整理自公开回忆版与个人 Obsidian 笔记',
    },
    docFooter: {
      prev: '上一篇',
      next: '下一篇',
    },
    lastUpdatedText: '最后更新',
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切到浅色',
    darkModeSwitchTitle: '切到深色',
  },
})
