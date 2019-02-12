import os
import cv2
import multiprocessing as mp


class framer(mp.Process):
    def __init__(self,input_queue, output_queue):
        mp.Process.__init__(self)
        print("initialized init of multiprocess")
        self.input_queue= input_queue
        self.output_queue= output_queue

    def run(self):
        proc_name = self.name
        print("Run initiated for proc: {}".format(proc_name))
        while True:
            stream_name, next_file = self.input_queue.get()
            print("asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf: ", stream_name)
            if next_file is None:
                print("Exiting stream in {}".format(proc_name))
                # self.input_queue.task_done()
                break
            print(proc_name, next_file)
            frames_gen = frame_generator(next_file)
            for frame in frames_gen:
                if frame is None:
                    continue
                # print(frame)
                self.output_queue.put((stream_name, frame),)
            # self.input_queue.task_done()
        return


class frame_generator(object):
    def __init__(self, input_data):
        print("Initialised frame_generator (should happen only once)")
        self.filename = input_data
        self.cap = cv2.VideoCapture(self.filename)
        print("filename: {}".format(self.filename))

    def __iter__(self):
        print("iter obj happen only once")
        ret = True
        while ret:
            ret, frame = self.cap.read()
            yield frame


def fmr(inqueue, outqueue):
    inlen = len(inqueue)

    consumers = [framer(inqueue[x], outqueue[x]) for x in range(inlen)]
    print(consumers)
    [w.start() for w in consumers]
    # while True:
        # print(outqueue[0].get())
    return
    # return (inqueue, outqueue)

if __name__ == '__main__':

    #stream_ids = os.listdir(videos_path)
    streams = 2
    manager = mp.Manager()
    framer_result = [manger.Queue() for stream in range(streams)]
    inqueuelist = [manger.Queue() for stream in range(streams)]
    inqueuelist[0].put(('stream1', '/home/prajwaljpj/projects/multiyolo/video/bakvid/20180818_0100_16-18-20.mp4'))
    inqueuelist[0].put(('stream1', '/home/prajwaljpj/projects/multiyolo/video/bakvid/20180818_0100_16-18-21.mp4'))
    inqueuelist[1].put(('stream2', '/home/prajwaljpj/projects/multiyolo/video/bakvid/20180818_0100_16-18-22.mp4'))
    inqueuelist[1].put(('stream2', '/home/prajwaljpj/projects/multiyolo/video/bakvid/20180818_0100_16-18-23.mp4'))

    fmr(inqueuelist, framer_result)

    print(framer_result[0].get())

