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

    def run(self):
        #call start() to execute non-blocking
        while(True):
           
            while(True):
                while(True):

                    try:
                        #self.eStop, self.fertOn, self.waterOn, self.ventOn, self.masterSolOn, self.waterSolOn, self.heatSolOn, self.fertSolOn, self.row1SolOn, self.row2SolOn, self.row3SolOn, self.masterSolOff,self.waterSolOff, self.heatSolOff, self.fertSolOff, self.row1SolOff, self.row2SolOff, self.row3SolOff = self.mygui2comQueue.get(block=False, timeout=None)
                        message = self.mygui2comQueue.get(block=False, timeout=None)
                    except:
                        pass

                    if TxReq==0: #Read Rx
                        inputValue = str(s1.readline())
                        print(inputValue)
                        # s = str(s1.readline())
                        # print(s)
                        if "$" not in inputValue:
                            break
                        data,space=inputValue.split('$')
                        data,junk1=space.split('*')
                        data,reading=data.split(':')
                        # print(data)
                        # print(reading)
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
							self.row2Error = 0
                            self.row2data = reading
                        if Moist3 in data:
                            print("Moisture Row 3  Value:")
                            print(reading)
							self.row3Error = 0
                            self.row3data = reading
                        if ErrR1 in data:
                            print("Moisture Row 1  Error")
                            #print(reading)
                            self.row1Error = 1
                        if ErrR2 in data:
                            print("Moisture Row 2  Error")
                            #print(reading)
                            self.row2Error = 1
                        if ErrR3 in data:
                            print("Moisture Row 3  Error")
                            #print(reading)
                            self.row3Error = 1
                        if ErrIn in data:
                            print("Inside Temp Error")
                            #print(reading)
                            self.temp1Error = 1
                            self.temp2Error = 1
							self.temp3Error = 1
                            self.temp4Error = 1
                        if ErrOut in data:
                            print("Outside Temp 2 Error")
                            #print(reading)
                            self.temp3Error = 1
                            self.temp4Error = 1
							self.temp1Error = 1
                            self.temp2Error = 1

                            
                        #self.tempIdata = 2 #testing
                        #self.tempOdata = 3 #testing
                        #self.row1data = 4 #testing
                        #self.row2data = 5 #testing
                        #self.row3data = 6 #testing
                        self.mycom2guiQueue.put((self.tempIdata, self.tempOdata, self.row1data, self.row2data, self.row3data, self.temp1Error, self.temp2Error, self.temp3Error, self.temp4Error, self.row1Error, self.row2Error, self.row3Error))


                    #if TxReq==1:
                    while("eStop" in message):        #eStop Send
                        print("eStop was received from GUI")
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %40, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
                            
                    while("fertOn" in message):       #fert Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %30, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
                    
                    while("waterOn" in message):    	# Water On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %20, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("ventOn" in message):		# Vent On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %10, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("masterSolOn" in message):		# All Sol On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %21, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("waterSolOn" in  message):		# Main Water Sol On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %22, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("heatSolOn" in  message):		# Heater Water Sol On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %23, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("fertSolOn" in message):		# Fert Water Sol On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %24, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("row1SolOn" in message):		# Row 1 Water Sol On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %25, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("row2SolOn" in message):		# Row 2 Water Sol On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %26, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("row3SolOn" in message):		# Row 3 Water Sol On Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %27, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("masterSolOff" in message):		# Master Water Sol OFF Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %51, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("waterSolOff" in message):		# Water Sol OFF Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %52, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("heatSolOff" in message):		# Heater Sol OFF Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %53, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("fertSolOff" in message):		# fert Sol OFF Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %54, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("row1SolOff" in message):		# Row 1 Sol OFF Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %55, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("row2SolOff" in message):		# Row 2 Sol OFF Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %56, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("row3SolOff" in message):		# Row 3 Sol OFF Send
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %57, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
					while("autoMode" in message):		# enter Auto Mode
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %60, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")
							
                    while("manualMode" in message):		# enter Manual Mode
                        GPIO.output(23,1)
                        s1.write(bytes('%d' %61, 'UTF-8'))
                        time.sleep(.25)
                        inputValue = str(s1.readline())
                        print(inputValue)
                        if "!!!" in inputValue:
                            GPIO.output(23,0)
                            message = ""
                            print("HI")

                    time.sleep(1)
