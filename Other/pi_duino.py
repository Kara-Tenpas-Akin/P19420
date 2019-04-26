#!/user/bin/env python
import serial
import time
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

s="1"
data="0"
space="0"
junk1="0"

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,0)
TxReq=1
while True:
 while True:
 	if TxReq==0: #Read Rx

  		inputValue = s1.readline()
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
  		if Temp1Outside in data:
   			print("Outside Temp 1  Value:")
   			print(reading)
  		if Moist1 in data:
   			print("Moisture Row 1  Value:")
   			print(reading)
  		if Moist2 in data:
   			print("Moisture Row 2  Value:")
   			print(reading)
  		if Moist3 in data:
   			print("Moisture Row 3  Value:")
   			print(reading)

 	if TxReq==1:
  		GPIO.output(23,1)
  		s1.write('%d'%20)
  		time.sleep(.25)
  		inputValue = s1.readline()
                print(inputValue)
                if "!!!" in inputValue:
  	        	#GPIO.output(23,0)
                        #TxReq = 0
                        print("HI")


