# This file is placed in the Public Domain.

import getpass
import importlib
import obj
import os
import pkgutil
import pwd
import sys
import time

from dft import Default
from obj import Object, spl
from prs import parse_txt
from hdl import Handler
from tbl import Table, builtin

def __dir__():
    return ('Cfg', 'Kernel')

class Cfg(Default):

    pass

class Kernel(Handler):

    cfg = Cfg()
    table = Object()
 
    @staticmethod
    def boot(name, version, mns=""):
        Kernel.parse()
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
        Kernel.privileges()
        Kernel.scan("obj")

    @staticmethod
    def daemon():
        pid = os.fork()
        if pid != 0:
            trm.termreset()
            os._exit(0)
        os.setsid()
        os.umask(0)
        si = open("/dev/null", 'r')
        so = open("/dev/null", 'a+')
        se = open("/dev/null", 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

    @staticmethod
    def init(mns):
        for mn in spl(mns):
            mnn = Table.getfull(mn)
            mod = Table.getmod(mnn)
            if "init" in dir(mod):
                launch(mod.init, Kernel)

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

    @staticmethod
    def root():
        if os.geteuid() != 0:
            return False
        return True

    @staticmethod
    def scan(mn):
        mod = __import__(mn)
        path = getdir(mod)
        for mn in pkgutil.walk_packages([path,]):
            if mn[1] == "tbl":
                continue
            zip = mn[0].find_module(mn[1])
            mod = zip.load_module(mn[1])
            builtin(mod)

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)

def getdir(mod):
    try:
        return os.path.dirname(mod.__file__)
    except AttributeError:
        return mod.__path__[0]
