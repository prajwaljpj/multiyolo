import os
import multiprocessing as mp

class Streamer():
    def __init__(self, folder_path, stream_set):
        self.folder_path = folder_path
        self.stream_set = stream_set

    #@classmethod
    def get_files(self, folders):
        folders = os.listdir(self.folder_path)
        for stream in self.stream_set:
            p = mp.Process(self.get_video, args=(folder, stream))
            p.start()

    def sorted_ls(self, path):
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))

    def get_video(self, folder, stream):
        stream.put(folder.split('/')[-1], sorted_ls(folder))


    def stats(self):
        folder_len = 0
        folders = []
        for _, dirs, files in os.walk(self.folder_path):
            folder_len += len(dirs)
            for folder in dirs:
                folders.append(folder)



