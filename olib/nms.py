# This file is placed in the Public Domain.

from obj import Default, Object
from itr import findmods, findnames
from utl import direct
from zzz import js

class Names(Object):

    names = Default({
    })

    modules = Object({
    })

    inits =  Object({
    })

    @staticmethod
    def getnames(nm, dft=None):
        return Names.names.get(nm, dft)

    @staticmethod
    def getmodule(mn):
        return Names.modules.get(mn, None)

    @staticmethod
    def getinit(mn):
        return Names.inits.get(mn, None)

    @staticmethod
    def tbl(tbl):
        Names.names.update(tbl["names"])
        Names.modules.update(tbl["modules"])
        Names.inits.update(tbl["inits"])
