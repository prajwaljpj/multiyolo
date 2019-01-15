import os
import cv2
import multiprocessing as mp

class frame_generator(object):
    def __init__(self, stream):
        self.frame_q = mp.Queue()
    def splitter(self):
        if stream_data = None:
            continue
        stream_id , stream_file = stream_data
        success, frame = cv2.VideoCapture(stream_file)

        while success:
                self.frame_q.put((stream_id, frame))
                success, frame = cv2.VideoCapture(stream_file)


class consumer(mp.Process):
    def __init__(self):
        pass

class Streamer():
    def __init__(self, folder_path, stream_set):
        self.folder_path = folder_path



    results = multiprocessing.Queue()
    streamer = Streamer(folder_path)
    streams = mp.Process(Streamer.get_files)

    streams.start()


