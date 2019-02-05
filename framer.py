import os
import cv2
import multiprocessing as mp

class frame_generator(object):
    def __init__(self, stream_queue, frame_q):
        self.frame_q = frame_q
        self.stream_queue = stream_queue

    #@classmethod
    def get_frames(self):
        for stream_q in self.stream_queue:
            fp = mp.Process(self.splitter, args=(self.stream_queue,))
            fp.start()

    def splitter(self, stream_data):
        if stream_data == None:
            return
        stream_id ,stream_file = stream_data
        success, frame = cv2.VideoCapture(stream_file)
        while success:
            self.frame_q.put((stream_id, frame))
            success, frame = cv2.VideoCapture(stream_file)

class frame_task(object):
    def __init__(self, frame_queue, stream_queue):
        self.frame_queue = frame_queue
        self.stream_queue = stream_queue

    def __call__(self):
        stream_frame = self.stream_queue.get()
        self.frame_queue.put(stream_frame)

    def __str__(self):
        return self.frame_queue

class frame_generator2(mp.Process):
    def __init__(self, input_queue, frame_queue):
        self.input_queue = input_queue
        self.frame_queue = frame_queue

    def run(self):
        proc_name = self.name
        while True:
           next_task = self.input_queue
           print(proc_name, next_task)
           self.input_queue.task_done()





if __name__ == '__main__':
    framer_result = mp.Queue()
    #stream_ids = os.listdir(videos_path)
    streams = 2

    streamer_queue = [mp.Queue() for stream in range(streams)]
    streamer_queue[0].put(('stream1', '/home/rbc-gpu/prajwal/multiprocess_yolo/bakvid/20180818_0100_16-18-20.mp4'))
    streamer_queue[0].put(('stream1', '/home/rbc-gpu/prajwal/multiprocess_yolo/bakvid/20180818_0100_16-18-21.mp4'))
    streamer_queue[1].put(('stream2', '/home/rbc-gpu/prajwal/multiprocess_yolo/bakvid/20180818_0100_16-18-22.mp4'))
    streamer_queue[1].put(('stream2', '/home/rbc-gpu/prajwal/multiprocess_yolo/bakvid/20180818_0100_16-18-23.mp4'))








    framz = frame_generator(streamer_queue, framer_result)
    #streamer = Streamer(folder_path)
    #streams = mp.Process(Streamer.get_files)
    framz.get_frames()
    #streams.start()
    #streams.join()

    while True:
        frame_meta = framer_result.get()
        if frame_meta == None:
            break
        st_id, frame_data = frame_meta
        print(st_id)
