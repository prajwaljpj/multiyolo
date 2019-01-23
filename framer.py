import os
import cv2
import multiprocessing as mp
from Streamer import Streamer

class frame_generator(object):
    def __init__(self, stream_queue, frame_q):
        self.frame_q = frame_q
        self.stream_queue = stream_queue

    #@classmethod
    def get_frames(self):
        for stream_q in self.stream_queue:
            fp = mp.Process(self.splitter, args=(self.stream_queue))
            fp.start()

    def splitter(self, stream_data):
        if stream_data == None:
            return
        stream_id ,stream_file = stream_data
        success, frame = cv2.VideoCapture(stream_file)

        while success:
                self.frame_q.put((stream_id, frame))
                success, frame = cv2.VideoCapture(stream_file)


if __name__ == '__main__':
    results = multiprocessing.Queue()
    streamer = Streamer(folder_path)
    streams = mp.Process(Streamer.get_files)

    streams.start()


