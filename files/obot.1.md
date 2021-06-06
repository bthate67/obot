% OBOT(1) OBOT(1)
% Bart Thate
% May 2021

# NAME
OBOT - 24/7 channel presence

# SYNOPSIS
| obot \<cmd\> [mods=mod1,mod2] [-v] [-d]

# DESCRIPTION
OBOT is a pure python3 IRC bot that you can run under systemd to restart
the bot after reboot. Provides a 24/7 channel presence in a IRC channel.

Programming commands is easy, just edit omod/hlo.py and add this piece of
code:

    def hlo(event):
        event.reply("hello")

The hlo command is now available:

    $ bot hlo
    hello

# EXAMPLES

| $ obot
| $ 

| $ obot cmd
| cfg,cmd,dlt,ech,exc,flt,fnd,krn,met,sve,thr,upt,ver

| $ obot cfg
| cc=@ channel=#botd nick=botd port=6667 server=localhost

| $ obot krn
| cmd=krn name=bot txt=krn users=True version=1 wd=/home/bart/.bot

| $ obot thr
| CLI.handler 0s | CLI.input 0s

| $ obot mods=csl,irc
| >

# SEE ALSO
| /var/lib/obot/
| /usr/local/share/obot
| ~/.obot

# COPYRIGHT
OBOT is placed in the Public Domain.
