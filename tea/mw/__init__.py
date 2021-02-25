# coding: utf-8
from contextlib import contextmanager

from tea.ctx import Ctx


def Mw(ctx: Ctx, handler, *mw):
    if mw:
        with contextmanager(mw[0])(ctx):
            return Mw(ctx, handler, *mw[1:])
    else:
        return handler(ctx)
