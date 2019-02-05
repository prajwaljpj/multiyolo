# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:41:07 2019

@author: Armaan Puri 
"""

import os
import multiprocessing
import glob
import time
import configparser

class Streamer():
    
    def __init__(self, directory):
        self.directory = directory
    
    def simpler(self, l, stream_name, latest_files, wait, list_length):
        known_latest = []           #
        print(multiprocessing.current_process())
        path = stream_name.get()
        # count = 0   
        try:
            while True:
                newest_file = max(glob.glob(path+"/*"), key=os.path.getctime)
                # print(newest_file)
                # print(path)
                # count+=1
                # print("Finding newest_file", count)
                if len(known_latest)<100:
                    if str(newest_file) not in known_latest:         #
                        l.acquire()
                        known_latest.append(str(newest_file))
                        latest_files.put(newest_file)
                        print("written to queue, releasing lock")
                        l.release()
                    else:
                        print("waiting for file now...")
                        # print(latest_files.get())
                        # print("The output queue is empty?",latest_files.empty())
                        time.sleep(wait)
                        continue
                else:
                    known_latest=[]
        except KeyboardInterrupt:
            print("Stopped by user")

    def check_status(self, workers_ls):
        # for worker in workers_ls:
        if worker.is_alive() == False:
            worker.start()
        else:
            pass

if __name__=='__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    path_to_rec = config["DEFAULT"]["path_to_rec"]
    wait = int(config["DEFAULT"]["wait_time"])
    list_length = int(config["DEFAULT"]["list_length"])

    streamer = Streamer(path_to_rec)
    myStreams = multiprocessing.Queue()
    myResults = multiprocessing.Queue()
    lock = multiprocessing.Lock()
    for stream in glob.glob(os.path.join(path_to_rec+"/*")):
        myStreams.put(stream)
    # workers = [multiprocessing.Process(target=streamer.latest_provider, args=(lock, myStreams, myResults)) for i in range(n)]
    n = len(os.listdir(streamer.directory))  # for each stream, a process would be started 
    workers = []
    processes = {}
    m=0
    
    for i in range(n):
        work = multiprocessing.Process(target=streamer.simpler, args=(lock, myStreams, myResults, wait, list_length))
        work.start()
        processes[n] = (work, i)
        m+=1
        workers.append(work)
    
    # for each in workers:
    #     print("Let's join workers")
    #     each.join()

    # while len(processes) > 0:
    #     for x in processes.keys():
    #         (p, a) = processes[x]
    #         time.sleep(0.5)
    #         if p.exitcode is None and not p.is_alive(): # Not finished and not running
    #              # Do your error handling and restarting here assigning the new process to processes[n]
    #              print(a, 'is gone as if never born!')
    #         elif p.exitcode < 0:
    #             print ('Process Ended with an error or a terminate', a)
    #             # Handle this either by restarting or delete the entry so it is removed from list as for else
    #         else:
    #             print (a, 'finished')
    #             p.join() # Allow tidyup
    #             del processes[x] # Removed finished items from the dictionary 
    #             # When none are left then loop will end

    # for worker in workers:
    #     check = multiprocessing.Process(target=streamer.check_status, args=(worker,))
    #     check.start()

    for worker in workers:
        if worker.is_alive() == False:
            worker.start()
            continue
        else:
            pass

    for i in range(n):
        print(myResults.get())
