# This file is placed in the Public Domain.

from obj import Object

param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["cfg server=localhost", "cfg", ""]
param.dne = ["test4", ""]
param.rm = ["reddit", ""]
param.dpl = ["reddit title,summary,link", ""]
param.log = ["test1", ""]
param.flt = ["0", "1", ""]
param.fnd = ["cfg",
             "log",
             "todo",
             "rss",
             "cfg server==localhost",
             "rss rss==reddit rss",
             "email From==pvp From Subject -t"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]
#param.mbx = ["~/Desktop/25-1-2013", ""]
