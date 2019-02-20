# Main File
# Run GUI.py and Communition.py

#!/usr/bin/env python3

from threading import Timer
from guiThread1 import Thread1
from commThread2 import Thread2

guiThread = Thread1('guiThread1')  
guiThread.start()   #starts new thread and continues (non-blocking)
guiThread.run()     #calls run in this same thread (blocking)

commThread = Thread2('commThread2')
commThread.start() #starts new thread and continues (non-blocking)
commThread.run()   #calls run in this same thread (blocking)

"""if__name__== "__main__":
run()"""
