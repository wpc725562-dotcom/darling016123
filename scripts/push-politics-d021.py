# -*- coding: utf-8 -*-
"""把 D021 学的政治 00-1-4 推进 Anki（专升本::政治::A级64篇默写）"""
import json
import urllib.request

API = "http://127.0.0.1:8765"
DECK = "专升本::政治::A级64篇默写"
MODEL = "问答题"
TAGS = ["D021", "00-1-4", "政治"]


def call(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(API, payload, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


CARDS = [
    ("毛 00-1-4 五大理论成果｜按顺序全列",
     "① <b>毛泽东思想</b>　② <b>邓小平理论</b>　③ <b>「三个代表」重要思想</b>"
     "　④ <b>科学发展观</b>　⑤ <b>习近平新时代中国特色社会主义思想</b><br>"
     "口诀：<b>毛邓三科习</b>"),

    ("毛 00-1-4 四块牌子｜四大成果各自的定位",
     "邓小平理论 → <b>开篇之作</b><br>"
     "「三个代表」→ 推动中特理论体系的<b>跨世纪发展</b><br>"
     "科学发展观 → 实现中特理论体系在<b>新世纪新阶段的新发展</b><br>"
     "习新时代 → 中特理论体系的<b>新篇章</b>"),

    ("毛 00-1-4 毛泽东思想和中特理论体系是什么关系？",
     "<b>不属于。</b>中国特色社会主义理论体系<b>从邓小平开始算</b>，"
     "毛泽东思想<b>在体系门外</b>。<br>"
     "⚠️ 这是最容易错的一题：毛是「基础/准备」，不是「体系成员」。"),

    ("毛 00-1-4 毛泽东思想定义（一）「来」",
     "毛泽东思想是<b>马克思列宁主义在中国的运用和发展</b>。<br>"
     "钩子：<b>来</b> —— 从哪来。"),

    ("毛 00-1-4 毛泽东思想定义（二）「是」",
     "毛泽东思想是<b>被实践证明了的</b>、<b>关于中国革命和建设的</b>、"
     "<b>正确的理论原则和经验总结</b>。<br>"
     "钩子：<b>是</b> —— 三截：<b>证据</b>（被实践证明了的）／<b>范围</b>（关于中国革命和建设的）／"
     "<b>性质</b>（正确的理论原则和经验总结）。<br>"
     "⚠️ 漏掉「关于中国革命和建设的」= 抹掉范围。"),

    ("毛 00-1-4 毛泽东思想定义（三）「归」",
     "毛泽东思想是<b>中国共产党集体智慧的结晶</b>。<br>"
     "钩子：<b>归</b> —— 归谁。不是毛泽东一个人的。"),

    ("毛 00-1-4 哪次会议提出「中国特色社会主义理论体系」这个概念？标志什么？",
     "<b>党的十七大（2007 年）</b>。<br>"
     "它把邓小平理论、「三个代表」、科学发展观<b>打包成一个体系</b>。<br>"
     "这一打包，标志着<b>理论和实践进一步成熟</b>。"),

    ("毛 00-1-4 一脉相承、与时俱进｜各承什么、进什么？",
     "<b>一脉相承</b>：承的是<b>立场、观点、方法</b> —— 实事求是、群众路线、独立自主。<br>"
     "<b>与时俱进</b>：进的是<b>时代课题和理论内容</b>。<br>"
     "一句话：<b>脉不变，话在变。</b>"),
]


def main():
    existing = call("findNotes", query=f'deck:"{DECK}" 00-1-4')["result"]
    fronts = set()
    if existing:
        for n in call("notesInfo", notes=existing)["result"]:
            fronts.add(n["fields"]["正面"]["value"].strip())

    notes = []
    skipped = []
    for front, back in CARDS:
        if front.strip() in fronts:
            skipped.append(front)
            continue
        notes.append({
            "deckName": DECK,
            "modelName": MODEL,
            "fields": {"正面": front, "背面": back},
            "tags": TAGS,
            "options": {"allowDuplicate": False, "duplicateScope": "deck"},
        })

    if not notes:
        print("全部已存在，未新增。")
        return

    res = call("addNotes", notes=notes)
    ids = res["result"]
    ok = [i for i in ids if i]
    print(f"新增 {len(ok)} 张，跳过重复 {len(skipped)} 张")
    for i, (front, _) in enumerate([c for c in CARDS if c[0] not in skipped]):
        print(f"  ✅ {front}")
    if skipped:
        for s in skipped:
            print(f"  ⏭ 已存在：{s}")


if __name__ == "__main__":
    main()
