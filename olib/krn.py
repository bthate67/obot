# This file is placed in the Public Domain.

"database,timer and tables"

import dft
import getpass
import hdl
import obj
import os
import prs
import pwd
import sys
import thr
import time
import utl

from obj import Object, cdir, cfg, spl
from prs import parse_txt
from thr import launch
from utl import privileges

def __dir__():
    return ('Cfg', 'Kernel', 'Repeater', 'Timer', 'all', 'debug', 'deleted',
            'every', 'find', 'fns', 'fntime', 'hook', "kcmd", 'last', 'lastfn',
            'lastmatch', 'lasttype', 'listfiles')

all = "adm,cms,fnd,irc,krn,log,rss,tdo"

class Cfg(dft.Default):

    pass

class Kernel(hdl.Handler):

    cfg = Cfg()
    cmds = Object()
    fulls = Object()
    names = dft.Default()
    modules = Object()
    table = Object()

    @staticmethod
    def addcmd(func):
        n = func.__name__
        Kernel.modules[n] = func.__module__
        Kernel.cmds[n] = func

    @staticmethod
    def addcls(clz):
        n = clz.__name__.lower()
        if n not in Kernel.names:
            Kernel.names[n] = []
        nn = "%s.%s" % (clz.__module__, clz.__name__)
        if nn not in Kernel.names[n]:
            Kernel.names[n].append(nn)

    @staticmethod
    def addmod(mod):
        n = mod.__spec__.name
        Kernel.fulls[n.split(".")[-1]] = n
        Kernel.table[n] = mod

    @staticmethod
    def boot(name, version, mns=""):
        Kernel.cfg.name = name
        Kernel.cfg.mods += "," + mns
        Kernel.cfg.version = version
        Kernel.cfg.update(Kernel.cfg.sets)
        Kernel.cfg.wd = obj.cfg.wd = Kernel.cfg.wd or obj.cfg.wd
        obj.cdir(Kernel.cfg.wd + os.sep)
        try:
            pwn = pwd.getpwnam(name)
        except KeyError:
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except KeyError:
                return
        try:
            os.chown(Kernel.cfg.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        privileges()

    @staticmethod
    def cmd(txt):
        c = Client()
        c.start()
        e = Command()
        e.orig = c.__dorepr__()
        e.txt = txt
        kcmd(c, e)

    @staticmethod
    def getcls(name):
        if "." in name:
            mn, clsn = name.rsplit(".", 1)
        else:
            raise NoClassError(name)
        mod = Kernel.getmod(mn)
        return getattr(mod, clsn, None)

    @staticmethod
    def getcmd(c):
        return Kernel.cmds.get(c, None)

    @staticmethod
    def getfull(c):
        return Kernel.fulls.get(c, None)

    @staticmethod
    def getmod(mn):
        return Kernel.table.get(mn, None)

    @staticmethod
    def getnames(nm, dft=None):
        return Kernel.names.get(nm, dft)

    @staticmethod
    def getmodule(mn, dft):
        return Kernel.modules.get(mn, dft)

    @staticmethod
    def init(mns):
        for mn in spl(mns):
            mnn = Kernel.getfull(mn)
            mod = Kernel.getmod(mnn)
            if "init" in dir(mod):
                launch(mod.init)

    @staticmethod
    def opts(ops):
        for opt in ops:
            if opt in Kernel.cfg.opts:
                return True
        return False

    @staticmethod
    def parse():
        parse_txt(Kernel.cfg, " ".join(sys.argv[1:]))

    @staticmethod
    def regs(mns):
        if mns is None:
            return
        for mn in spl(mns):
            mnn = Kernel.getfull(mn)
            mod = Kernel.getmod(mnn)
            if "register" in dir(mod):
                mod.register(Kernel)

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)
