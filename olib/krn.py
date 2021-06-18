# This file is placed in the Public Domain.

import getpass
import importlib
import obj
import os
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
 
    def boot(self, name, version, mns=""):
        self.cfg.name = name
        self.cfg.mods += "," + mns
        self.cfg.version = version
        self.cfg.update(self.cfg.sets)
        self.cfg.wd = obj.cfg.wd = self.cfg.wd or obj.cfg.wd
        obj.cdir(self.cfg.wd + os.sep)
        try:
            pwn = pwd.getpwnam(name)
        except KeyError:
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except KeyError:
                return
        try:
            os.chown(self.cfg.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        self.privileges()

    def cmd(self, txt):
        Bus.add(self)
        e = self.event(txt)
        self.dispatch(self, e)
        e.wait()

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

    def init(self, mns):
        for mn in spl(mns):
            mnn = Table.getfull(mn)
            mod = Table.getmod(mnn)
            if "init" in dir(mod):
                launch(mod.init, self)

    def opts(self, ops):
        for opt in ops:
            if opt in self.cfg.opts:
                return True
        return False

    def parse(self):
        parse_txt(self.cfg, " ".join(sys.argv[1:]))

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

    def say(self, channel, txt):
        print(txt)

    @staticmethod
    def scan(path, base=None):
        if not os.path.exists(path):
            return
        if base is None:
            base = os.path.abspath(path).split(os.sep)[-1]
        sys.path.insert(0, base)
        for p in os.listdir(path):
            mn = p.split(os.sep)[-1][:-3]
            try:
                mod = importlib.import_module(mn)
            except ModuleNotFoundError:
                continue
            builtin(mod)

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)
