#!/usr/bin/env python3
# Main File
# Run GUI.py and Communition.py
from threading import Timer
from GUI import guiThread1
from Communication import commThread2
from queue import Queue

com2guiQueue = Queue()
gui2comQueue = Queue()

guiThread = guiThread1('guiThread1',com2guiQueue, gui2comQueue)  
guiThread.start()   #starts new thread and continues (non-blocking)
commThread = commThread2('commThread2',com2guiQueue, gui2comQueue)
commThread.start() #starts new thread and continues (non-blocking)


"""if__name__== "__main__":
run()"""
