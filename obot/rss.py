# This file is placed in the Public Domain.

"""
BOTLIB provides, with the use of feedparser, the possibility to serve rss
feeds in your channel. Install python3-feedparser if you want to display 
rss feeds in the channel::

 $ sudo apt install python3-feedparser

To add an url use the rss command with an url::

 $ bot rss https://github.com/bthate/botlib/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 $ bot fnd rss
 0 https://github.com/bthate/botlib/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 $ bot ftc
 fetched 20
"""

from bus import Bus
from clk import Repeater
from dbs import all, find, last, lastmatch
from edt import edit
from obj import Cfg, Default, Object
from thr import launch
from url import geturl, striphtml, unescape
from zzz import threading, urllib

from urllib.error import HTTPError, URLError


try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

def init(hdl):
    f = Fetcher()
    launch(f.start)
    return f

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.dosave = False
        self.display_list = "title,link"
        self.tinyurl = False

class Feed(Default):

    pass

class Rss(Object):

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(Object):

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(Object):

    cfg = Cfg()
    seen = Seen()

    def __init__(self):
        super().__init__()
        self.connected = threading.Event()

    def display(self, o):
        result = ""
        dl = []
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            pass
        if not dl:
            dl = self.cfg.display_list.split(",")
        if not dl or not dl[0]:
            dl = ["title", "link"]
        for key in dl:
            if not key:
                continue
            data = o.get(key, None)
            if not data:
                continue
            data = data.replace("\n", " ")
            data = striphtml(data.rstrip())
            data = unescape(data)
            result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, feed):
        counter = 0
        objs = []
        if not feed.rss:
            return 0
        for o in reversed(list(getfeed(feed.rss))):
            if not o:
                continue
            f = Feed()
            f.update(feed)
            f.update(dict(o))
            u = urllib.parse.urlparse(f.link)
            if u.path and not u.path == "/":
                url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            else:
                url = f.link
            if url in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(f)
            if self.cfg.dosave:
                f.save()
        if objs:
            Fetcher.seen.save()
        for o in objs:
            txt = self.display(o)
            Bus.announce(txt)
        return counter

    def run(self):
        thrs = []
        for fn, o in all("rss"):
            thrs.append(launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        last(Fetcher.cfg)
        last(Fetcher.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()

    def stop(self):
        self.seen.save()

def getfeed(url):
    got = False
    if gotparser:
        try:
            result = geturl(url)
            if not result:
                got = False
            else:
                result = feedparser.parse(result.data)
                if result and "entries" in result:
                    got = True
                    for entry in result["entries"]:
                        yield entry
        except (ValueError, HTTPError, URLError):
            pass
    if not got:
        return [Object(), Object()]

def dpl(event):
    if len(event.args) < 2:
        event.reply("dpl <stringinurl> <item1,item2>")
        return
    setter = {"display_list": event.args[1]}
    fn, o = lastmatch("rss", {"rss": event.args[0]})
    if o:
        edit(o, setter)
        o.save()
        event.reply("ok")

def ftc(event):
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return

def rem(event):
    if not event.args:
        event.reply("rem <stringinurl>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for fn, o in find("rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        o.save()
    event.reply("ok")

def rss(event):
    if not event.args:
        event.reply("rss <url>")
        return
    url = event.args[0]
    res = list(find("rss", {"rss": url}))
    if res:
        return
    o = Rss()
    o.rss = event.args[0]
    o.save()
    event.reply("ok")
