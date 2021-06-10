# This file is placed in the Public Domain.

import hdl
import queue
import thr
import utl

class Client(hdl.Handler):

    def __init__(self):
        super().__init__()
        self.iqueue = queue.Queue()
        self.stopped = False
        self.running = False

    def announce(self, txt):
        self.raw(txt)

    def cmd(self, txt):
        e = Command()
        e.orig = self.__dorepr__()
        e.txt = txt
        return hdl.docmd(c, e)

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
        thr.launch(self.input)

    def stop(self):
        self.running = False
        self.stopped = True
        self.iqueue.put(None)
        super().stop()

class CLI(Client):

    def error(self, e):
        utl.cprint(e.exc)
        raise RestartError

    def raw(self, txt):
        utl.cprint(txt)

class Console(CLI):

    def handle(self, e):
        self.put(e)
        e.wait()

    def poll(self):
        return input("> ")

    def start(self):
        self.register("cmd", krn.kcmd)
        super().start()
