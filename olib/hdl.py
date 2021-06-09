# This file is placed in the Public Domain.

import queue
import threading

from bus import Bus
from evt import Event
from obj import Object
from thr import launch
from trc import get_exception

class ENOMORE(Exception):

    pass

class Handler(Object):

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.queue = queue.Queue()
        self.ready = threading.Event()
        self.speed = "normal"
        self.stopped = False

    def callbacks(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def error(self, event):
        pass

    def handler(self):
        while not self.stopped:
            e = self.queue.get()
            if not e:
                break
            try:
                self.callbacks(e)
            except Exception as ex:
                e = Event()
                e.type = "error"
                e.exc = get_exception()
                self.error(e)

    def initialize(self):
        Bus.add(self)

    def put(self, e):
        self.queue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def restart(self):
        self.stop()
        self.start()        

    def start(self):
        self.initialize()
        self.stopped = False
        launch(self.handler)
        return self

    def stop(self):
        self.stopped = True
        e = Event()
        e.type = "end"
        self.queue.put(e)

    def wait(self):
        self.ready.wait()

def docmd(hdl, obj):
    obj.parse()
    f = hdl.getcmd(obj.cmd)
    if f:
        f(obj)
        obj.show()
    obj.ready()

def end(hdl, obj):
    raise ENOMORE
