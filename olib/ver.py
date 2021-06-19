# This file is placed in the Public Domain.

__version__ = 101

from krn import Kernel

def ver(event):
    event.reply("%s %s" % (Kernel.cfg.name.upper(), Kernel.cfg.version))
