import multirpocessing as mp
from yolov3 import YOLOV3


class consumer:
    def __init__(self, inqueue, outqueue):
        self.inqueue = inqueue
        self.outqueue = outqueue

    def run(self):
        next_task = self.inqueue.get()

