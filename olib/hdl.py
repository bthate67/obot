# This file is placed in the Public Domain.

import queue
import threading

from bus import Bus
from evt import Event
from obj import Object
from thr import launch
from trc import get_exception

class Handler(Object):

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.queue = queue.Queue()
        self.ready = threading.Event()
        self.speed = "normal"
        self.started = threading.Event()
        self.stopped = threading.Event()

    def callbacks(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def error(self, event):
        pass

    def handler(self):
        dorestart = False
        self.stopped.clear()
        while not self.stopped.isSet():
            e = self.queue.get()
            try:
                self.callbacks(e)
            except RestartError:
                dorestart = True
                break
            except StopError:
                break
            except Exception as ex:
                e = Event()
                e.type = "error"
                e.exc = get_exception()
                self.error(e)
        if dorestart:
            self.restart()

    def initialize(self):
        Bus.add(self)

    def put(self, e):
        self.queue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def restart(self):
        pass

    def start(self):
        self.initialize()
        self.stopped.clear()
        launch(self.handler)
        return self

    def stop(self):
        self.stopped.set()
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
    raise StopError
