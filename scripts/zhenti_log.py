#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真题页工具链 · 共享日志（2026-09-20，修 E3）

E3 为什么算缺陷
---------------
审计原话是「全脚本 0 logging」。这句话本身不是重点，重点是这些脚本
原本**唯一的沟通方式就是 `print`**，于是有两件事做不到：

① **分不清「给人看的结果」和「给自己看的诊断」**
   `zhenti_regress.py` 的 stdout 是人读的表格，同时 `--json` 模式下还要
   被整体重定向成机器可读的 JSON。想在中间插一句「正在读哪个配置」，
   就只能混进 stdout —— 要么污染输出，要么干脆不写。
   于是「跑了、没比对、退出码 0」那类假绿（A1/A2/A4）能长期存活。

② **没有级别**
   想临时看细节，只能改代码加 `print`、跑完再删。删不干净就变成噪声。

logging 解决的正是这两件事：

   · 默认写 **stderr**，与 stdout 的正式输出天然分离；
   · 级别由 `ZHENTI_LOG` 环境变量或 `-v/-vv` 控制，**不改代码**就能调；
   · 带时间戳，跨进程排查时能对齐。

★ 只做加法
----------
所有脚本原有的 `print` 输出**一行都没动**。日志是**额外通道**，不是替代品 ——
把 print 换成 logging 会破坏既有输出契约（`--json`、外部脚本解析 stdout 等）。
「既有输出稳定 + 新增可调诊断」才是这次要的结果。

用法
----
    from zhenti_log import add_logging_args, get_logger, setup_from_args

    LOG = get_logger(__name__)        # 模块顶层

    LOG.debug("读配置 %s", path)      # 默认不显示
    LOG.info("共 %d 题", n)           # -v 时显示
    LOG.warning("配置缺失，跳过 %s", name)   # 默认就显示

命令行（脚本有 argparse 时）：

    ap = argparse.ArgumentParser()
    add_logging_args(ap)              # 加 -v / -vv / --log-level
    a = ap.parse_args()
    setup_from_args(a)                # 按参数配好级别

没有 argparse 的脚本（如 `zhenti_regress.py` 手写 sys.argv）：
只用 `ZHENTI_LOG` 环境变量即可，或自己调 `setup(level)`。

级别
----
    ZHENTI_LOG=DEBUG | INFO | WARNING（默认）| ERROR | CRITICAL | 数字
    -v → INFO      -vv → DEBUG
    --log-level=X 直接指定，优先级高于 -v

★ 优先级：`--log-level` > `-v/-vv` > `ZHENTI_LOG` > WARNING。

    ZHENTI_LOG=DEBUG python scripts/zhenti_regress.py
    python scripts/zhenti_convert.py --config x.json -vv
"""
from __future__ import annotations

import argparse
import logging
import os
import sys

# 根 logger 名。所有子 logger 都挂在它下面，共用同一个 handler。
ROOT_NAME = "zhenti"

# ★ 默认写 stderr：stdout 留给正式输出，这样 `--json`、`| grep` 之类都不受影响。
_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATEFMT = "%H:%M:%S"

_configured = False


def _parse_level(raw):
    """把 `ZHENTI_LOG` / `--log-level` 的值解析成 logging 级别常量。

    认不出来时返回 None（交给调用方决定回退），**不抛异常** ——
    环境变量写错不该让整个脚本崩掉。
    """
    if raw is None:
        return None
    s = str(raw).strip().upper()
    if not s:
        return None
    if s.isdigit():
        return int(s)
    return getattr(logging, s, None)


def setup(level=None):
    """配置（幂等）并返回根 logger。

    只装一个 handler，重复调用不会叠加 —— 脚本里 `get_logger()` 是在
    模块顶层调的，`setup_from_args()` 又在解析参数后调，必须幂等。
    """
    global _configured
    root = logging.getLogger(ROOT_NAME)
    if not _configured:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_FMT, datefmt=_DATEFMT))
        root.addHandler(handler)
        # 不往上级冒泡：否则 root logger 没配 handler 时会被 lastResort 再打一遍。
        root.propagate = False
        _configured = True
    if level is not None:
        root.setLevel(level)
    elif root.level == logging.NOTSET:
        root.setLevel(_parse_level(os.environ.get("ZHENTI_LOG")) or logging.WARNING)
    return root


def get_logger(name):
    """取一个挂在 `zhenti` 下的子 logger。

    `__name__` 传进来是 `zhenti_convert`（脚本以顶层模块运行），
    归一化成 `zhenti.convert`，日志里就能一眼看出是哪个脚本。

    ★ `__main__` 要特判：这些脚本都是**直接** `python scripts/zhenti_x.py` 跑的，
      此时 `__name__ == "__main__"`，不特判的话每份日志都印成 `zhenti.__main__`，
      多份脚本串在一个终端里就分不清谁是谁了。改用脚本文件名兜底。
    """
    setup()
    if name in (None, "__main__"):
        name = os.path.basename(sys.argv[0] or "") or ROOT_NAME
        if name.endswith(".py"):
            name = name[:-3]
    short = str(name).rsplit(".", 1)[-1]
    if short == ROOT_NAME:
        return logging.getLogger(ROOT_NAME)
    if short.startswith(ROOT_NAME + "_"):
        # `zhenti_convert` → `convert`，再挂到 `zhenti` 下 → `zhenti.convert`。
        # ★ 这里剥掉前缀、交给 getChild() 去拼，不能自己拼成 `zhenti.convert`
        #   再传进去 —— getChild() 是**追加**，会拼成 `zhenti.zhenti.convert`。
        short = short[len(ROOT_NAME) + 1:]
    return logging.getLogger(ROOT_NAME).getChild(short)


def add_logging_args(parser, *, verbose=True):
    """给 argparse 加日志开关。独立成组，`--help` 里不会跟业务参数混在一起。"""
    grp = parser.add_argument_group("日志")
    if verbose:
        grp.add_argument(
            "-v", "--verbose", action="count", default=0,
            help="提高日志级别：-v=INFO，-vv=DEBUG（默认 WARNING，写 stderr）",
        )
    grp.add_argument(
        "--log-level", default=None, metavar="LV",
        help="直接指定日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL），优先级高于 -v",
    )
    return grp


def setup_from_args(args):
    """按解析好的命令行参数定级别。

    ★ 优先级：`--log-level` > `-v/-vv` > `ZHENTI_LOG` > WARNING。
      `--log-level` 显式给了就完全按它；没给才看 `-v`；
      都没给就回到 `setup()` 里的环境变量回退。
    """
    lv = _parse_level(getattr(args, "log_level", None))
    if lv is None:
        v = getattr(args, "verbose", 0) or 0
        if v >= 2:
            lv = logging.DEBUG
        elif v == 1:
            lv = logging.INFO
    if lv is None:
        # 三者都没给：让 setup() 去读环境变量 / 回落 WARNING。
        return setup()
    return setup(lv)
