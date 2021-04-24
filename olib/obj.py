# This file is placed in the Public Domain.

"""BOTLIB provides a library you can use to program objects under python3.
It  provides a basic BigO Object, that mimics a dict while using attribute
access and provides a save/load to/from json files on disk. Objects can be
searched with a little database module, provides read-only files to improve
persistence and use a type in filename reconstruction.

Basic usage is this:

 >>> from obj import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 'value'
 >>> o
 {"key": "value"}

Objects can be saved and loaded to JSON files:

 >>> from obj import Object, cfg
 >>> cfg.wd = "data"
 >>> o = Object()
 >>> o.key = "value"
 >>> path = o.save()
 >>> oo = Object().load(path)
 >>> oo.key
 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. Hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values."""

from err import ENOCLASS, ENOFILENAME
from zzz import datetime, importlib, js, os, time, types, uuid, _thread

savelock = _thread.allocate_lock()

def gettype(o):
    return str(type(o)).split()[-1][1:-2]

class O:

    __slots__ = ("__dict__", "__stp__")

    def __init__(self):
        self.__stp__ = os.path.join(gettype(self), str(uuid.uuid4()), os.sep.join(str(datetime.datetime.now()).split()))

    def __delitem__(self, k):
        try:
            del self.__dict__[k]
        except KeyError:
            pass

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __repr__(self):
        return js.dumps(self.__dict__, default=default, sort_keys=True)

class Obj(O):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            self.update(args[0])

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def register(self, key, value):
        self[str(key)] = value

    def set(self, key, value):
        self.__dict__[key] = value

    def update(self, data):
        return self.__dict__.update(data)

    def values(self):
        return self.__dict__.values()

class Object(Obj):

    def load(self, opath):
        assert cfg.wd
        if opath.count(os.sep) != 3:
            raise ENOFILENAME(opath)
        spl = opath.split(os.sep)
        stp = os.sep.join(spl[-4:])
        lpath = os.path.join(cfg.wd, "store", stp)
        try:
            with open(lpath, "r") as ofile:
                d = js.load(ofile, object_hook=Obj)
                self.update(d)
        except FileNotFoundError:
            pass
        self.__stp__ = stp
        return self

    #@locked(savelock)
    def save(self, tab=False):
        assert cfg.wd
        prv = os.sep.join(self.__stp__.split(os.sep)[:2])
        self.__stp__ = os.path.join(prv, os.sep.join(str(datetime.datetime.now()).split()))
        opath = os.path.join(cfg.wd, "store", self.__stp__)
        cdir(opath)
        with open(opath, "w") as ofile:
            js.dump(self, ofile, default=default, indent=4, sort_keys=True)
        os.chmod(opath, 0o444)
        return self.__stp__

class ObjectList(Object):

    def append(self, key, value):
        if key not in self:
            self[key] = []
        if value in self[key]:
            return
        if isinstance(value, list):
            self[key].extend(value)
        else:
            self[key].append(value)

    def update(self, d):
        for k, v in d.items():
            self.append(k, v)

class Default(Object):

    default = ""

    def __getattr__(self, k):
        try:
            return super().__getattribute__(k)
        except AttributeError:
            try:
                return super().__getitem__(k)
            except KeyError:
                return self.default

class Cfg(Default):

    mods = ""
    opts = Default()
    name = "bot"
    version = None
    wd = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mods = Cfg.mods
        self.opts = Cfg.opts
        self.name = Cfg.name
        self.version = Cfg.version
        self.wd = Cfg.wd

cfg = Cfg()

starttime = time.time()

def cdir(path):
    if os.path.exists(path):
        return
    res = ""
    path2, _fn = os.path.split(path)
    for p in path2.split(os.sep):
        res += "%s%s" % (p, os.sep)
        padje = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(padje)
            os.chmod(padje, 0o700)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass

def dorepr(o):
    return '<%s.%s object at %s>' % (
        o.__class__.__module__,
        o.__class__.__name__,
        hex(id(o))
    )

def getcls(fullname):
    try:
        modname, clsname = fullname.rsplit(".", 1)
    except Exception as ex:
        raise ENOCLASS(fullname) from ex
    mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    o = getcls(cname)()
    o.load(fn)
    return o

def opts(ops):
    global cfg
    for opt in ops:
        if opt in cfg.opts:
            return True
    return False

def default(o):
    if isinstance(o, O):
        return vars(o)
    if isinstance(o, dict):
        return o.items()
    if isinstance(o, list):
        return iter(o)
    if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
        return o
    return dorepr(o)

def fmt(o, keys=None, empty=True, skip=None):
    if keys is None:
        keys = o.keys()
    if not keys:
        keys = ["txt"]
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in sorted(keys):
        if key in skip:
            continue
        try:
            val = o[key]
        except KeyError:
            continue
        if empty and not val:
            continue
        val = str(val).strip()
        res.append((key, val))
    result = []
    for k, v in res:
        result.append("%s=%s%s" % (k, v, " "))
    txt += " ".join([x.strip() for x in result])
    return txt.strip()

def getname(o):
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    try:
        n = "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    except AttributeError:
        try:
            n = "%s.%s" % (o.__class__.__name__, o.__name__)
        except AttributeError:
            try:
                n = o.__class__.__name__
            except AttributeError:
                n = o.__name__
    return n

def tojson(o):
    return js.dumps(o.__dict__, default=default, indent=4, sort_keys=True)
