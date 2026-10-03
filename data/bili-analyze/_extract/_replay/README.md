# 画面补录 · 重放清单（REPLAY.md）

> **这个目录是干什么的**：知识地图里的「画面补录」条目，是把 B 站视频**画面抽帧 + OCR**
> 得到的内容合进地图的。抽帧/OCR 很贵（67 个分P ≈ 2 GB 视频 + 4,564 帧 ≈ 半小时以上），
> 而合并脚本 `merge_asr_into_map.py` **依赖这里的 `_add-*.md` 作为唯一输入**。
>
> **2026-10-03 补建**。此前这些文件只存在于 WorkBuddy 的本地工作区
> `D:\WorkBuddy\2026-09-24-18-32-54\out\frames2\`，**两个仓库都不管**。
> 一旦本地工作区被清（它占了 2.5 GB，迟早要清），**整条画面补录链路就断了**：
> 无法审计「哪条内容来自哪个视频」，也无法重放。

---

## 为什么必须留（真实事故教训）

2026-09-26 出过一次严重事故：给 `merge_asr_into_map.py` 加 `--map` 参数时，
只改了「读」、忘了改「写」，三次调用（computer / math / english）**全部写进了默认的
`english-gaokao.md`**，把 269 章 / 2,582 条的高考英语地图**冲成了 16 章 / 115 条**。

能恢复，**只因为两件事同时成立**：

1. 碰巧有一份 `english-gaokao.pre-asr.bak`；
2. 那 5 轮合并**可确定重放** —— 但当时是**凭记忆**重放的，中途漏过一轮
   （总数从 2,582 掉到 2,532 才发现）。

**教训：可重放 = 退路。但「凭记忆重放」不是可重放。** 这份清单就是为了把记忆换成文件。

---

## 目录结构

```
_replay/
├── README.md（本文件）
├── _add-screen.md              ← 归档版（合并后完整版）
├── _add-screen-zero.md
├── _add-screen-wx.md
├── _add-screen-wt.md
├── _add-screen-zsb-computer.md
├── _add-screen-zsb-math.md
├── _add-screen-zsb-english.md
├── fragments/                  ← 分片版（提炼子代理的原始输出，33 份）
│   └── _add-screen-{p1p2,p3p4,...,zero-p1p2,...,wt-p1p4,...}.md
└── screens/                    ← 画面清单（OCR 后按帧去重整理，62 份）
    └── <BV>_p<NN>/_screen.md
```

- **`_add-*.md`（根目录）** = 实际喂给 `merge_asr_into_map.py --add` 的文件。
  **重放只需要这 7 份。**
- **`fragments/`** = 每批视频的提炼子代理各自产出的小文件，被 `cat` 拼成上面的归档版。
  留它是为了**溯源**：某条内容出自哪个分P，能在这一层看到。
- **`screens/`** = `build_screen_digest.py` 的输出。留着可以**不重跑 OCR** 就重新提炼
  （OCR 是整条链路最贵的一步）。

---

## 重放矩阵（★ 权威版：哪份文件 → 哪张图 → 什么参数）

命令模板（在 `D:\WorkBuddy\2026-09-24-18-32-54\` 下跑）：

```bash
python scripts/merge_asr_into_map.py \
  --map   "D:/deeepseek/zhuan-sheng-ben-notes/data/bili-analyze/_extract/_subject/<图>.md" \
  --add   "<本目录>/<增补文件>" \
  --prefix "<前缀>" \
  [--dry-run]
```

### 高考英语（目标图：`english-gaokao.md`）

| # | 增补文件 | prefix | 产出 |
|:-:|:---|:---|:---|
| 1 | `_add-screen.md` | `画面补录 · ` | 语法完形第一阶段 +50 条 |
| 2 | `_add-screen-zero.md` | `画面补录 · ` | 零基础训练 20 讲 +92 条 |
| 3 | `_add-screen-wx.md` | `画面补录 · ` | 完形综述 +69 条 |
| 4 | `_add-screen-wt.md` | `画面补录 · ` | 应用文写作 +22 条 |

> **顺序必须按上表**。这 4 批是把 `english-gaokao.md` 从 194 章 / 2,257 条
> （`out/english-gaokao.pre-asr.bak`）一路推到 269 章 / 2,582 条的完整链条。
> 逐轮数字：**2349 → 2399 → 2491 → 2560 → 2582**。
> ⚠️ 上面第 1–4 轮对应 2349/2399/2491/2560 的中间态；**2,582 是含 ASR 补录的最终值**，
> 重放画面这批时应先有 ASR 那几轮（见下方「ASR 部分」）。

### 专升本三份图

| # | 增补文件 | 目标图 | prefix | 产出 |
|:-:|:---|:---|:---|:---|
| 5 | `_add-screen-zsb-computer.md` | `computer.md` | **`""`（空）** | 557 → **561** · 一灯老师 4 条 |
| 6 | `_add-screen-zsb-math.md` | `math.md` | **`""`（空）** | 927 → **931** · 帆哥老师 4 条 |
| 7 | `_add-screen-zsb-english.md` | `english.md` | **`""`（空）** | 106 → **115** · 易易 + 乐贯中西 9 条 |

> **★★★ `--prefix ""` 与高考英语不同，这一点极易踩错。**
> 专升本三份图的章名形如 `补充（帆哥）· 真题难度与命题规律（画面）`
> —— **`·` 后面直接是章名，中间没有 `画面补录 · `**。
> 若误用 `--prefix "画面补录 · "` 重放，脚本会拼出
> `补充（帆哥）· 画面补录 · 真题难度与命题规律（画面）` 这个**图上不存在的章名**，
> 于是判成「新章」⇒ **整章内容被重复插一遍**。
>
> **2026-10-03 已给脚本加了防护**（`have_essence` 前缀无关索引）：现在两种 prefix
> 都会正确识别为「已存在」。但**记录在案的权威参数仍是 `--prefix ""`** ——
> 恢复历史状态时要复现当时的写法。

---

## ASR 部分（字幕补录，与画面补录是两条独立线）

ASR 那批的增补文件在 `D:\WorkBuddy\2026-09-24-18-32-54\out\asr\`：

```
_add-asr.md                      _add-asr-核心词汇1.md
_add-asr-一轮下册高阶阅读.md       _add-asr-核心词汇1-v2.md
_add-asr-应用文-v2.md             _add-asr-核心词汇2.md
_add-asr-应用文语法完形.md         _add-asr-真题讲解.md
```

它们的 prefix 是 `ASR 补录 · `，目标图同样是 `english-gaokao.md`。
**⚠️ 这 8 份尚未归档进本目录**（2026-10-03 只处理了画面线）。
若要彻底断掉「凭记忆重放」的风险，应同样拷进来并补全顺序表。

---

## 复现验证（做完重放后跑这几条）

```bash
cd D:/deeepseek/zhuan-sheng-ben-notes

# ① 幂等：同一批重跑必须报「没有新章节」
python ../2026-09-24-18-32-54/scripts/merge_asr_into_map.py \
  --map data/bili-analyze/_extract/_subject/math.md \
  --add <本目录>/_add-screen-zsb-math.md --prefix "" --dry-run
# 期望：没有新章节（全部已存在，幂等）

# ② 章数/条数核对
for f in computer math english english-gaokao; do
  printf "%-16s 章=%s 条=%s\n" "$f" \
    "$(grep -c '^## ' data/bili-analyze/_extract/_subject/$f.md)" \
    "$(grep -c '^- \*\*要点\*\*' data/bili-analyze/_extract/_subject/$f.md)"
done
# 期望：computer 73/561 · math 58/931 · english 16/115 · english-gaokao 269/2582
#       （2026-10-03 实测值）
```

> 注：上面「条数」的准确口径以 `_subject/*.md` 中 `- **要点**` 行数为准 ——
> README 与 memory 里历次记录的 561/1607 等数字用的是**页面侧**口径
> （`docs/guide/knowledge-map/*/`），两者差在「同一知识点在多个主题下重复计数」，
> **不是不一致**。核对时先确认口径。

---

## 维护约定

1. **新增画面补录批次时，必须同步更新本文件的「重放矩阵」** —— 加一行：
   文件 / 目标图 / prefix / 产出条数。
2. **`--prefix` 必须显式记录**，不要依赖「反正能跑通」。专升本那次就是空 prefix。
3. **不要删本目录**（2.4 MB）。要删必须先确认：地图里的内容已提交进 git
   （`data/bili-analyze/_extract/_subject/*.md` 在版本控制内）。
