# This file is placed in the Public Domain.

import queue
import sys
import threading

from bus import Bus
from err import Restart, Stop
from evt import Command, Event
from obj import Object
from tbl import Table
from thr import launch
from trc import get_exception

class Handler(Object):

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.queue = queue.Queue()
        self.iqueue = queue.Queue()
        self.oqueue = queue.Queue()
        self.ready = threading.Event()
        self.speed = "normal"
        self.started = threading.Event()
        self.stopped = threading.Event()
        self.istopped = threading.Event()
        self.ostopped = threading.Event()

    def callbacks(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    @staticmethod
    def dispatch(hdl, obj):
        obj.parse()
        f = Table.getcmd(obj.cmd)
        if f:
            f(obj)
            obj.show()
        sys.stdout.flush()
        obj.ready()

    def error(self, event):
        pass

    def event(self, txt):
        if txt is None:
            return txt
        c = Command()
        c.txt = txt or ""
        c.orig = self.__dorepr__()
        return c

    def handle(self, e):
        self.queue.put(e)

    def dispatcher(self):
        dorestart = False
        self.stopped.clear()
        while not self.stopped.isSet():
            e = self.queue.get()
            try:
                self.callbacks(e)
            except Restart:
                dorestart = True
                break
            except Stop:
                break
            except Exception as ex:
                e = Event()
                e.type = "error"
                e.exc = get_exception()
                self.error(e)
        if dorestart:
            self.restart()

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

    def restart(self):
        self.stop()
        self.start()

    def say(self, channel, txt):
        self.raw(txt)

    def put(self, e):
        self.iqueue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        self.register("cmd", Handler.dispatch)
        Bus.add(self)
        launch(self.dispatcher)
        launch(self.handler)
        return self

    def stop(self):
        self.stopped.set()
        self.iqueue.put(None)
        self.oqueue.put(None)

    def wait(self):
        self.ready.wait()
