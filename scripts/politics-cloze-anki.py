# -*- coding: utf-8 -*-
"""政治挖空 L3 骨架 → Anki 默写卡

为什么加这一批卡：
  网页上的挖空练习适合「坐下写一遍」，不适合每天通勤时刷。
  而政治丢分的地方恰恰是「看着眼熟、闭卷写不出」——这需要高频短时重复。
  所以把 L3 的骨架抽成卡：正面是残缺的句子，背面是原文。
  两者同源（都来自 scripts/politics-cloze-gen.mjs 的同一段），改一处两边都变。

★ 不动已有卡片。这个脚本只 INSERT，不 UPDATE、不 DELETE。
  写入前强制备份 collection.anki2；写入后读回校验张数。
  任何一步对不上就回滚（用备份覆盖回去）并退出非 0。

用法：
  python scripts/politics-cloze-anki.py                # 试运行，只报数量
  python scripts/politics-cloze-anki.py --apply        # 真写
  python scripts/politics-cloze-anki.py --apply --deck "专升本::政治::A级64篇默写"

为什么直接写 sqlite 而不是走 AnkiConnect：
  AnkiConnect 需要 Anki 开着。批处理时开着 GUI 反而会让 collection 被锁。
  schema 18 的写入规则已经摸清（见下面 note/card 的字段），
  加上「只 INSERT + 先备份 + 写后读回」，风险可控。
"""
from __future__ import annotations

import base64
import json
import hashlib
import os
import random
import shutil
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLOZE_DIR = ROOT / "docs" / "posts" / "politics" / "cloze"
COLLECTION = Path(os.path.expanduser("~")) / "AppData" / "Roaming" / "Anki2" / "账户 1" / "collection.anki2"

DECK_DEFAULT = "专升本\x1f政治\x1fA级64篇默写"
NOTETYPE = "问答题"
TAG_BASE = ["政治", "挖空", "L2半句"]

MIN_LEN = 12  # 太短的骨架没有练习价值（比如只剩「____」）


def guid() -> str:
    return base64.b64encode(bytes(random.getrandbits(8) for _ in range(8))).decode("ascii")


def checksum(text: str) -> int:
    """Anki 的 csum = sha1(sfld) 前 8 位十六进制转十进制。"""
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest()[:8], 16)


def main() -> int:
    apply = "--apply" in sys.argv
    deck_name = DECK_DEFAULT
    if "--deck" in sys.argv:
        deck_name = sys.argv[sys.argv.index("--deck") + 1]

    if not COLLECTION.exists():
        print(f"找不到 collection：{COLLECTION}")
        return 1
    if not CLOZE_DIR.exists():
        print(f"找不到挖空产物：{CLOZE_DIR}（先跑 scripts/politics-cloze-gen.mjs）")
        return 1

    conn = sqlite3.connect(COLLECTION)
    # Anki 给 decks.name 挂了自定义排序规则 `unicase`，Python 的 sqlite3 不认识，
    # 不注册就会在第一次按名字查牌组时抛 "no such collation sequence: unicase"。
    # casefold 足够贴近 Anki 的语义（这里只用于等值匹配，不依赖排序细节）。
    conn.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold()) - (a.casefold() < b.casefold()))
    cur = conn.cursor()

    deck_id = cur.execute("select id from decks where name=?", (deck_name,)).fetchone()
    if not deck_id:
        print(f"牌组不存在：{deck_name}")
        print("现有政治牌组：", [r[0] for r in cur.execute("select name from decks where name like '%政治%'")])
        return 1
    deck_id = deck_id[0]

    mid = cur.execute("select id from notetypes where name=?", (NOTETYPE,)).fetchone()
    if not mid:
        print(f"笔记类型不存在：{NOTETYPE}")
        return 1
    mid = mid[0]

    # 已有正面文本 → 用来去重。只读，不改。
    existing = {r[0] for r in cur.execute(
        "select substr(flds, 1, instr(flds, char(31)) - 1) from notes where mid=?", (mid,))}

    new_cards: list[tuple[str, str, str]] = []  # (正面, 背面, 篇名)
    per_file: list[tuple[str, int]] = []

    # 配对表由 scripts/politics-cloze-gen.mjs 生成。不在这里解析 markdown：
    # 页面里有 `---` 分隔线和 <details> 包裹，按行数对齐会差几行，
    # 而生成器那边两侧是同一个数组切出来的，索引严格对齐。
    pair_file = CLOZE_DIR / "_pairs.json"
    if not pair_file.exists():
        print(f"找不到配对表：{pair_file}（先跑 scripts/politics-cloze-gen.mjs）")
        return 1
    pairs = json.loads(pair_file.read_text(encoding="utf-8"))
    if not pairs:
        print("配对表是空的。")
        return 1

    for p in pairs:
        front, back, name = p["front"], p["back"], p["source"]
        if front in existing:
            continue
        existing.add(front)
        new_cards.append((front, back, name))
        per_file.append((name, 1))

    # 按篇聚合计数，方便看哪几篇没产出
    agg: dict[str, int] = {}
    for name, _ in per_file:
        agg[name] = agg.get(name, 0) + 1
    per_file = sorted(agg.items())

    print(f"\n=== 政治 L2 半句卡 ===")
    print(f"牌组：{deck_name}  笔记类型：{NOTETYPE}")
    print(f"待写入：{len(new_cards)} 张（已去重，现有 {len(existing)} 条正面）\n")
    for name, n in per_file:
        print(f"  {name:32} +{n}")

    if not new_cards:
        print("\n没有新卡可写。")
        return 0
    if not apply:
        print("\n[试运行] 加 --apply 才真写入")
        return 0

    backup = COLLECTION.with_name(f"collection.anki2.bak-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(COLLECTION, backup)
    print(f"\n已备份 → {backup.name}")

    before_notes = cur.execute("select count(*) from notes").fetchone()[0]
    before_cards = cur.execute("select count(*) from cards").fetchone()[0]

    now_ms = int(time.time() * 1000)
    now_s = int(time.time())
    next_due = (cur.execute("select max(due) from cards where type=0").fetchone()[0] or 0) + 1

    try:
        for i, (front, back, name) in enumerate(new_cards):
            nid = now_ms + i
            flds = f"{front}\x1f{back}"
            cur.execute(
                "insert into notes (id,guid,mid,mod,usn,tags,flds,sfld,csum,flags,data)"
                " values (?,?,?,?,?,?,?,?,?,0,'')",
                (nid, guid(), mid, now_s, -1, f" {TAG_BASE[0]} {TAG_BASE[1]} {TAG_BASE[2]} ",
                 flds, front, checksum(front)),
            )
            cur.execute(
                "insert into cards (id,nid,did,ord,mod,usn,type,queue,due,ivl,factor,reps,lapses,left,odue,odid,flags,data)"
                " values (?,?,?,0,?,-1,0,0,?,0,0,0,0,0,0,0,0,'')",
                (nid, nid, deck_id, now_s, next_due + i),
            )
        cur.execute("update col set mod=?", (now_s,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        shutil.copy2(backup, COLLECTION)
        print(f"写入失败，已回滚：{e}")
        return 1

    after_notes = cur.execute("select count(*) from notes").fetchone()[0]
    after_cards = cur.execute("select count(*) from cards").fetchone()[0]

    print(f"\nnotes {before_notes} → {after_notes}（+{after_notes - before_notes}）")
    print(f"cards {before_cards} → {after_cards}（+{after_cards - before_cards}）")

    ok = (after_notes - before_notes) == len(new_cards) and (after_cards - before_cards) == len(new_cards)
    if not ok:
        conn.close()
        shutil.copy2(backup, COLLECTION)
        print("张数对不上，已回滚。")
        return 1

    # 抽样读回，确认字段能取出来（不是只看 count）
    sample = cur.execute(
        "select n.flds, c.did from notes n join cards c on c.nid=n.id where n.id>=? limit 1",
        (now_ms,)).fetchone()
    print(f"\n抽样：did={sample[1]} 正面={sample[0].split(chr(31))[0][:40]}")
    conn.close()
    print(f"\n✅ 写入 {len(new_cards)} 张，读回校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
