#!/usr/bin/python

from __future__ import division
from omxplayer import OMXPlayer
import threading
import pigpio
import time
import sys
import numpy as np

class KuBo():
	
	
	def __init__(self, servoPin = 19, lowerReedPin = 17, higherReedPin = 22, start_pos = 900):
		self.servoPin = servoPin
		self.lowerReedPin = lowerReedPin
		self.higherReedPin = higherReedPin
			
		self.start_pos = start_pos	#The servo position at boot up
		
		self.pi = pigpio.pi()
		
		# Configure Pin Mode
		self.pi.set_mode(self.servoPin, pigpio.OUTPUT)
		self.pi.set_mode(self.lowerReedPin, pigpio.INPUT)
		self.pi.set_mode(self.higherReedPin, pigpio.INPUT)
		
		
		# Set position of servo to start position
		self.pi.set_servo_pulsewidth(self.servoPin, self.start_pos)
		
		# Parameters for the thread need to be lists to change their values 
		# during thread execution
		self.end_pos_list = [0]
		self.freq_list = [0]
		
		# Start Audio Player process
		self.audiopath = '/home/pi/Documents/Audio/'
		self.omx = OMXPlayer(self.audiopath + 'gangsta.mp3')
		self.omx.pause()
		
		# Initiallize edge listener
		self.cb_lower = self.pi.callback(self.lowerReedPin, pigpio.RISING_EDGE, self._callback_lower)
		self.cb_higher = self.pi.callback(self.higherReedPin, pigpio.RISING_EDGE, self._callback_higher)
				
		# zero count parameters
		#self.max_zero_count = 45
		self.max_zero_count = 2000
		self.min_zero_count = 5
		
		# one count parameters
		self.min_one_count = 3
		
		# polling period
		self.T_poll = 0.001
		
		# lower reed contact data
		self.lower_timestamps = []
		self.lower_speed = 0
		self.lower_weight = 0
		self.lower_history = []
		
		# higher reed contact data
		self.higher_timestamps = []
		self.higher_speed = 0
		self.higher_weight = 0
		self.higher_history = []
		
		
		# Locks
		self.lock_lower = threading.Lock()
		self.lock_higher = threading.Lock()

		
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
				
				
				self.pi.set_servo_pulsewidth(self.servoPin, end_pos_list[0])
				time.sleep(settle)
				self.pi.set_servo_pulsewidth(self.servoPin, self.start_pos)
				time.sleep(settle)
				if freq_list[0] != 0:
					sleep_time = 1/freq_list[0]-2*settle
				else:
					break
				
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
			
	def say(self, filename):
		return self.omx.load(self.audiopath + filename)
		
	def init_voice(self, audiopath = '/home/pi/Documents/Audio/'):
		self.audiopath = audiopath
		self.omx = OMXPlayer(self.audiopath + 'gangsta.mp3')
		return self.omx.pause()
		
	def stop_voice(self):
		return self.omx.quit()
		
	def _callback_lower(self, gpio, level, tick):
		print "==== Callback lower reed contact ===="
		t = time.time()
		# stop interrupts
		self.cb_lower.cancel()
		magnet_count = 0
		one_count = 0
		while True:
			inter_flag = False
			while self.pi.read(gpio):
					one_count = one_count + 1
					time.sleep(self.T_poll)
			if one_count < self.min_one_count:
				# Interference if no valey interference compensates for it
				print "Peak Interference suspicion"
				inter_flag = True
			
			zero_count = 0
			while self.pi.read(gpio) == 0:
				zero_count = zero_count + 1
				time.sleep(self.T_poll)
				if zero_count > self.max_zero_count:
					# No more consecutive magnets --> activate 
					# interrupts again for next passing of weights
					break
			if zero_count < self.min_zero_count:
				# Interference --> continue with first while loop
				print "Valey Interference detected on lower contact"
				if inter_flag:
					print "No peak interference"
			elif zero_count > self.max_zero_count:
				if not inter_flag:
					# Do calculations here
					magnet_count = magnet_count + 1
					print "Magnet Count: ", magnet_count
					with self.lock_lower: # save old timestamp
						self.lower_timestamps.append(t)
						print " Timestamps: ", self.lower_timestamps
						self.lower_history.append(self.lower_timestamps)
						self.lower_timestamps = []
					
					print "End of consecutive magnets"
				else:
					print "Peak interference detected on lower contact"
				self.cb_lower = self.pi.callback(gpio, pigpio.RISING_EDGE, self._callback_lower)
				break
			else:
				if not inter_flag:
					# start of next magnet
					with self.lock_lower: # save old timestamp
						self.lower_timestamps.append(t)
					t = time.time()
					one_count = 0
					magnet_count = magnet_count + 1
					print "Magnet Count: ", magnet_count
				else:
					# break out of interrupt thread and reactivate listening
					print "Peak interference detected on lower contact"
					self.cb_lower = self.pi.callback(gpio, pigpio.RISING_EDGE, self._callback_lower)
					break
					
			
				
				
			
			
	def _callback_higher(self, gpio, level, tick):
		print "==== Callback higher reed contact ===="
		t = time.time()
		# stop interrupts
		self.cb_higher.cancel()
		magnet_count = 0
		one_count = 0
		while True:
			inter_flag = False
			while self.pi.read(gpio):
					one_count = one_count + 1
					time.sleep(self.T_poll)
			if one_count < self.min_one_count:
				# Interference if no valey interference compensates for it
				print "Peak Interference suspicion"
				inter_flag = True
			
			zero_count = 0
			while self.pi.read(gpio) == 0:
				zero_count = zero_count + 1
				time.sleep(self.T_poll)
				if zero_count > self.max_zero_count:
					# No more consecutive magnets --> activate 
					# interrupts again for next passing of weights
					break
			if zero_count < self.min_zero_count:
				# Interference --> continue with first while loop
				print "Valey Interference detected on higher contact"
				if inter_flag:
					print "No peak interference"
			elif zero_count > self.max_zero_count:
				if not inter_flag:
					# No more consecutive magnets --> activate 
					# interrupts again for next passing of weights
					# Do calculations here
					magnet_count = magnet_count + 1
					print "Magnet Count: ", magnet_count
					with self.lock_higher: # save old timestamp
						self.higher_timestamps.append(t)
						print " Timestamps: ", self.higher_timestamps
						self.higher_history.append(self.higher_timestamps)
						self.higher_timestamps = []
					
					print "End of consecutive magnets"
				else:
					print "Peak interference detected on higher contact"
				self.cb_higher = self.pi.callback(gpio, pigpio.RISING_EDGE, self._callback_higher)
				break
			else:
				if not inter_flag:
					# start of next magnet
					with self.lock_higher: # save old timestamp
						self.higher_timestamps.append(t)
					t = time.time()
					one_count = 0
					magnet_count = magnet_count + 1
					print "Magnet Count: ", magnet_count
				else:
					# break out of interrupt thread and reactivate listening
					print "Peak interference detected on higher contact"
					self.cb_higher = self.pi.callback(gpio, pigpio.RISING_EDGE, self._callback_higher)
					break
			
	def stop_listening(self):
		if hasattr(self, 'cb_lower') and hasattr(self, 'cb_higher'):
			self.cb_lower.cancel()
			self.cb_higher.cancel()
		elif hasattr(self, 'cb_lower'):
			self.cb_lower.cancel()
		elif hasattr(self, 'cb_higher'):
			self.cb_higher.cancel()
		else:
			print "No listeners to close"
			
	def start_listening(self, lowerReedPin = 17, higherReedPin = 22):
		self.cb_lower = self.pi.callback(self.lowerReedPin, pigpio.RISING_EDGE, self._callback_lower)
		self.cb_higher = self.pi.callback(self.higherReedPin, pigpio.RISING_EDGE, self._callback_higher)
		
		
			

		
			
			
			
			
			