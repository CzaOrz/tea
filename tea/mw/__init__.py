# coding: utf-8
import loggus
import inspect

from tea.ctx import Ctx
from contextlib import contextmanager


def CheckMw(*mws):
    for mw in mws:
        if not inspect.isgeneratorfunction(mw):
            loggus.panic(f"mw[{mw}] is not a generator func")


def Mw(ctx: Ctx, handler, *mw):
    if mw:
        with contextmanager(mw[0])(ctx):
            return Mw(ctx, handler, *mw[1:])
    else:
        return handler(ctx)
