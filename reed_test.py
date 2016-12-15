#!/usr/bin/python

import RPi.GPIO as GPIO
import numpy as np
import time
import sys
import csv


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

sample_period = 0.001
close = False	#if magnets are close or not

while True:
	val_1 = GPIO.input(pin_s1)
	val_2 = GPIO.input(pin_s2)
	
	arr1.append(val_1)

	arr2.append(val_2)
	
	time.sleep(sample_period)
	idx_1 = idx_1 + 1
	if idx_1 > 10000:
		break

#sys.stdout.write ("[")
#for e in arr1:
#	if e == 0:
#		sys.stdout.write (".")
#	else:
#		sys.stdout.write (str(e))
#	sys.stdout.write (",")
#print "]"


sys.stdout.write ("[")
for e in arr2:
	if e == 0:
		sys.stdout.write (".")
	else:
		sys.stdout.write (str(e))
	sys.stdout.write (",")
print "]"



#asking for number of up and down in a safe way (wrong value will ask again)
nb_ud = -1
while nb_ud < 0:
	nb_ud = input("Number of ud:")
	try:
		nb_ud = int(nb_ud)
	except ValueError:
		nb_ud = -1
		continue

#now define the filename
fname = "ud"*nb_ud
fname += "_"+str(sample_period)

if close:
	fname += "_close"

fname += ".csv"

#Output as csv file
with open(fname, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for val in arr2:
		writer.writerow([val])

print "Saved to", fname
