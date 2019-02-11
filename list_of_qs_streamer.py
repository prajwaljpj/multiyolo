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
import signal

class Streamer():
	
	def __init__(self, directory, wait, list_length, final_q):
		self.directory = directory
		self.wait = wait
		self.list_length = list_length
		self.final_q = final_q
	
	def simpler(self, stream_name, f_q,  wait, list_length):
		# signal.signal(signal.SIGINT, signal.SIG_IGN)
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
						print("writing to queue done for {}".format(multiprocessing.current_process().name))
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

	def indefinite_checker(self, streams, n, final_q):
		# signal.signal(signal.SIGINT, signal.SIG_IGN)
		multiprocessing.current_process().name = "indefinite checker"
		print(multiprocessing.current_process())
		try:
			while True:
				newstreams = os.listdir(self.directory)
				newstreams = [self.directory+"/"+'{}'.format(element) for element in newstreams]
				new_workers = []
				for i, name in enumerate(list(set(newstreams)^set(streams))):
					streams=newstreams
					print("new stream detected.")
					time.sleep(1)
					final_q.append(multiprocessing.Queue())
					work = multiprocessing.Process(target=self.simpler, args=(name,final_q[n+i], self.wait, self.list_length)) 
					work.start()
					new_workers.append(work)
					break
		except KeyboardInterrupt:
			print("checking stopped by user")

	def execute(self):
		myStreams = os.listdir(self.directory)
		myStreams = [self.directory+"/"+'{}'.format(element) for element in myStreams]

		n = len(os.listdir(self.directory))   #for each stream, a process would be started 
		self.final_q = []    # initializing n queues, 1 for each stream, this list is the final OUTPUT
		for i in range(n):
			self.final_q.append(multiprocessing.Queue())

		workers = []
		processes = {}
		m=0


		for i in range(n):
			work = multiprocessing.Process(target=self.simpler, args=(myStreams[i],self.final_q[i], self.wait, self.list_length)) 
			work.start()
			processes[n] = (work, i)
			m+=1
			workers.append(work)

		checker = multiprocessing.Process(target=self.indefinite_checker, args=(myStreams, n, self.final_q))
		checker.start()

		for worker in workers:
			if not worker.is_alive():
				print("Joining dead {} *****\n".format(worker.name))
				worker.join()

def call_streamer():
	config = configparser.ConfigParser()
	config.read('./config.ini')
	streamer = Streamer(config["DEFAULT"]["path_to_rec"], int(config["DEFAULT"]["wait_time"]), int(config["DEFAULT"]["list_length"]), [])
	streamer.execute()
	# print(streamer.final_q) ## streamer.final_q is the list of queues	

if __name__=='__main__':
	call_streamer()