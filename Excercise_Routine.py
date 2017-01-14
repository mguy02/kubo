#!/usr/bin/python

import numpy as np
import time
from behaviour_exercise import Behaviour_exercise
from KuBo import KuBo

kubo = KuBo()

be = Behaviour_exercise(kubo)
# Instantiate KuBo --> activates listener on sensors

up_flag = 0
low_flag = 0
zero_time = float('inf')
restart_flag = 0
number_repetition = 0
speed_const = 0.15
ku_flag = 0
bo_flag = 1

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
				number_repetition = 0
				be.set_relax(0)
				be.set_weight(lower_data[2])
				restart_flag = 0
				#if be.get_message_flag() == 0:
				if bo_flag and number_repetition>6:
					kubo.say('ku.mp3')
					ku_flag = 1
					bo_flag=0
			elif low_flag == 2:
				low_flag = 1
				restart_flag = 0
				#if be.get_message_flag() == 0:
				if bo_flag and number_repetition>6:
					kubo.say('ku.mp3')
					ku_flag = 1
					bo_flag = 0
			elif low_flag == 1:
				low_flag = 2
				restart_flag = 1
				zero_time = time.time()
				#be.update_behaviour_exercise()
			
		if higher_data[0]:
			print "==== Weight block detected at higher sensor ===="
			print "Time: ", higher_data[1]
			print "Weight: ", higher_data[2]
			print "Speed: ", higher_data[3]
			print
			if up_flag == 0:
				up_flag = 1
				#be.set_speed(higher_data[3])
				be.set_speed(speed_const)
				
			elif up_flag == 2:
				up_flag = 1
				#be.set_speed(higher_data[3])
				if higher_data[3] > 0.05:
					be.set_speed(speed_const)
				#if number_repetition < 6 and higher_data[3] > 0.05:
				be.update_behaviour_exercise()
			elif up_flag == 1:
				number_repetition = number_repetition + 1
				up_flag = 2
				#if be.get_message_flag() == 0:
				if ku_flag and number_repetition>5:
					kubo.say('bo.mp3')
					bo_flag=1
					ku_flag = 0
				speed = be.get_speed()
				print
				print "==Speed: ", speed
				print "==repetition: ", number_repetition
				print
				if speed < 0.2 and speed > 0:
					kubo.start_jumping(2100,0)
				elif 0.2 <= speed and speed < 0.25:
					kubo.start_jumping(1500,0)
				else:
					kubo.start_jumping(1100,0)
				
		
		if time.time() - zero_time > 15 and restart_flag == 1:
			low_flag = 0
			up_flag = 0
			# save num repetition
			be.set_relax(1)
			kubo.say('i_relax.mp3')
			#be.update_behaviour_exercise()
			restart_flag = 0
			
			
		
		time.sleep(0.01)
	#except KeyboardInterrupt:
	except (KeyboardInterrupt, Exception) as e:
		kubo.stop_voice()
		kubo.stop_listening()
		raise

