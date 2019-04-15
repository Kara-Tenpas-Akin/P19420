#!/usr/bin/env python3
# Communication from Pi to Arduino
import threading
import time, random
from queue import Queue


class commThread2(threading.Thread):
    def __init__(self,name, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.commQueue = threadQueue
        print("Comm thread is initialized")

    def run(self):
        #call start() to execute non-blocking
        while(True):
            # put code here
            time.sleep(2)
            
    def testComm(): print('comm function call is working')
            
    def getGraphData():
        data = random.sample(range(0, 100), 1)
        return data
