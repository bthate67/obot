# This file is placed in the Public Domain.

"database,timer and tables"

import bus
import dft
import getpass
import hdl
import obj
import os
import prs
import pwd
import sys
import tbl
import thr
import time
import utl

from obj import Object, cdir, cfg, spl
from prs import parse_txt
from thr import launch
from utl import privileges

def __dir__():
    return ('Cfg', 'Kernel', 'Repeater', 'Timer', 'all', 'debug', 'deleted',
            'every', 'find', 'fns', 'fntime', 'hook', 'last', 'lastfn',
            'lastmatch', 'lasttype', 'listfiles')

all = "adm,cms,fnd,irc,krn,log,rss,tdo"

class Cfg(dft.Default):

    pass

class Kernel(hdl.Handler):

    cfg = Cfg()
    cmds = Object()
    table = Object()

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

    def cmd(self, clt, txt):
        e = clt.event(txt)
        self.put(e)
        e.wait()

    def getcmd(mn):
        return tbl.Table.cmds.get(mn, None)

    def getmod(mn):
        return tbl.Table.table.get(mn, None)

    @staticmethod
    def init(mns):
        for mn in spl(mns):
            mnn = tbl.Table.getfull(mn)
            mod = tbl.Table.getmod(mnn)
            if "init" in dir(mod):
                launch(mod.init, Kernel)

    @staticmethod
    def dispatch(hdl, obj):
        obj.parse()
        f = Kernel.getcmd(obj.cmd)
        if f:
            f(obj)
            obj.show()
        print(obj)
        sys.stdout.flush()
        obj.ready()

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

    def start(self):
        super().start()
        self.register("cmd", self.dispatch)

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)
