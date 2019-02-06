import multiprocessing as mp
import glob
import os

def f(x):
	files_sent=[]
	count=0
	new = 0
	while True:
		latest_file = max(glob.glob(x+"/*"), key=os.path.getctime)
		count +=1
		print(count)
		if len(files_sent)<100:
			# print("files_sent:"+str(len(files_sent)))
			if str(latest_file) not in files_sent:
				files_sent.append(str(latest_file))
				f.q.put(latest_file)                                         #put latest files in a queue for FRAMER
				

			else:
				print(2)

				pass
		else:   
			files_sent=[]
			print(3)
			# pass

def f_init(q):
	f.q = q

def main(path_to_rec):
	jobs = glob.glob(os.path.join(path_to_rec+"/*"))

	q = mp.Queue()
	p = mp.Pool(None, f_init, [q])
	results = p.imap(f, jobs)
	# p.join()
	# p.close()

	for i in range(len(jobs)):
		print(q.get())
		# print(results.next())
	# [print(i) for i in results]

if __name__ == '__main__':
	path_to_rec = "/mnt/f/IISc_Big/recordings/"
	main(path_to_rec)