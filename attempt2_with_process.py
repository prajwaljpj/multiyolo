# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:41:07 2019

@author: Armaan Puri 
"""

import os
import multiprocessing
import glob

class Streamer():
    
    def __init__(self, directory):
        self.directory = directory
        
    def latest_provider(self, stream_name, latest_files):                       #stream_name and latest_files are queues. 
        #get latest files, if any.
        files_sent=[]
        while True:
            if len(files_sent)<100:
                newest_file = max(glob.glob(stream_name.get()+"/*"), key=os.path.getctime)
                if str(newest_file) not in files_sent:
                    files_sent.append(str(newest_file))
                    latest_files.put([multiprocessing.current_process().name,stream_name.get(),newest_file])            #put latest files in a queue for FRAMER
                else:
                    continue
            else:   
                files_sent=[]
                continue
        #do something if condition not satisfied. Also start process again once condition satisfies
        
# =============================================================================
#     def get_streams(self):
# #        streamer = Streamer(directory)   ## directory is path to recordings folder
#         n = len(os.listdir(self.directory))  # for each stream, a process would be started
#         myTasks = multiprocessing.Queue()
#         myResults = multiprocessing.Queue()
#         
#         workers = [multiprocessing.Process(target=streamer.latest_provider, args=(myTasks, myResults)) for i in range(n)]
#         
#         for each in workers:
#             each.start()
#         
#         for each in glob.glob(os.path.join(self.directory+"/*")):
#             myTasks.put(each)
#             
#         while n:
#             results = myResults.get()
#             n -= 1
#         
# =============================================================================

if __name__=='__main__':
    streamer = Streamer(path_to_rec)
#    latest = streamer.get_streams()                                         #get queue output to be given to FRAMER
    n = len(os.listdir(streamer.directory))  # for each stream, a process would be started
    myStreams = multiprocessing.Queue()
    myResults = multiprocessing.Queue()
    
    for stream in glob.glob(os.path.join(path_to_rec+"/*")):
        myStreams.put(stream)
    
    workers = [multiprocessing.Process(target=streamer.latest_provider, args=(myStreams, myResults)) for i in range(n)]
    
    for each in workers:
        each.start()
    
    for each in workers:
        each.join()
        
    while n:
        results = myResults.get()
        n -= 1
