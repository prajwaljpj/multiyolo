import os
import multiprocessing as mp
import time
import sys
import glob
import cv2
from yolov3 import YOLOV3
# yolov3 = YOLOV3("cfg/yolo_2k_reanchored.cfg", "weights/yolo_2k_reanchored_70000.weights", "cfg/2k_aug.data")


# lock = None

# def init(_lock):
        # global lock
        # lock = _lock

class yolo_load(mp.Process):
        def __init__(self,task_queue, result_queue):
                mp.Process.__init__(self)
                self.yolo_task_q = task_queue
                self.yolo_result_q = result_queue

        def run(self):
                proc_name = self.name
                print("new_proc {}".format(proc_name))
                while True:
                        next_yolo_task = self.yolo_task_q.get()
                        print("got next task:{}".format(next_yolo_task))
                        if next_yolo_task is None:
                                print("exiting {}".format(proc_name))
                                self.yolo_task_q.task_done()
                                break
                        # with lock:
                        results = next_yolo_task()
                        print(proc_name, results)
                        self.yolo_task_q.task_done()
                        self.yolo_result_q.put(results)

class yolo_task(object):
        def __init__(self, stream_id, lock, yv3):
                #provide yolo arguments
                self.lock = lock
                self.stream_id = stream_id
                # self.capture = cv2.VideoCapture(stream_id)

        @classmethod
        def analytics(yolo_task):
                # read from stream_id
                print("initiating video capture")
                capture = cv2.VideoCapture(self.stream_id)
                success, yolo_frame= capture.read()
                results_set_for_video = []
                while success:
                        with self.lock:
                                out_scores, out_boxes, out_classes = yolo_task.yv3.detect_image(yolo_frame)
                        results_set_for_video.append((out_scores, out_boxes, out_classes))
                        success , yolo_frame = capture.read()
                        print(results_set_for_video)
                return results_set_for_video

        def __call__(self):
                #  results_set = self.analytics()
                # results = yolov3.run()
                return results_set
        def __str__(self):
                return "{}".format(self.stream_id)

# def load_model(cfg_path,weights_path,data_path):
        # net = load_net(cfg_path,weights_path, 0)
        # meta = load_meta(data_path)

if __name__ == '__main__':
        mp.set_start_method('spawn')
        # establish queues
        m = mp.Manager()
        lock = mp.Lock()
        tasks = mp.JoinableQueue()
        results = mp.Queue()
        filepath = sys.argv[1]

        yv3 = YOLOV3("cfg/yolo_2k_reanchored.cfg", "weights/yolo_2k_reanchored_70000.weights", "cfg/2k_aug.data")
        # fchkr = folder_checker()
        #start consumers
        # number_consumers = mp.cpu_count() * 2
        number_consumers = 2
        print("cpu count = {}".format(number_consumers))

        consumers = [
                        yolo_load(tasks, results)
                        for i in range(number_consumers)
                        ]
        # print(consumers)
        for w in consumers:
                # print(w)
                w.start()

        streams = glob.glob(os.path.join(filepath, '*'))

        for strm in streams:
                tasks.put(yolo_task(strm, lock, yv3))
        for i in range(number_consumers):
                tasks.put(None)
        tasks.join()
        while number_consumers:
                result = results.get()
                print(result[0])
                number_consumers-=1

