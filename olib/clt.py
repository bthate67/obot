# This file is placed in the Public Domain.

import queue
import threading

from krn import Kernel
from obj import Object

class Client(Object):

    def __init__(self):
        super().__init__()
        self.iqueue = queue.Queue()
        self.ready = threading.Event()
        self.speed = "normal"
        self.target = Kernel
        
    def event(self, txt):
        if txt is None:
            return
        c = Command()
        c.txt = txt or ""
        c.orig = self.__dorepr__()
        return c

    def handle(self, e):
        self.target.put(e)

    def handler(self):
        while not self.stopped.isSet():
            txt = self.poll()
            if txt is None:
                break
            e = self.event(txt)
            if not e:
                break
            self.handle(e)

    def poll(self):
        return self.iqueue.get()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)

    def put(self, e):
        self.iqueue.put_nowait(e)

    def start(self):
        Bus.add(self)
        launch(self.handler)
        return self

    def stop(self):
        self.stopped.set()
        self.iqueue.put(None)

    def wait(self):
        self.ready.wait()
