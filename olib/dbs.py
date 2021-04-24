# This file is placed in the Public Domain.

from obj import cfg, gettype, hook
from nms import Names
from tms import fntime
from zzz import os, _thread

dirlock = _thread.allocate_lock()

def all(otype, selector=None, index=None, timed=None):
    nr = -1
    if selector is None:
        selector = {}
    otypes = Names.getnames(otype, [otype,])
    for t in otypes:
        for fn in fns(t, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

def deleted(otype):
    otypes = Names.getnames(otype, [otype,])
    for t in otypes:
        for fn in fns(t):
            o = hook(fn)
            if "_deleted" not in o or not o._deleted:
                continue
            yield fn, o

def every(selector=None, index=None, timed=None):
    nr = -1
    if selector is None:
        selector = {}
    for otype in os.listdir(os.path.join(cfg.wd, "store")):
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

def find(otype, selector=None, index=None, timed=None):
    if selector is None:
        selector = {}
    otypes = Names.getnames(otype, [otype,])
    got = False
    nr = -1
    for t in otypes:
        for fn in fns(t, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            got = True
            yield (fn, o)
    if not got:
        return (None, None)

def last(o):
    path, l = lastfn(str(gettype(o)))
    if  l:
        o.update(l)
    if path:
        spl = path.split(os.sep)
        stp = os.sep.join(spl[-4:])
        return stp

def lastmatch(otype, selector=None, index=None, timed=None):
    res = sorted(find(otype, selector, index, timed), key=lambda x: fntime(x[0]))
    if res:
        return res[-1]
    return (None, None)

def lasttype(otype):
    fnn = fns(otype)
    if fnn:
        return hook(fnn[-1])

def lastfn(otype):
    fn = fns(otype)
    if fn:
        fnn = fn[-1]
        return (fnn, hook(fnn))
    return (None, None)

#@locked(savelock)
def fns(name, timed=None):
    if not name:
        return []
    assert cfg.wd
    p = os.path.join(cfg.wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if timed and "from" in timed and timed["from"] and fntime(p) < timed["from"]:
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)

def listfiles(wd):
    path = os.path.join(wd, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))

def search(o, s):
    ok = False
    try:
        ss = vars(s)
    except TypeError:
        ss = s
    for k, v in ss.items():
        vv = getattr(o, k, None)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok
