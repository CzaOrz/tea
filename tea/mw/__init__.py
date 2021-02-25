# coding: utf-8
import loggus
import inspect

from tea.ctx import Ctx
from contextlib import contextmanager

__all__ = "Mw",


def CheckArgs(func):
    if len(inspect.getfullargspec(func).args) != 1:
        loggus.panic(f"{func} only 1 params")


def CheckGenerator(func):
    if not inspect.isgeneratorfunction(func):
        loggus.panic(f"{func} is not a generator")


def CheckMw(*mws):
    for mw in mws:
        CheckArgs(mw)
        CheckGenerator(mw)


def Mw(ctx: Ctx, handler, *mw):
    if mw:
        with contextmanager(mw[0])(ctx):
            return Mw(ctx, handler, *mw[1:])
    else:
        return handler(ctx)
