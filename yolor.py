import multirpocessing as mp
from yolov3 import YOLOV3


class consumer:
    def __init__(self, inqueue, outqueue):
        self.inqueue = inqueue
        self.outqueue = outqueue

    def run(self):
        proc_name = self.name
        print("Process for yolor: {}".format(proc_name))
        while True:
            fmr_data = self.inqueue.get()
            if fmr_data is None:
                print("Exiting stream in {}".format(proc_naem))
                break

            yolo_data = yv3detector(fmr_data)
            self.outqueue.put((fmr_data, yolo_data),)

        return


def yv3detector():
    pass



if __name__ == '__main__':
    manager = mp.Manager()

    streams = 2
    framer_queues = [manager.Queue() for stream in range(streams)]
    yolo_out_queues = [manager.Queue() for stream in range(streams)]

    yolov3 = YOLOV3("cfg/yolo_2k_reanchored.cfg", "weights/yolo_2k_reanchored_70000.weights", "cfg/2k_aug.data")
