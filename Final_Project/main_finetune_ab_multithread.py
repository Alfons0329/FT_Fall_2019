#!/usr/bin/python3
'''
20191227:
This code is used for fine tuning rsi_s > a for buying and rsi_s < b for selling, more strict for better
fitting the data.
'''

import os, sys, threading, time

assert len(sys.argv) == 6, 'Usage: python3 main_finetune_multithread.py <THREAD_CNT> <best_l> <best_s> <precision> <type_eval, 0 for daily, 1 for minutely>'
THREAD_CNT = int(sys.argv[1])
best_l = int(sys.argv[2])
best_s = int(sys.argv[3])
precision = float(sys.argv[4])
type_eval = int(sys.argv[5])
scale =  float(1 / THREAD_CNT)

class mythread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        cnt = self.num
        exe = 'python3 main_finetune_ab.py ' + str(best_l) + ' ' + str(best_s) + ' ' + str(type_eval) + ' ' + str(precision) + ' ' + str(cnt * scale) + ' ' + str((cnt + 1) * scale)
        os.system(exe)

threads = []
for i in range(THREAD_CNT):
    threads.append(mythread(i))
    threads[i].start()

for i in range(THREAD_CNT):
    threads[i].join()

print('finished all')
