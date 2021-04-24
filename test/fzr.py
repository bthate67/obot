# This file is placed in the Public Domain.

import os, sys ; sys.path.insert(0, os.getcwd())

from bot.evt import Event
from bot.hdl import Handler, cmd
from bot.itr import getmods
from bot.krn import cprint, debug, kernel, opts
from bot.obj import Object, dorepr, getname
from bot.rss import Feed
from bot.tbl import tbl
from bot.usr import ENOUSER
from bot.trc import exception
from bot.ver import ver
from bot.zzz import inspect, os, sys, unittest

def cb():
    if opts("v") and debug:
        cprint("yoo")

exclude = ["poll", "handler", "input", "doconnect", "raw", "start"]
exc = []
result = []

values = Object()
values["daemonic"] = True
values['url'] = "http://rtfd.io"
values['code'] = 200
values['msg'] = "OK"
values['hdrs'] = {}
values['fp'] = "bla"
values["addr"] = ("127.0.0.1", 6667)
values["reason"] = "whyyyyy????"
values["channel"] = "#opbot"
values["mn"] = "bot.obj"
values["cmd"] = ver
values["txt"] = "yoo2"
values["key"] = "txt"
values["value"] = Object()
values["d"] = {}
values["hdl"] = Handler()
values["event"] = Event({"txt": "thr", "orig": dorepr(k)})
values["pevent"] = Event({"txt": "thr", "orig": dorepr(k)})
values["dccevent"] = Event({"txt": "thr", "orig": dorepr(k)})
values["path"] = k.cfg.wd
values["channel"] = "opbot"
values["orig"] = dorepr(values["hdl"])
values["obj"] = k
values["rssobj"] = Object({"rss": "https://www.reddit.com/r/python/.rss"})
values["pkgnames"] = "op"
values["name"] = "ver"
values["callback"] = cb
values["e"] = Event({"txt": "thr", "orig": repr(k), "error": "test"})
values["mod"] = cmd
values["mns"] = "irc,udp,rss"
values["sleep"] = 60.0
values["func"] = cb
values["origin"] = "test@shell"
values["perm"] = "USER"
values["permission"] = "USER"
values["text"] = "yoo"
values["server"] = "localhost"
values["nick"] = "opbot"
values["o"] = Object()
values["handler"] = Handler()
values["skip"] = []
values["k"] = k
values["key"] = "txt"
values["value"] = {"txt": "test"}
values["v"] = values["value"]
values["data"] = values["e"]
values["typ"] = Object
values["tbl"] = tbl
values["mnn"] = "bot.obj"
values["feed"] = Feed({"rss": "https://www.reddit.com/r/python/.rss"})
values["val"] = {}

class Test_Fuzzer(unittest.TestCase):

    def test_fuzz(self):
        m = getmods("op")
        for x in range(k.cfg.index or 1):
            for mod in m:
                fuzz(mod)

def getvalues(vars):
    args = []
    for k in vars:
        res = values.get(k, None)
        if res is not None:
            args.append(res)
    return args

def fuzz(mod, *args, **kwargs):
    for name, o in inspect.getmembers(mod, inspect.isclass):
        if not issubclass(o, Object):
            continue
        if "_" in name:
            continue
        try:
            sig = inspect.signature(o.__init__)
            arg = sig.parameters.keys()
            args = getvalues(arg)
            cprint("%s(%s)" % (name, arg))
            oo = o(*args, **kwargs)
        except TypeError as ex:
            continue
        oo.stopped = True
        for name, meth in inspect.getmembers(oo, inspect.ismethod):
            if "_" in name or name in exclude:
                continue
            try:
                sig = inspect.signature(meth)
                arg = sig.parameters.keys()
                args = getvalues(arg)
                res = meth(*args, **kwargs)
            except RuntimeError:
                pass
            except ENOUSER:
                continue
            except Exception as ex:
                exc.append((getname(meth), exception()))
    for e in exc:
        cprint(e)
