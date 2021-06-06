# This is file is placed in Public Domain.

"commands"

from krn import Kernel

def __dir__():
    return ("cmd", "register")

def register(k):
    k.addcmd(cmd)

def cmd(event):
    event.reply(",".join(sorted(Kernel.modules)))
