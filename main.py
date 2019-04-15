# Main File
# Run GUI.py and Communition.py

#!/usr/bin/env python3

from threading import Timer
from GUI import guiThread1
from Communication import commThread2
from queue import Queue

myqueue = Queue()

guiThread = guiThread1('guiThread1',myqueue)  
guiThread.start()   #starts new thread and continues (non-blocking)
print("gui started,starting comm")
commThread = commThread2('commThread2',myqueue)
commThread.start() #starts new thread and continues (non-blocking)


"""if__name__== "__main__":
run()"""
