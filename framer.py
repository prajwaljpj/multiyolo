import os
import cv2
import multiprocessing as mp

class frame_generator(object):
    def __init__(self, stream_queue):
        self.frame_q = mp.Queue()

    @classmethod
    def get_frames(self):
        for stream_q in stream_queue:
            fp = mp.Process(self.splitter, args=(frame_q))



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

    @classmethod
    def get_files(self, folders):
        for stream in stream_set:
            p = mp.Process(self.get_video, args=(folder, stream))
            p.start()

    def sorted_ls(path):
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))

    def get_video(self, folder, stream):
        stream.put(folder.split('/'), sorted_ls(folder))


    def stats(self):
        folder_len = 0
        folders = []
        for _, dirs, files in os.walk(self.folder_path)
            folder_len += len(dirs)
            for folder in dirs:
                folders.append(folder)




if __name__ == '__main__':
    results = multiprocessing.Queue()
    streamer = Streamer(folder_path)
    streams = mp.Process(Streamer.get_files)

    streams.start()


