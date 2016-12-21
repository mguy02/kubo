#!/usr/bin/python

from __future__ import division
from omxplayer import OMXPlayer
import threading
import pigpio
import time
import sys
import numpy as np

class KuBo():
	
	
	def __init__(self, servoPin = 19, lowerReedPin = 17, higherReedPin = 22, start_pos = 900, plate_dist = 0.02, plate_weight = 5):
		self.servoPin = servoPin
		self.lowerReedPin = lowerReedPin
		self.higherReedPin = higherReedPin
			
		self.start_pos = start_pos	#The servo position at boot up
		
		self.plate_dist = plate_dist
		self.plate_weight = plate_weight
		
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
<<<<<<< HEAD
		self.max_zero_count = 45
		# self.max_zero_count = 1000
=======
		#self.max_zero_count = 45
		self.max_zero_count = 2000
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b
		self.min_zero_count = 5
		
		# one count parameters
		self.min_one_count = 3
<<<<<<< HEAD
		
		# polling period
		self.T_poll = 0.001
		
		# lower reed contact data
		self.lower_speed = 0
		self.lower_weight = 0
		self.lower_flag = 0
		self.lower_timestamp = 0
		
		
		# higher reed contact data
		self.higher_speed = 0
		self.higher_weight = 0
		self.higher_flag = 0
		self.higher_timestamp = 0
=======
		
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
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b
		
		
		# Locks
		self.lock_lower = threading.Lock()
		self.lock_higher = threading.Lock()
<<<<<<< HEAD
		
		self.data = []
=======
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b

		
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
<<<<<<< HEAD
		
		t = time.time()
		
		# stop interrupts
		self.cb_lower.cancel()
		
		self.data.append('...')
		
		print "==== Callback lower reed contact ===="
		
		timestamps = []
=======
		print "==== Callback lower reed contact ===="
		t = time.time()
		# stop interrupts
		self.cb_lower.cancel()
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b
		magnet_count = 0
		one_count = 0
		while True:
			inter_flag = False
<<<<<<< HEAD
			input = 1
			while input:
				input = self.pi.read(gpio)
				
				# debug
				# self.data.append(input)
				
				one_count = one_count + 1
				time.sleep(self.T_poll)
			if one_count < self.min_one_count:
				# Interference if no valey interference compensates for it
				# print "Peak Interference suspicion"
				inter_flag = True
			
			
			zero_count = 0
			input = 0
			while input == 0:
				input = self.pi.read(gpio)
				
				# debug
				# self.data.append(input)
				
=======
			while self.pi.read(gpio):
					one_count = one_count + 1
					time.sleep(self.T_poll)
			if one_count < self.min_one_count:
				# Interference if no valey interference compensates for it
				print "Peak Interference suspicion"
				inter_flag = True
			
			zero_count = 0
			while self.pi.read(gpio) == 0:
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b
				zero_count = zero_count + 1
				time.sleep(self.T_poll)
				if zero_count > self.max_zero_count:
					# No more consecutive magnets --> activate 
					# interrupts again for next passing of weights
					break
<<<<<<< HEAD
				elif inter_flag and zero_count >= self.min_zero_count:
					# No valey interference to compensate for peak interference
					# check if interference is isolated
					# print "Peak interference detected on lower contact"
					if magnet_count == 0:
						# isolated interference
						self.cb_lower = self.pi.callback(gpio, pigpio.RISING_EDGE, self._callback_lower)
						print "Interference detected"
						return
					else:
						# interference between magnets --> treet ones as zeros
						zero_count = zero_count + one_count
			if zero_count < self.min_zero_count:
				pass
				# Interference --> continue with first while loop
				# print "Valey Interference detected on lower contact"
				# if inter_flag:
					# print "No peak interference"
			elif zero_count > self.max_zero_count:
				# No more consecutive magnets --> calculate values of one repetition
				magnet_count = magnet_count + 1
				print "Magnet Count: ", magnet_count
				timestamps.append(t) # save old timestamp
				print " Timestamps: ", timestamps
				
				v = 0
				if magnet_count > 1:
					for i in range(magnet_count-1):
						v = v + self.plate_dist / (timestamps[i+1] - timestamps[i])
				else:
					print "Only one magnet detected --> cannot determine speed"
				
				with self.lock_lower: # save values of one repetition
					self.lower_weight = self.plate_weight*magnet_count
					self.lower_speed = v / magnet_count
					if self.lower_flag:
						print "flag wasn't read or properly set back to 0"
					self.lower_flag = 1
					self.lower_timestamp = timestamps[magnet_count-1]
					
					
				print "End of consecutive magnets"
				# Reactivate interrupt listener
				self.cb_lower = self.pi.callback(gpio, pigpio.RISING_EDGE, self._callback_lower)
				break
			else:
				# start of next magnet
				timestamps.append(t) # save old timestamp
				t = time.time()
				one_count = 0
				magnet_count = magnet_count + 1
				print "Magnet Count: ", magnet_count
					
=======
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
					
			
				
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b
				
			
			
	def _callback_higher(self, gpio, level, tick):
<<<<<<< HEAD
		t = time.time()
		
		# stop interrupts
		self.cb_higher.cancel()
		
		self.data.append('...')
		
		print "==== Callback higher reed contact ===="
		
		timestamps = []
=======
		print "==== Callback higher reed contact ===="
		t = time.time()
		# stop interrupts
		self.cb_higher.cancel()
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b
		magnet_count = 0
		one_count = 0
		while True:
			inter_flag = False
<<<<<<< HEAD
			input = 1
			while input:
				input = self.pi.read(gpio)
				
				# debug
				# self.data.append(input)
				
				one_count = one_count + 1
				time.sleep(self.T_poll)
			if one_count < self.min_one_count:
				# Interference if no valey interference compensates for it
				# print "Peak Interference suspicion"
				inter_flag = True
			
			
			zero_count = 0
			input = 0
			while input == 0:
				input = self.pi.read(gpio)
				
				# debug
				# self.data.append(input)
				
=======
			while self.pi.read(gpio):
					one_count = one_count + 1
					time.sleep(self.T_poll)
			if one_count < self.min_one_count:
				# Interference if no valey interference compensates for it
				print "Peak Interference suspicion"
				inter_flag = True
			
			zero_count = 0
			while self.pi.read(gpio) == 0:
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b
				zero_count = zero_count + 1
				time.sleep(self.T_poll)
				if zero_count > self.max_zero_count:
					# No more consecutive magnets --> activate 
					# interrupts again for next passing of weights
					break
<<<<<<< HEAD
				elif inter_flag and zero_count >= self.min_zero_count:
					# No valey interference to compensate for peak interference
					# check if interference is isolated
					# print "Peak interference detected on higher contact"
					if magnet_count == 0:
						# isolated interference
						self.cb_higher = self.pi.callback(gpio, pigpio.RISING_EDGE, self._callback_higher)
						print "Interference detected"
						return
					else:
						# interference between magnets --> treet ones as zeros
						zero_count = zero_count + one_count
			if zero_count < self.min_zero_count:
				pass
				# Interference --> continue with first while loop
				# print "Valey Interference detected on higher contact"
				# if inter_flag:
					# print "No peak interference"
			elif zero_count > self.max_zero_count:
				# No more consecutive magnets --> calculate values of one repetition
				magnet_count = magnet_count + 1
				print "Magnet Count: ", magnet_count
				timestamps.append(t) # save old timestamp
				print " Timestamps: ", timestamps
				
				v = 0
				if magnet_count > 1:
					for i in range(magnet_count-1):
						v = v + self.plate_dist / (timestamps[i+1] - timestamps[i])
				else:
					print "Only one magnet detected --> cannot determine speed"
				
				with self.lock_higher: # save values of one repetition
					self.higher_weight = self.plate_weight*magnet_count
					self.higher_speed = v / magnet_count
					if self.higher_flag:
						print "flag wasn't read or properly set back to 0"
					self.higher_flag = 1
					self.higher_timestamp = timestamps[magnet_count-1]
					
					
				print "End of consecutive magnets"
				# Reactivate interrupt listener
				self.cb_higher = self.pi.callback(gpio, pigpio.RISING_EDGE, self._callback_higher)
				break
			else:
				# start of next magnet
				timestamps.append(t) # save old timestamp
				t = time.time()
				one_count = 0
				magnet_count = magnet_count + 1
				print "Magnet Count: ", magnet_count
=======
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
>>>>>>> 663b9502f56d58be3c9e90dfed9eeefdaee9291b
			
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
		
		
			

		
			
			
			
			
			