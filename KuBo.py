#!/usr/bin/python

from __future__ import division
import threading
import pigpio
import time
import sys
import numpy as np

class KuBo():
	
	
	def __init__(self, servoPin = 19, start_pos = 900):
		self.servoPin = servoPin
		self.start_pos = start_pos	#The servo position at boot up
		self.pi = pigpio.pi()
		self.pi.set_servo_pulsewidth(self.servoPin, self.start_pos)
		# Parameters for the thread need to be lists to change their values 
		# during thread execution
		self.end_pos_list = [0]
		self.freq_list = [0]
		
	def start_jumping(self, end_pos, freq):
		
		# check if thread is allready running
		if hasattr(self, 't_jump'):
			if self.t_jump.isAlive():
				print "Kubo is allready jumping... Let him take a break :D"
				return
		
		self.end_pos_list[0] = end_pos
		self.freq_list[0] = freq
		
		# Set Servo to starting value
		self.pi.set_servo_pulsewidth(self.servoPin, self.start_pos)
		
		# Create lock for thread values
		self.jump_lock = threading.Lock()
		
		# Create event that is triggered when thread should be stopped
		self.jump_stop = threading.Event()
		
		# Define thread
		self.t_jump = threading.Thread(target=self._jump_thread, args=(self.end_pos_list, self.freq_list, self.jump_stop))
		
		self.t_jump.start()
		
		
	def _jump_thread(self, end_pos_list, freq_list, stop_event):
		print "Thread started"
		while(not stop_event.is_set()):
			with self.jump_lock:
				print "End position: ", end_pos_list[0]
				print "Frequency: ", freq_list[0]
				
				# Calculate the settle time the servo needs for moving
				# Convert pulsewidth to degrees
				degree = (end_pos_list[0]-self.start_pos) / 10
				# Servo speed is 0.15s/60deg
				# Safety factor of 1.1
				settle = 0.15/60*degree*1.1
				
				
				sleep_time = 1/freq_list[0]-2*settle
				self.pi.set_servo_pulsewidth(self.servoPin, end_pos_list[0])
				time.sleep(settle)
				self.pi.set_servo_pulsewidth(self.servoPin, self.start_pos)
				time.sleep(settle)
			if sleep_time > 0:
				time.sleep(sleep_time)
			elif sleep_time < 0:
				print "Frequency too high"
		print "Thread stopped"
	
	def stop_jumping(self):
		if not hasattr(self, 't_jump'):
			print "Kubo needs to start jumping first"
			return
		else:
			if not self.t_jump.isAlive():
				print "Kubo needs to start jumping first"
				return
	
		self.jump_stop.set()
		
	def change_jumping(self, end_pos, freq):
		if not hasattr(self, 't_jump'):
			print "Kubo needs to start jumping first"
			return
		else:
			if not self.t_jump.isAlive():
				print "Kubo needs to start jumping first"
				return
			
	
		with self.jump_lock:
			self.end_pos_list[0] = end_pos
			self.freq_list[0] = freq
			
	def is_jumping(self):
		if not hasattr(self, 't_jump'):
			return False
		else:
			return self.t_jump.isAlive()
			
			
			
			
			