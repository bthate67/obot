README
######

Welcome to OBOT,

OBOT is a pure python3 IRC bot you can use to display RSS feeds, act as a 
UDP to IRC relay and one you can program your own commands for. 

OBOT is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

OBOT can be found on pypi, see http://pypi.org/project/obot

installation is through pypi::

 $ sudo pip3 install obot --upgrade --force-reinstall

CONFIGURE
=========

OBOT has it's own CLI, the bot program, you can run it on the shell prompt 
and, as default, it won't do anything::

 $ obot
 $ 

use obot <cmd> to run a command directly, e.g. the cmd command shows
a list of commands::

 $ obot cmd
 cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,krn,log,met,mod,rem,rss,thr,ver,upt

configuration is done with the cfg command::

 $ obot cfg server=irc.freenode.net channel=\#dunkbots nick=botje
 ok

start the bot with the irc module enabled::

 $ obot mods=irc
 >

a shell is started as well so you can type commands on the bot's console.

RSS
===

OBOT provides, with the use of feedparser, the possibility to serve rss
feeds in your channel. Install python3-feedparser if you want to display 
rss feeds in the channel::

 $ sudo apt install python3-feedparser

To add an url use the rss command with an url::

 $ obot rss https://github.com/bthate/botlib/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 $ obot fnd rss
 0 https://github.com/bthate/botlib/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 $ obot ftc
 fetched 20

UDP
===

OBOT has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.

to enable udp start the bot with the udp module enabled::

 $ obot mods=irc,udp

output to the IRC channel is done with the use python3 code to send a UDP
packet to OBOT, it's unencrypted txt send to the bot and displayed in the
joined channels:

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)


COMMANDS
========

If you want to program on the bot and write your own commands, clone the
repository at github::

 $ sudo git clone https://github.com/bthate67/obot

programming your own commands is easy, open mod/hlo.py and add the following
code::

    def hlo(event):
        event.reply("hello %s" % event.origin)

recreate the dispatch table by using the tbl command::

 $ bin/tbl > obot/tbl.py

now you can type the "hlo" command, showing hello <user>::

    $ obot hlo
    hello root@console

24/7
====

to run OBOT 24/7 you need to enable the bots service under systemd:

edit /etc/systemd/system/bot.service and add the following txt::

 [Unit]
 Description=OBOTD - 24/7 channel service
 After=multi-user.target

 [Service]
 DynamicUser=True
 StateDirectory=obotd
 LogsDirectory=obotd
 CacheDirectory=obotd
 ExecStart=/usr/local/bin/obotd
 CapabilityBoundingSet=CAP_NET_RAW

 [Install]
 WantedBy=multi-user.target

then enable the bot service with::

 $ sudo systemctl enable obotd
 $ sudo systemctl daemon-reload

edit the irc configuration::

 $ sudo obotd cfg server=irc.freenode.net channel=\#dunkbots 

and start the bot::

 $ sudo systemctl start obotd

if you don't want the bot to startup at boot, remove the service file::

 $ sudo rm /etc/systemd/system/obotd.service

CONTACT
=======

have fun coding

| Bart Thate (bthate67@gmail.com)
| botfather on #dunkbots irc.freenode.net
