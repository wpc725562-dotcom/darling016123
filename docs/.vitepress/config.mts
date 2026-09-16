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
      {
        text: '高数',
        items: [
          { text: '📖 学习手册 ⭐', link: '/posts/math/学习手册' },
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
          { text: '📊 真题考频矩阵 ⭐', link: '/guide/真题考频矩阵' },
          { text: '✍️ 专项题库', link: '/posts/computer/专项题库/' },
          { text: '知识点', link: '/posts/computer/notes/' },
          { text: '2024 全卷', link: '/posts/computer/2024' },
          { text: '考点拆分', link: '/posts/computer/topics/' },
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
      { text: '🎓 学习路线', link: '/guide/零基础学习路线' },
      {
        text: '🇯🇵 日语',
        items: [
          { text: '学习路线', link: '/learn/' },
          { text: '🎯 零基础五十音入门', link: '/learn/zero-baseline' },
          { text: '标日手册总目录', link: '/learn/standard-japanese/' },
          { text: '动词形容词变形总览', link: '/learn/standard-japanese/conjugation-guide' },
          { text: '🎯 易混淆语法对比表', link: '/learn/standard-japanese/grammar-comparison' },
          { text: '初级篇 1-48 课', link: '/learn/standard-japanese/elementary' },
          { text: '中级篇 1-32 课', link: '/learn/standard-japanese/intermediate' },
          { text: '高级篇 1-24 课', link: '/learn/standard-japanese/advanced' },
          { text: '从零开始学日语 📖', link: '/learn/systematic-japanese-learning-guide' },
        ],
      },
      { text: '🎬 B站资源', link: '/guide/bili-resources' },
      { text: '使用说明', link: '/guide/' },
      { text: '🎯 公办院校', link: '/guide/公办院校与录取' },
      { text: '💻 计算机报考', link: '/guide/计算机专业-报考指南' },
      { text: '📊 投档招生', link: '/guide/投档与招生数据' },
      { text: '📈 2026 省控线', link: '/guide/省控线-录取分数线' },
      {
        text: '📊 高频考点',
        items: [
          { text: '总览', link: '/posts/高频考点/' },
          { text: '计算机 TOP20', link: '/posts/高频考点/计算机-高频考点TOP20' },
          { text: '政治 TOP20', link: '/posts/高频考点/政治-高频考点TOP20' },
          { text: '高数 TOP20', link: '/posts/高频考点/高数-高频考点TOP20' },
          { text: '英语 TOP20', link: '/posts/高频考点/英语-高频考点TOP20' },
        ],
      },
      {
        text: 'GitHub',
        link: 'https://github.com/wpc725562-dotcom/darling016123',
      },
    ],
    sidebar: {
      '/learn/': [
        {
          text: '🇯🇵 日语学习',
          items: [
            { text: '学习路线', link: '/learn/' },
            { text: '🎯 零基础五十音入门', link: '/learn/zero-baseline' },
            { text: '从零开始学日语 📖', link: '/learn/systematic-japanese-learning-guide' },
          ],
        },
        {
          text: '标日同步手册',
          items: [
            { text: '三卷总目录', link: '/learn/standard-japanese/' },
            { text: '词类与变形总览', link: '/learn/standard-japanese/conjugation-guide' },
            { text: '🎯 易混淆语法对比表', link: '/learn/standard-japanese/grammar-comparison' },
            { text: '第一卷：初级篇', link: '/learn/standard-japanese/elementary' },
            { text: '第二卷：中级篇', link: '/learn/standard-japanese/intermediate' },
            { text: '第三卷：高级篇', link: '/learn/standard-japanese/advanced' },
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
                              "text": "2025 回忆版 📷",
                              "link": "/posts/math/2025"
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
          text: "笔记 · 一章 函数与极限",
          collapsed: true,
          items: [
                    {
                              "text": "1.1 函数的概念",
                              "link": "/posts/math/notes/1.1-函数的概念"
                    },
                    {
                              "text": "1.1 左右极限与极限存在判定",
                              "link": "/posts/math/notes/1.1-左右极限与极限存在判定"
                    },
                    {
                              "text": "1.2 函数的连续性与间断点分类",
                              "link": "/posts/math/notes/1.2-函数的连续性与间断点分类"
                    },
                    {
                              "text": "1.3 函数的连续性",
                              "link": "/posts/math/notes/1.3-函数的连续性"
                    },
                    {
                              "text": "1.3 极限界限之“抓大头”法则",
                              "link": "/posts/math/notes/1.3-极限界限之“抓大头”法则"
                    },
                    {
                              "text": "1.4 等价无穷小替换原理",
                              "link": "/posts/math/notes/1.4-等价无穷小替换原理"
                    },
                    {
                              "text": "1.5 闭区间上连续函数的性质",
                              "link": "/posts/math/notes/1.5-闭区间上连续函数的性质"
                    },
                    {
                              "text": "1.10 极限计算三法决策树 ⭐",
                              "link": "/posts/math/notes/1.10-极限计算三法决策树"
                    },
                    {
                              "text": "1.11 极限求值零基础·抓大头 ⭐",
                              "link": "/posts/math/notes/1.11-极限求值零基础-抓大头"
                    }
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
                    }
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
                    }
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
                              "text": "📊 真题考频矩阵 ⭐",
                              "link": "/guide/真题考频矩阵"
                    },
                    {
                              "text": "✍️ 专项题库（按考频排序）",
                              "link": "/posts/computer/专项题库/"
                    },
                    {
                              "text": "真题章节对照表 🎯",
                              "link": "/posts/computer/真题章节对照表"
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
                              "text": "1.6 数组",
                              "link": "/posts/computer/notes/1.6-数组"
                    },
                    {
                              "text": "1.7 函数",
                              "link": "/posts/computer/notes/1.7-函数"
                    },
                    {
                              "text": "1.8 指针",
                              "link": "/posts/computer/notes/1.8-指针"
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
            { text: "阅读理解高分技巧", link: '/posts/english/notes/reading' },
            { text: "高频词汇速记", link: '/posts/english/notes/vocabulary' },
          ],
        },
        {
          text: '公共英语 · 真题',
          items: [
            { text: '真题总览', link: '/posts/english/' },
            { text: '真题题型对照表 🎯', link: '/posts/english/真题题型对照表' },
            { text: '2024 刷题版 ✍️', link: '/posts/english/2024-英语-刷题版' },
            { text: '2023 刷题版 ✍️', link: '/posts/english/2023-英语-刷题版' },
            { text: '2022 刷题版 ✍️', link: '/posts/english/2022-英语-刷题版' },
            { text: '2021 刷题版 ✍️', link: '/posts/english/2021-英语-刷题版' },
            { text: '2020 刷题版 ✍️', link: '/posts/english/2020-英语-刷题版' },
            { text: '2020 精析版 📖', link: '/posts/english/2020-英语-精析版' },
            { text: '2019 刷题版 ✍️', link: '/posts/english/2019-英语-刷题版' },
            { text: "高频考点 TOP20 📊", link: '/posts/高频考点/英语-高频考点TOP20' },
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
            { text: '2024', link: '/posts/politics/2024' },
            { text: '2023', link: '/posts/politics/2023' },
            { text: '2022', link: '/posts/politics/2022' },
            { text: '2021', link: '/posts/politics/2021' },
            { text: '2020', link: '/posts/politics/2020' },
            { text: '2019', link: '/posts/politics/2019' },
            { text: '2018', link: '/posts/politics/2018' },
          ],
        },
      ],
      '/guide/': [
        {
          text: '考情速查',
          items: [
            { text: '🎓 0基础学习路线', link: '/guide/零基础学习路线' },
            { text: '📊 真题考频矩阵 ⭐', link: '/guide/真题考频矩阵' },
            { text: '💻 计算机专业报考', link: '/guide/计算机专业-报考指南' },
            { text: '📊 投档与招生数据', link: '/guide/投档与招生数据' },
            { text: '🎯 公办院校与录取', link: '/guide/公办院校与录取' },
            { text: '📊 2026 省控线', link: '/guide/省控线-录取分数线' },
            { text: '🎬 B站学习资源', link: '/guide/bili-resources' },
            { text: '🎥 考纲↔视频对照', link: '/guide/video-ka-map' },
          ],
        },
        {
          text: '使用说明',
          items: [
            { text: '站点说明', link: '/guide/' },
            { text: '资料边界', link: '/guide/sources' },
            { text: '📚 学习博客借鉴清单', link: '/guide/学习博客借鉴' },
          ],
        },
        {
          text: '📚 备考资料',
          items: [
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
