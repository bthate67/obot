# This file is placed in the Public Domain.

from bus import Bus
from nms import Names
from obj import cfg
from zzz import unittest

from test.prm import param

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(cfg.index or 1):
            exec()
        consume()

events = []

def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    #for e in events:
    #    print(e)
    return res

def exec():
    c = Bus.objs[0]
    l = sorted(Names.modules)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd + " " + ex)
            c.put(e)
            events.append(e)
