import os, sys, threading, time

THREAD_CNT = int(sys.argv[1])

min_search = 0
max_search = 25
scale = (max_search - min_search) // THREAD_CNT

class mythread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        cnt = self.num
        exe = 'python3 main.py ' + str(min_search + cnt * scale) + ' ' + str(min_search + (cnt + 1) * scale)
        print('exe ', exe)
        os.system(exe)
        print('thread %d finished'%(cnt))

threads = []
for i in range(THREAD_CNT):
    threads.append(mythread(i))
    threads[i].start()

for i in range(THREAD_CNT):
    threads[i].join()

print('finished all')
