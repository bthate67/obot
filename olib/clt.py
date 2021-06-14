# This file is placed in the Public Domain.

import bus
import evt
import obj
import queue
import thr
import threading
import utl

class Client(obj.Object):

    def __init__(self, target):
        super().__init__()
        self.iqueue = queue.Queue()
        self.speed = "normal"
        self.stopped = threading.Event()
        self.target = target

    def announce(self, txt):
        self.raw(txt)

    def cmd(self, txt):
        e = evt.Command()
        e.orig = self.__dorepr__()
        e.txt = txt
        return hdl.docmd(c, e)

    def event(self, txt):
        c = evt.Command()
        if txt is None:
            c.type = "end"
        else:
            c.txt = txt
        c.orig = self.__dorepr__()
        return c

    def handle(self, e):
        self.target.put(e)

    def input(self):
        while not self.stopped.isSet():
            e = self.once()
            if not e:
                break
            self.handle(e)

    def once(self):
        return self.event(self.poll())

    def poll(self):
        return self.iqueue.get()

    def raw(self, txt):
        pass

    def restart(self):
        self.stop()
        self.start()

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        bus.Bus.add(self)
        thr.launch(self.input)

    def stop(self):
        self.stopped.set()
        self.iqueue.put(None)
