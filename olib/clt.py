# This file is placed in the Public Domain.

import queue

from evt import Command
from hdl import ENOMORE, Handler, docmd
from thr import launch

class Client(Handler):

    def __init__(self):
        super().__init__()
        self.iqueue = queue.Queue()
        self.stopped = False
        self.running = False

    def announce(self, txt):
        self.raw(txt)

    def event(self, txt):
        c = Command()
        if txt is None:
            c.type = "end"
        else:
            c.txt = txt
        c.orig = self.__dorepr__()
        return c

    def handle(self, e):
        super().put(e)

    def input(self):
        while not self.stopped:
            e = self.once()
            if not e:
                break
            self.handle(e)

    def once(self):
        txt = self.poll()
        return self.event(txt)

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
        if self.running:
            return
        self.stopped = False
        self.running = True
        self.initialize()
        super().start()
        launch(self.input)

    def stop(self):
        self.running = False
        self.stopped = True
        self.iqueue.put(None)
        super().stop()
