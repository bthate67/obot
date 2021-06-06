# This file is placed in the Public Domain.

import queue

from lst import List
from obj import Object
from thr import launch

class Output(Object):

    cache = List()

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()

    @staticmethod
    def append(channel, txtlist):
        if channel not in Output.cache:
            Output.cache[channel] = []
        Output.cache[channel].extend(txtlist)

    def dosay(self, channel, txt):
        pass

    def oput(self, channel, txt):
        self.oqueue.put_nowait((channel, txt))

    def output(self):
        while not self.stopped:
            (channel, txt) = self.oqueue.get()
            if self.stopped or channel is None:
                break
            self.dosay(channel, txt)

    @staticmethod
    def size(name):
        if name in Output.cache:
            return len(Output.cache[name])
        return 0

    def start(self):
        self.stopped = False
        launch(self.output)
        return self

    def stop(self):
        self.stopped = True
        self.oqueue.put_nowait((None, None))
