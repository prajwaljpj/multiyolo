# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:41:07 2019

@author: Armaan Puri 
"""

import os
import multiprocessing
import glob
import time
import sched
import configparser
from multiprocessing import Event 

class Streamer():
	
	def __init__(self, directory, wait, list_length):
		self.directory = directory
		self.wait = wait
		self.list_length = list_length
	
	def simpler(self, stream_name, f_q,  wait, list_length):
		known_latest = []
		path = str(stream_name) #.get()
		multiprocessing.current_process().name = path
		print(multiprocessing.current_process())
		try:
			while True:
				if os.path.isdir(path) and len(os.listdir(path))>0:
					newest_file = max(glob.glob(path+"/*"), key=os.path.getctime)
				else:
					print("Stream folder {} has been removed or is empty.".format(multiprocessing.current_process().name))
					break
				if len(known_latest)<list_length:
					if str(newest_file) not in known_latest:
						known_latest.append(str(newest_file))
						f_q.put(newest_file)
						print("writing to queue done, releasing lock")
						# print("here's the output", f_q)
					else:
						print("waiting for {} file now...".format(multiprocessing.current_process().name))
						time.sleep(wait)
						continue
				else:
					known_latest=[]
		except KeyboardInterrupt:
			print("Stopped by user")

	def spawner(self, toggle, path, qs_list):
		qs_list.append(multiprocessing.Queue())
		multiprocessing.Process(target=self.simpler, args=(path, qs_list[-1], wait, list_length))
		toggle.clear()
		return

	def indefinite_checker(self, n, final_q):
		# multiprocessing.current_process().name = path
		print(multiprocessing.current_process())
		try:
			while True:
				new_len = len(os.listdir(self.directory))
				new_workers = []
				if new_len > n:
					for i in range(n,new_len):
						final_q.append(multiprocessing.Queue())
						myStreams = os.listdir(self.directory)
						myStreams = [path_to_rec+"/"+'{}'.format(element) for element in myStreams]
						work = multiprocessing.Process(target=self.simpler, args=(myStreams[i],final_q[i], wait, list_length)) 
						work.start()
						new_workers.append(work)
						break
				else:
					# print("elsed fine")
					pass
		except KeyboardInterrupt:
			print("checking stopped, by user")

	def execute(self):
		myStreams = os.listdir(self.directory)
		myStreams = [self.directory+"/"+'{}'.format(element) for element in myStreams]

		n = len(os.listdir(self.directory))   #for each stream, a process would be started 
		final_q = []    # initializing n queues, for each stream, this list is the final OUTPUT
		for i in range(n):
			final_q.append(multiprocessing.Queue())


		workers = []
		processes = {}
		m=0
		
		# n=int(return_num.value)

		for i in range(n):
			work = multiprocessing.Process(target=self.simpler, args=(myStreams[i],final_q[i], self.wait, self.list_length)) 
			work.start()
			processes[n] = (work, i)
			m+=1
			workers.append(work)

		checker = multiprocessing.Process(target=self.indefinite_checker, args=(n, final_q))
		checker.start()
		
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
	  
		# for i in range(n):
		#     print("Final queue containing queues for each stream: ", final_q.get())
		# event = Event()
		
		# signal.signal()
		# 	event.set()
		# 	streamer.spawner(event, new_stream_path, final_q)

		for worker in workers:
			if not worker.is_alive():
				print("Joining the process before restarting.\n")
				worker.join()
				time.sleep(2)
				print("Restarting process.")
				worker.start()
				continue
			else:
				pass

if __name__=='__main__':
	config = configparser.ConfigParser()
	config.read('./config.ini')
	streamer = Streamer(config["DEFAULT"]["path_to_rec"], int(config["DEFAULT"]["wait_time"]), int(config["DEFAULT"]["list_length"]))
	streamer.execute()
