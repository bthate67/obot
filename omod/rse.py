# This file is placed in the Public Domain.

from hdl import ENOMORE

def register(k):
    k.addcmd(rse)

def rse(event):
    raise ENOMORE
