# This file is placed in the Public Domain.

"database,timer and tables"

import getpass
import os
import pwd
import sys
import time

from dft import Default
from obj import Object, cdir, cfg, spl
from prs import parse_txt
from thr import launch

def __dir__():
    return ('Cfg', 'Kernel', 'Repeater', 'Timer', 'all', 'debug', 'deleted',
            'every', 'find', 'fns', 'fntime', 'hook', 'last', 'lastfn',
            'lastmatch', 'lasttype', 'listfiles')

all = "adm,cms,fnd,irc,krn,log,rss,tdo"

class ENOCLASS(Exception):

    pass

class ENOTYPE(Exception):

    pass

class Cfg(Default):

    pass

class Kernel(Object):

    cfg = Cfg()
    cmds = Object()
    fulls = Object()
    names = Default()
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
        Kernel.cfg.wd = cfg.wd = Kernel.cfg.wd or cfg.wd
        cdir(Kernel.cfg.wd + os.sep)
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
    def getcls(name):
        if "." in name:
            mn, clsn = name.rsplit(".", 1)
        else:
            raise ENOCLASS(name)
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

def kcmd(hdl, obj):
    obj.parse()
    f = Kernel.getcmd(obj.cmd)
    if f:
        f(obj)
        obj.show()
    sys.stdout.flush()
    obj.ready()

def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    t = Kernel.getcls(cname)
    if not t:
        raise ENOTYPE(cname)
    if fn:
        o = t()
        o.load(fn)
        return o
    raise ENOTYPE(cname)

def privileges(name=None):
    if os.getuid() != 0:
        return
    if name is None:
        try:
            name = getpass.getuser()
        except KeyError:
            pass
    try:
        pwnam = pwd.getpwnam(name)
    except KeyError:
        return False
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)
    old_umask = os.umask(0o22)
    return True

def root():
    if os.geteuid() != 0:
        return False
    return True
