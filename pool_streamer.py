# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 10:16:19 2019

@author: Armaan Puri 
"""
import os
import multiprocessing
import glob

class Streamer():
    
    def __init__(self, directory):
        self.directory = directory
    
    def latest_provider(self, stream_name):
        # get latest files, if any.
        files_sent=[]
        try:
            while True:
                if len(files_sent)<100:
                    latest_file = max(glob.glob(stream_name.get()+"/*"), key=os.path.getctime)
                    if str(latest_file) not in files_sent:
                        files_sent.append(str(latest_file))
                        self.latest_provider.q.put(latest_file)                                         #put latest files in a queue for FRAMER
                        print(1)
                    else:
                        continue
                else:   
                    files_sent=[]
                    print(2)
                    continue
        except KeyboardInterrupt:
            print("Stopped by User")
        # do something if condition not satisfied. Also start process again once condition satisfies

    def latest_provider_init(self, q):
        self.latest_provider.q = q
        
    def get_streams(self): #os.listdir("recordings")                           ###### check how to output multiprocessing stream output
        q = multiprocessing.Queue()
        p = multiprocessing.Pool(len(os.listdir(self.directory)), self.latest_provider_init, [q])    ###### add handle for process dying.sum(os.path.isdir(i) for i in os.listdir(path))
        streams = p.imap(self.latest_provider, (glob.glob(os.path.join(self.directory+"/*")),))
        p.close()

        for i in range(len(os.listdir(self.directory))):
            print(q.get())
            print(streams.next())
        
        # put retrieved streams in a queue
    
    def check_latest(stream_name):
        pass
        

if __name__=='__main__':
    directory = "/mnt/f/IISc_Big/recordings"
    streamer = Streamer(directory)
    streamer.get_streams()

