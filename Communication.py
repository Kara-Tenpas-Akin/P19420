#!/usr/bin/env python3
# Communication from Pi to Arduino
import threading
import time, random
from queue import Queue
import serial
import struct
import RPi.GPIO as GPIO
port = '/dev/ttyACM0'

s1 = serial.Serial(port,115200)
s1.flushInput()

Temp1Inside="01-01-01"
Temp1Outside="01-01-02"
Temp1In=0
Temp1Out=0

Moist1="01-02-01"
Moist2="01-02-02"
Moist3="01-02-03"
MLvl1=0
MLvl2=0
MLvl3=0

ErrR1="01-03-01"
ErrR2="01-03-02"
ErrR3="01-03-03"
ErrIn="01-03-04"
ErrOut="01-03-05"

s="1"
data="0"
space="0"
junk1="0"

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,0)
TxReq=0


class commThread2(threading.Thread):
    def __init__(self,name, com2guiQueue, gui2comQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.mycom2guiQueue = com2guiQueue
        self.mygui2comQueue = gui2comQueue
        print("Comm thread is initialized")
        # Comm to GUI
        self.tempIdata = 0
        self.tempOdata = 0
        self.row1data = 0
        self.row2data = 0
        self.row3data = 0
        self.temp1Error = 0
        self.temp2Error = 0
        self.temp3Error = 0
        self.temp4Error = 0
        self.row1Error = 0
        self.row2Error = 0
        self.row3Error = 0
        self.message = 0


    def run(self):
        #call start() to execute non-blocking
        while(True):
           
            while(True):
                while(True):
                    if self.mygui2comQueue.empty():
                        TxReq=0
                    else:
                        TxReq=1

                    if TxReq==0: #Read Rx
                        inputValue = str(s1.readline())
                        if inputValue != None:
                            print(inputValue)
                            # s = str(s1.readline())
                            # print(s)
                            if "$" not in inputValue:
                                break
                            if "!!!" in inputValue:
                                break
                            #print("Passes Break")
                            data,space=inputValue.split('$')
                            data,junk1=space.split('*')
                            data,reading=data.split(':')
                            #print(data)
                            #print(reading)
                            if Temp1Inside in data:
                                print("Inside Temp 1  Value:")
                                print(reading)
                                self.tempIdata = reading
                                self.temp1Error = 0
                                self.temp2Error = 0
                            if Temp1Outside in data:
                                print("Outside Temp 1  Value:")
                                print(reading)
                                self.tempOdata = reading
                                self.temp3Error = 0
                                self.temp4Error = 0
                            if Moist1 in data:
                                print("Moisture Row 1  Value:")
                                print(reading)
                                self.row1data = reading
                                self.row1Error = 0
                            if Moist2 in data:
                                print("Moisture Row 2  Value:")
                                print(reading)
                                self.row2data = reading
                                self.row2Error = 0
                            if Moist3 in data:
                                print("Moisture Row 3  Value:")
                                print(reading)
                                self.row3data = reading
                                self.row3Error = 0
                            if ErrR1 in data:
                                print("Moisture Row 1  Error")
                                #print(reading)
                                self.row1Error = 1
                                self.row1data = -99
                            if ErrR2 in data:
                                print("Moisture Row 2  Error")
                                #print(reading)
                                self.row2Error = 1
                                self.row2data = -99
                            if ErrR3 in data:
                                print("Moisture Row 3  Error")
                                #print(reading)
                                self.row3Error = 1
                                self.row3data = -99
                            if ErrIn in data:
                                print("Inside Temp Error")
                                #print(reading)
                                self.temp1Error = 1
                                self.temp2Error = 1
                                self.temp3Error = 1
                                self.temp4Error = 1
                                self.tempIdata = -99
                                self.tempOdata = -99

                            if ErrOut in data:
                                print("Outside Temp 2 Error")
                                #print(reading)
                                self.temp1Error = 1
                                self.temp2Error = 1
                                self.temp3Error = 1
                                self.temp4Error = 1
                                self.tempIdata = -99
                                self.tempOdata = -99

       
                            #self.tempIdata = 2 #testing
                            #self.tempOdata = 3 #testing
                            #self.row1data = 4 #testing
                            #self.row2data = 5 #testing
                            #self.row3data = 6 #testing
                            self.mycom2guiQueue.put((self.tempIdata, self.tempOdata, self.row1data, self.row2data, self.row3data, self.temp1Error, self.temp2Error, self.temp3Error, self.temp4Error, self.row1Error, self.row2Error, self.row3Error))
                            #time.sleep(1)


                    if TxReq==1:
                        try:
                            self.message = self.mygui2comQueue.get(block=False, timeout=None)
                        except:
                            print("  ERROR!! queue was not empty, but coudn't get anything out of it")
                            #pass
                        while(self.message == "eStop"):        #eStop Send
                            print("eStop was received from GUI")
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %40, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
                     
                        while(self.message == "fertOn"):       #fert Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %30, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")

                        while(self.message == "waterOn"):     	# Water On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %20, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
				
                        while(self.message == "ventOn"): 		# Vent On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %10, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
				
                        while(self.message == "masterSolOn"):		# All Sol On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %21, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
				
                        while(self.message == "waterSolOn"):		# Main Water Sol On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %22, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
			
                        while(self.message == "heatSolOn"):		# Heater Water Sol On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %23, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
			
                        while(self.message == "fertSolOn"):		# Fert Water Sol On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %24, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
				
                        while(self.message == "row1SolOn"):		# Row 1 Water Sol On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %25, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "row2SolOn"):		# Row 2 Water Sol On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %26, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "row3SolOn"):	# Row 3 Water Sol On Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %27, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "masterSolOff"):		# Master Water Sol OFF Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %51, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "waterSolOff"):		# Water Sol OFF Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %52, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    			
                        while(self.message == "heatSolOff"):		# Heater Sol OFF Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %53, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "fertSolOff"):		# fert Sol OFF Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %54, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "row1SolOff"):	# Row 1 Sol OFF Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %55, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "row2SolOff"):		# Row 2 Sol OFF Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %56, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "row3SolOff"):		# Row 3 Sol OFF Send
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %57, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "autoMode"):		# enter Auto Mode
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %60, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")
    				
                        while(self.message == "manualMode"):		# enter Manual Mode
                            GPIO.output(23,1)
                            s1.write(bytes('%d' %61, 'UTF-8'))
                            #time.sleep(.25)
                            inputValue = str(s1.readline())
                            print(inputValue)
                            if "!!!" in inputValue:
                                GPIO.output(23,0)
                                self.message = ""
                                print("HI")

                time.sleep(0.1)

