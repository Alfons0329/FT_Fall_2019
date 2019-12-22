import os, sys, threading, time

THREAD_CNT = int(sys.argv[1])

min_search = 100
max_search = 200
scale = (max_search - min_search) // THREAD_CNT

class mythread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        cnt = self.num
        exe = 'python3 main.py ' + str(min_search + cnt * scale) + ' ' + str(min_search + (cnt + 1) * scale)
        os.system(exe)

threads = []
for i in range(THREAD_CNT):
    threads.append(mythread(i))
    threads[i].start()

for i in range(THREAD_CNT):
    threads[i].join()
    print('thread %d finished'%(i))

print('finished all')
