# This file is placed in the Public Domain.

from obj import Object, ObjectList
from utl import direct, spl, hasmod
from zzz import os, importlib, inspect, pkgutil, sys

def findcmds(mod):
    cmds = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in cmds:
                    cmds[key] = o
    return cmds

def findclass(mod):
    mds = ObjectList()
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            mds.append(o.__name__, o.__module__)
    return mds

def findclasses(mod):
    nms = ObjectList()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            nms.append(o.__name__, t)
    return nms

def findfuncs(mod):
    funcs = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in funcs:
                    funcs[key] = "%s.%s" % (o.__module__, o.__name__)
    return funcs

def findmods(mod):
    mods = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in mods:
                    mods[key] = o.__module__
    return mods

def findmodules(pns):
    mods = []
    for mn in findall(pns):
        if mn in mods:
            continue
        mod = direct(mn)
        mods.append(mod)
    return mods

def findnames(mod):
    tps = Object()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            if t not in tps:
                tps[o.__name__.lower()] = t
    return tps


def getargs(f):
    spec = inspect.signature(f)
    return spec.parameters

def getnames(pkgs):
    res = Object()
    for pkg in spl(pkgs):
        for mod in getmods(pkg):
            n = findnames(mod)
            res.update(n)
    return res

def hasmod(fqn):
    if fqn in sys.modules:
        return True
    try:
        spec = importlib.util.find_spec(fqn)
        if spec:
            return True
    except (ValueError, ModuleNotFoundError):
        pass
    try:
        direct(fqn)
        return True
    except ModuleNotFoundError:
        pass
    return False
