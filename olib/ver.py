# This file is placed in the Public Domain.

__version__ = 45

from krn import Kernel

def register(k):
    k.addcmd(ver)

def ver(event):
    event.reply("%s %s" % (Kernel.cfg.name.upper(), Kernel.cfg.version))
