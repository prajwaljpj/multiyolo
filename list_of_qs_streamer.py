# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:41:07 2019

@author: Armaan Puri 
"""

import os
import numpy as np
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
		self.myStreams = os.listdir(self.directory)
		self.myStreams = [self.directory+"/"+'{}'.format(element) for element in self.myStreams]
		self.n = len(os.listdir(self.directory))
	
	def simpler(self, stream_name, f_q,  wait, list_length):
		signal.signal(signal.SIGTSTP, signal.SIG_IGN)
		known_latest = []
		path = str(stream_name) #.get()
		multiprocessing.current_process().name = path
		print(multiprocessing.current_process())
		try:
			while True:
				# print(os.getpid())
				if os.path.isdir(path) and len(os.listdir(path))>0:
					newest_file = max(glob.glob(path+"/*"), key=os.path.getctime)
				else:
					print("Stream folder {} has been removed or is empty.".format(multiprocessing.current_process().name))
					try:
						print("removing:", path)
						self.myStreams.remove(path)
					except:
						print("Removed from streams already.")
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

	def checker(self):
		# signal.signal(signal.SIGTSTP, signal.SIG_IGN)
		multiprocessing.current_process().name = "checker"
		print(multiprocessing.current_process())
		try:
			newstreams = os.listdir(self.directory)
			newstreams = [self.directory+"/"+'{}'.format(element) for element in newstreams]
			new_workers = []
			oldstreams = self.myStreams
			self.myStreams = newstreams
			for i, name in enumerate(list(set(newstreams)^set(oldstreams))):
			# for i, name in enumerate(list(np.setdiff1d(newstreams, oldstreams))):
				# self.myStreams.append((set(newstreams)^set(self.myStreams)))
				print("new stream(s) {} detected.".format((set(newstreams)^set(oldstreams))))
				# time.sleep(1)
				self.final_q.append(multiprocessing.Queue())
				work = multiprocessing.Process(target=self.simpler, args=(name,self.final_q[self.n+i], self.wait, self.list_length))
				# work.daemon = True
				work.start()
				new_workers.append(work)
				# break
		except KeyboardInterrupt:
			print("checking stopped by user")

	def handler(self, signum, frame):
		print("Checking for new streams now.")
		checker = multiprocessing.Process(target=self.checker, args=())
		checker.start()
		checker.join()
		print("checker done and joined.")

	def execute(self):
		   #for each stream, a process would be started 
		self.final_q = []    # initializing n queues, 1 for each stream, this list is the final OUTPUT
		for i in range(self.n):
			self.final_q.append(multiprocessing.Queue())

		workers = []
		processes = {}
		m=0

		try:
			for i in range(self.n):
				work = multiprocessing.Process(target=self.simpler, args=(self.myStreams[i],self.final_q[i], self.wait, self.list_length))
				# signal.signal(signal.SIGQUIT, self.handler)
				# work.daemon = True
				work.start()
				processes[i] = (work, i)
				m+=1
				workers.append(work)

			
			for worker in workers:
				if not worker.is_alive():
					print("Joining dead {} *****\n".format(worker.name))
					worker.join()
		except KeyboardInterrupt:
			for worker in workers:
				worker.join()

def call_streamer():
	config = configparser.ConfigParser()
	config.read('./config.ini')
	streamer = Streamer(config["DEFAULT"]["path_to_rec"], int(config["DEFAULT"]["wait_time"]), int(config["DEFAULT"]["list_length"]), multiprocessing.Manager().list())
	signal.signal(signal.SIGTSTP, streamer.handler)
	streamer.execute()

	# print(streamer.final_q) ## streamer.final_q is the list of queues	

if __name__=='__main__':
	call_streamer()
