#!/usr/bin/env python3
# Communication from Pi to Arduino
import threading
import time, random
from GUI import guiThread1 as gui

class commThread2(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        print("Comm thread is initialized")

    def run(self):
        #call start() to execute non-blocking
        while(True):
            print("Comm Thread is running")
            gui.testGUI()
            time.sleep(2)
            
    def testComm(): print('comm function call is working')
            
    def getGraphData():
        data = []
        data = random.sample(range(0, 100), 10)
        return data
