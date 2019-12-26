#!/usr/bin/python3
import os, sys, threading, time

assert len(sys.argv) == 5, 'Usage: python3 main_multithread_2.py <THREAD_CNT> <min_search> <max_search> <type_eval, 0 for daily, 1 for minutely>'
THREAD_CNT = int(sys.argv[1])

min_search = int(sys.argv[2])
max_search = int(sys.argv[3])
type_eval = int(sys.argv[4])
scale = (max_search - min_search) // THREAD_CNT

class mythread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        cnt = self.num
        exe = 'python3 main.py ' + str(min_search + cnt * scale) + ' ' + str(min_search + (cnt + 1) * scale) + ' ' + str(type_eval)
        os.system(exe)

threads = []
for i in range(THREAD_CNT):
    threads.append(mythread(i))
    threads[i].start()

for i in range(THREAD_CNT):
    threads[i].join()
    print('thread %d finished'%(i))

print('finished all')
