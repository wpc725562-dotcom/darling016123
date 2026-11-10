# -*- coding: utf-8 -*-
"""向 学习日志.jsonl 追加 2022 完形精讲记录（append-only，不改旧行）"""
import json, io, os

LOG = r'D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl'

entry = {
    "date": "2026-10-23",
    "subject": "英语",
    "kind": "lecture",
    "title": "2022 完形填空精讲 · 交付「骨架→对仗→词义→回读」四步流程，逐空讲 21/22/23/26/29，余 7 空带提示交回",
    "score": "",
    "mastery": "learning",
    "weak": "学生原话：「很多单词我都不认识 还有该怎么写」。真实卡点有两个：① 生词密度高，说明文话题词（gender / biological / verbal / spatial / compartment）全不熟；② **没有可执行的填空顺序**，15 空是「从上往下逐空硬想」，遇到需要跨句结构的空就卡死。",
    "note": (
        "【关于「Free 高考英语」方法 —— 必须留证，不能编】\n"
        "学生要求「按照 free 高考英语写完形填空的方法」讲。查证结果：\n"
        "① 本地讲义库 `data/bili-analyze/_extract/` 共 238 份 md，英语类 **0 份**（`ls | grep -icE \"英语|english\"` = 0）；\n"
        "② WebSearch 命中 B 站「FREE高考英语一轮复习课程：完形填空部分」两个 opus 页（1014117825306951698 / 1058582943130189862）；\n"
        "③ WebFetch 打开第一个，**页面只有标题和发布时间，无正文无讲义**（客户端渲染，抓不到内容）。\n"
        "⇒ **按反空转纪律第 2 次尝试无新信息即停**，不继续换姿势抓。已向学生明确声明「Free 的原始方法我没有可信来源，不编」，并说明本轮方法是从**他自己的错题数据**反推的。若他提供 Free 讲义截图/文字，再合并。\n\n"
        "【本次交付：完形四步流程（自建，非引用）】\n"
        "① **骨架** —— 只读首句与各段首句，不填任何空，30 秒判文体+段落角色。本文：第1段 `have made us believe` = 旧观点；第2段 `But ... newly published` = 反转新观点；第3段 `Try this experiment` = 实验证据；第4段 `This is one of the many ... prove` = 回指总结。\n"
        "② **对仗** —— 一句话里出现两个空且 `and` 两侧结构对称，必须成对填。本文 22/23：`women can be trained to do <jobs> that men traditionally do, and men can and should do more <housework>`。\n"
        "③ **词义** —— 前三步过不了才看选项。本文 15 空里只有 24/27/28 是纯词义题（学生这三题全对，说明词义层不是瓶颈）。\n"
        "④ **回读** —— 填完整段连读，读不通就是错。\n\n"
        "【逐空精讲（5 空，均带判据）】\n"
        "· **21** 答 C practice ❌ 应 D result。`the ___ of` 四选项全是名词，语法不卡人；旧观点说「差异是教养造成的」⇒ 教养是原因、差异是结果，`the result of` = ……的结果。`the practice of` = ……的做法，代入成「差异是教养方式的做法」，不通。**判据：A is the result of B ⇒ B 造成 A，先问谁造成谁。**\n"
        "· **22/23** 答 A cooking / B experiments ❌ 应 C jobs / A housework。两空单独看都「像」，镜像一对就锁死：第一空后有定语从句 `that men traditionally do` ⇒ 填男人做的事；第二空主语换成 men ⇒ 填女人做的事。**判据：看到 and 两边结构一样，一定成对填。**\n"
        "· **26** 答 C disappear ❌ 应 B exist。这是新观点句，新观点要**支持**「男女有别」；`because` 后是「大脑完全不同」⇒ 差异当然**存在**。disappear 代入成「差异消失，因为大脑不同」，因果反了。**判据：because 后面那句必须能推出前面，推不出就是错项。**\n"
        "· **29** 答 B word ❌ 应 D passage。`read a passage aloud` 是固定搭配（朗读一段）；且实验要「一边读一边敲桌保持匀速」，读一个单词 1 秒就完，实验做不成。**判据：搭配 + 这事在现实里做不做得成（常识校验）—— 这个动作学生完全没有。**\n\n"
        "【生词处理（今天最该带走的一条）】\n"
        "说明文生词分两类，处理方式相反：\n"
        "· **话题词 → 必须查**（答案建在它们上面）：gender 性别 · biological 生理的 · verbal 言语的 · spatial 空间的 · compartment 隔间/分区 · prove 证明\n"
        "· **修饰词 → 先跳过**：completely 完全地 · newly 新近地 · traditionally 传统上 · so-called 所谓的 · mainly 主要地\n"
        "**判据：只查「空周围 5 个词以内」的生词；离空三步以外、只起修饰作用的，先跳过。** 说明文生词密度高，不可能全查完再动笔。\n"
        "分段时间线生词表已给：第1段 psychologist / be brought up / theory / so-called；第2段 gender / biological / behave；第3段 tap / constant / maintain / aloud；第4段 compartment / verbal / spatial / be dealt with。\n\n"
        "【交回学生的部分（未给答案，只给指路）】\n"
        "余 7 空 25/30/31/32/33/34/35，要求每空写「依据句 + 用了哪一步」。提示：34 走第①步骨架；31/32/33 是**一组对仗**，先找 `Men, however` 这个反转信号，再把 `with ___ hand` 与 `men ... with their left hand` 摆一起看；30 对照第 33 空 `slow down` 反推；25 联系后文 `according to a recent scientific study`。\n\n"
        "【未做】Anki 建卡未建（等学生勾词，不替他决定）；VS/GDB 速查卡实测仍欠。"
    ),
}

with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')

with io.open(LOG, 'r', encoding='utf-8') as f:
    n = sum(1 for _ in f)
print('appended -> line', n)
