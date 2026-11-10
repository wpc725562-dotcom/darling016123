"""高数第11章（曲线积分）字幕蒸馏：BV1Up4y1Y76a p133-p136 -> 考点笔记

字幕是纯口播文字，无标点、无公式排版，全部靠模型还原为 LaTeX 契约格式。
单分P一请求，串行重试；大批量单请求会触发网关 502。
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path("D:/deeepseek/zhuan-sheng-ben-notes/data/bili-analyze/BV1Up4y1Y76a")
OUT_DIR = Path("D:/deeepseek/zhuan-sheng-ben-notes/scripts")

GATEWAY = "http://127.0.0.1:18899/v1/chat/completions"
TOKEN = "ofm-opwWQtmqjdxQvhFGM66N0tqQKW8FEDE2"
MODEL = "nvidia/nemotron-3.5-super-vl:free"

# 分P -> (考点编号, 考点名, 题型, 考频)
PARTS = {
    "p133": ("G11-2", "曲线积分的概念与两类积分的区别", "单选、填空、判断", "★★★☆☆"),
    "p134": ("G11-3", "曲线积分的计算——直接代入法", "计算", "★★★★★"),
    "p135": ("G11-4", "格林公式及其应用", "计算、证明", "★★★★★"),
    "p136": ("G11-5", "曲线积分与路径无关", "计算、判断", "★★★★☆"),
}

PROMPT_TMPL = """你是《高等数学》专升本电子书蒸馏工程的执行者。任务：把网课口播字幕整理成一篇考点笔记。

要求：
1. 字幕是语音识别的原始文字，没有标点、公式全靠口述。你必须还原成规范的数学表述。
2. 所有数学公式必须用 LaTeX 行内 $...$ 或独立 $$...$$ 表示，不许写成纯文本。
3. 忠实原视频讲法：老师强调的步骤、口诀、例题数字、易错点必须保留，不许替换成通用教材说法。
4. 老师没讲的内容不要编。若某个必要环节视频未展开，在对应位置写「（视频未展开）」。
5. 严格按下面的模板输出，不要加任何前后缀说明、不要写"好的以下是"之类的话。

【课程】04-高数
【章节】第11章　曲线积分与曲面积分
【节】第11章 {kp} {name}
【考点】{kp}　{name}
【考频】{freq}
【题型】{qtype}
============================================================

> **学科系统**：（一句话说明这个考点在高数体系里的位置）
> **秒杀类比**：（一句生活化类比，帮助秒记核心思想）

## 一、 核心知识解构

（主体部分。按视频讲解顺序展开，每个知识点用 ### 小标题。
定义、定理、公式全部 LaTeX 化。视频里出现的每道例题都要写出来：
题目原文 -> 解题步骤 -> 最终答案，公式化呈现。一条不许漏。）

## 二、 考试红牌警告与秒杀秘籍

* 🚨 **易错雷区**：（具体到公式或步骤层面，写清楚错在哪）
* 🔑 **秒杀秘籍**：（看到什么特征就走什么套路）

（红牌 3-5 条，秘籍 3-5 条）

## 三、 闭卷真题挑战

> **【真题演练】**：（依据视频讲解的题型，出一道同类型新题，难度对齐真题）

【答案与解析】
**【正确答案】**：
（完整解题过程，LaTeX 公式）

**【核心解析】**：
（点明这题考的是哪个套路）

（出 2 道）

============================================================
【原文锚点】第11章 {kp}"{name}"（BV1Up4y1Y76a 字幕 {part}，网课口播）
【来源】网课字幕蒸馏，非讲义原文；讲义第11章仅53行，本节为补齐内容

========== 字幕原文（语音识别，无标点） ==========
{raw}
========== 结束 ==========

请直接输出考点笔记正文，完整输出全部小节，不要截断：
"""


def call_model(prompt: str, max_tokens: int = 24000) -> dict:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    req = urllib.request.Request(
        GATEWAY,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def distill(part: str, kp: str, name: str, qtype: str, freq: str) -> bool:
    raw_path = BASE / f"subtitle_{part}.txt"
    if not raw_path.exists():
        print(f"[{part}] 字幕缺失: {raw_path}")
        return False

    raw = raw_path.read_text(encoding="utf-8", errors="replace")
    prompt = PROMPT_TMPL.format(
        kp=kp, name=name, qtype=qtype, freq=freq, part=part, raw=raw
    )

    for attempt in range(5):
        try:
            data = call_model(prompt)
            choice = data["choices"][0]
            content = choice["message"]["content"]
            usage = data.get("usage", {})
            finish = choice.get("finish_reason")

            if finish == "length":
                print(f"[{part}] 警告：输出被截断 (finish_reason=length)")

            out = OUT_DIR / f"_gs_{part}_{kp}.txt"
            out.write_text(content, encoding="utf-8")
            print(
                f"[{part}] OK {kp} | {len(content)} 字符 | "
                f"prompt={usage.get('prompt_tokens')} completion={usage.get('completion_tokens')} "
                f"reasoning={usage.get('completion_tokens_details', {}).get('reasoning_tokens')} "
                f"finish={finish} -> {out.name}"
            )
            return True
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:200]
            print(f"[{part}] [{attempt + 1}/5] HTTP {e.code}: {body}")
            time.sleep(5)
        except Exception as e:
            print(f"[{part}] [{attempt + 1}/5] {type(e).__name__}: {e}")
            time.sleep(5)

    print(f"[{part}] 全部重试失败")
    return False


def main() -> int:
    targets = sys.argv[1:] or list(PARTS)
    ok = 0
    for part in targets:
        kp, name, qtype, freq = PARTS[part]
        if distill(part, kp, name, qtype, freq):
            ok += 1
    print(f"完成 {ok}/{len(targets)}")
    return 0 if ok == len(targets) else 1


if __name__ == "__main__":
    sys.exit(main())
