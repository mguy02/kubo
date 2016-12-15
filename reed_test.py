#!/usr/bin/python

import RPi.GPIO as GPIO
import numpy as np
import time
import sys
GPIO.setmode(GPIO.BCM)

# Sensor pins
pin_s1 = 17
pin_s2 = 22

GPIO.setup(pin_s1,GPIO.IN)
GPIO.setup(pin_s2,GPIO.IN)
idx_1 = 0
arr1 = []
arr2 = []

print "Listening to Reed contacts..."

while True:
	val_1 = GPIO.input(pin_s1)
	val_2 = GPIO.input(pin_s2)
	
	arr1.append(val_1)

	arr2.append(val_2)
	
	time.sleep(0.001)
	idx_1 = idx_1 + 1
	if idx_1 > 10000:
		break

sys.stdout.write ("[")
for e in arr1:
	if e == 0:
		sys.stdout.write (".")
	else:
		sys.stdout.write (str(e))
	sys.stdout.write (",")
print "]"


sys.stdout.write ("[")
for e in arr2:
	if e == 0:
		sys.stdout.write (".")
	else:
		sys.stdout.write (str(e))
	sys.stdout.write (",")
print "]"
	
with open("rawdata.txt", "w") as f:
	f.write(str(arr1))
	f.write("\n")
	f.write(str(arr2))


