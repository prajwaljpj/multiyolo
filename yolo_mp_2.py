import os
import cv2
from yolov3 import YOLOV3
import multiprocessing as mp
import time
import sys
import glob

class process_instance(mp.Process):
    def __init__(self, task_queue, result_queue):
        mp.Process.__init__(self)
        self.yolo_task_q = task_queue
        self.yolo_result_q = result_queue

    def run(self):
        proc_name = self.name
        print("new_proc {}".format(proc_name))
        while True:
            next_yolo_task = self.yolo_task_q.get()
            print("got next task: {}".format(proc_name))
            if next_yolo_task is None:
                print("exiting {}".format(proc_name))
                self.yolo_task_q.task_done()
                break
            results = next_yolo_task()
            print(proc_name, results)
            self.yolo_task_q, task_done()
            self.yolo_result_q.put(results)


def yolo_task(stream_id, yolov3, lock):
    capture = cv2.VideoCapture(stream_id)
    success, yolo_frame = capture.read()
    result_set_for_video = []
    while success:
        #with lock:
        print("stream id :{}".format(stream_id))
        out_scores, out_boxes, out_classes = yolov3.detect_image(yolo_frame)
        result_set_for_video.append((out_scores, out_boxes, out_classes))
        success, yolo_frame = capture.read()
        #print(result_set_for_video)
    return (stream_id, result_set_for_video)

if __name__=="__main__":
    m = mp.Manager()
    lock = m.Lock()
    tasks = mp.JoinableQueue()
    results = mp.Queue()
    filepath = sys.argv[1]

    yolov3 = YOLOV3("cfg/yolo_2k_reanchored.cfg", "weights/yolo_2k_reanchored_70000.weights", "cfg/2k_aug.data")
    number_consumers = mp.cpu_count() * 2
    print("number of consumers: {}".format(number_consumers))
    consumers = [process_instance(tasks, results) for i in range(number_consumers)]

    [w.start() for w in consumers]

    streams = glob.glob(os.path.join(filepath, "*"))

    for strm in streams:
        tasks.put(yolo_task(strm, yolov3, lock))

    for i in range(number_consumers):
        task.put(None)
    task.join()

    while number_consumers:
        result = results.get()
        print(result[-1])
        number_consumers-=1
