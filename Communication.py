# Communication from Pi to Arduino

import threading
import time, random
#import GUI from guiThread1 as gui

class commThread2(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        print("Comm thread is initialized")

    def run(self):
        #does stuff here
        
        #call start() to execute non-blocking
        while(True):
            print("Comm Thread is running")
            #put code
            time.sleep(2)

            
    def getGraphData():
        data = []
        data = random.sample(range(0, 100), 10)
        return data
