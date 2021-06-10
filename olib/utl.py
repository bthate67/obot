# This file is placed in the Public Domain.

import builtins
import importlib
import inspect
import krn
import os
import pwd
import sys
import trm

def builtin(mod):
    classes = find_cls(mod)
    for nm, c in classes.items():
        setattr(builtins, nm, c)

def cprint(*args):
    print(*args)
    sys.stdout.flush()

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

def find_cls(mod):
    res = {}
    for key, o in inspect.getmembers(mod, inspect.isclass):
        res[o.__name__] = o
    return res

def wrap(func):
    trm.termsave()
    try:
        func()
    except PermissionError as ex:
        cprint(str(ex))
    except KeyboardInterrupt:
        pass
    finally:
        trm.termreset()

def privileges(name):
    if os.getuid() != 0:
        return
    try:
        pwn = pwd.getpwnam(name)
    except KeyError:
        return
    os.setgroups([])
    os.setgid(pwn.pw_gid)
    os.setuid(pwn.pw_uid)
    old_umask = os.umask(0o22)
    return True

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
        krn.Kernel.addmod(mod)
        if "register" in dir(mod):
            mod.register(krn.Kernel)
