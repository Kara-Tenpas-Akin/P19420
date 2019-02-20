# Communication from Pi to Arduino

import threading
import time

class commThread2(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        print("Comm thread is initialized")

    def run(self):
        #does stuff here

        #csll start() to execute non-blocking
        while(True):
            print("Comm Thread is running")
            #put code
            time.sleep(2)
