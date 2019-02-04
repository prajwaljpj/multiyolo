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
        
    def latest_provider(self, stream_name, outputq):
        #get latest files, if any.
        files_sent=[]
        while True:
            if len(files_sent)<100:
                latest_file = max(glob.glob(stream_name.get()+"/*"), key=os.path.getctime)
                if latest_file not in files_sent:
                    files_sent.append(str(latest_file))
                    outputq.put(latest_file)                                         #put latest files in a queue for FRAMER
                else:
                    continue
            else:   
                files_sent=[]
                continue
        #do something if condition not satisfied. Also start process again once condition satisfies
        
    def get_streams(self): #os.listdir("recordings")                           ###### check how to output multiprocessing stream output
        p = multiprocessing.Pool(processes=len(os.listdir(self.directory)))    ###### add handle for process dying.sum(os.path.isdir(i) for i in os.listdir(path))
        streams = p.imap(target=self.latest_provider, args=(glob.glob(os.path.join(self.directory+"/*")),))
        q = multiprocessing.Queue()
        
        #put retrieved streams in a queue
    
    def check_latest(stream_name):
        pass
        

if __name__=='__main__':
    streamer = Streamer(directory)
    latest = streamer.get_streams()

