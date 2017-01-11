#!/usr/bin/python

import numpy as np
import time
from behaviour_exercise import Behaviour_exercise
from KuBo import KuBo

kubo = KuBo()

be= Behaviour_exercise(kubo)
# Instantiate KuBo --> activates listener on sensors

up__flag = 0
low_flag = 0
zero_time = 0
restart_flag = 0

while True:
	try:
		lower_data = kubo.get_lower_data()
		higher_data = kubo.get_higher_data()
		if lower_data[0]:
			print "==== Weight block detected at lower sensor ===="
			print "Time: ", lower_data[1]
			print "Weight: ", lower_data[2]
			print "Speed: ", lower_data[3]
			print
			if low_flag == 0:
				low_flag = 1
				kubo.say('ku.mp3')
			elif low_flag == 2:
				low_flag = 1
				kubo.say('ku.mp3')
			elif low_flag == 1:
				low_flag = 2
				zero_time = time.time()
			
		if higher_data[0]:
			print "==== Weight block detected at higher sensor ===="
			print "Time: ", higher_data[1]
			print "Weight: ", higher_data[2]
			print "Speed: ", higher_data[3]
			print
			if up_flag == 0:
				up_flag = 1
			elif up_flag == 2:
				up_flag = 1
			elif up_flag == 1:
				up_flag = 2
				kubo.say('bo.mp3')
				
		
		if time.time() - zero_time > 10:
			low_flag = 0
			up__flag = 0
			
			
		
		time.sleep(0.5)
	except KeyboardInterrupt:
		kubo.stop_voice()
		kubo.stop_listening()
		raise

