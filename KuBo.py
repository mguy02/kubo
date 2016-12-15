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
		
		self.last_cb_lower = 0
		self.last_cb_higher = 0
		
		# Debounce parameters
		self.deb = 0.12
		self.num_it = 5
		self.it_delay = 0.005
		
		# Contact counter
		self.lower_count = 0
		self.higher_count = 0
		
		# Locks
		self.lock_cb_lower = threading.Lock()
		self.lock_cb_higher = threading.Lock()

		
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
		t = time.time()
		
		# debounce
		with self.lock_cb_lower:
			t_diff = t - self.last_cb_lower
		if  t_diff < self.deb:
			# caught debounce
			return
		else:
			# despike
			sum = 0
			it_count = 0
			while it_count < self.num_it:
				sum = sum + self.pi.read(self.lowerReedPin)
				it_count = it_count + 1
				time.sleep(self.it_delay)
			if sum/self.num_it > 0.5:
				# legitamite contact
				print "====Lower Reed contact activated===="
				print "System Time at interrupt: ", t
				print "Pin: ", gpio
				print "Level: ", level
				
				with self.lock_cb_lower:
					self.last_cb_lower = t
					self.lower_count = self.lower_count + 1
				print "Lower Reed contact count: ", self.lower_count
				print
			else:
				# interference
				print "Interference detected on lower Reed Contact on Pin: ", self.lowerReedPin 
		
	def _callback_higher(self, gpio, level, tick):
		t = time.time()
		
		# debounce
		with self.lock_cb_higher:
			t_diff = t - self.last_cb_higher
		if  t_diff < self.deb:
			# caught debounce
			return
		else:
			# despike
			sum = 0
			it_count = 0
			while it_count < self.num_it:
				sum = sum + self.pi.read(self.higherReedPin)
				it_count = it_count + 1
				time.sleep(self.it_delay)
			if sum/self.num_it > 0.5:
				# legitimate contact
				print "====Higher Reed contact activated===="
				print "System Time at interrupt: ", t
				print "Pin: ", gpio
				print "Level: ", level
				# time.sleep(1)
				# print "Tick difference: ", self.pi.get_current_tick() - tick
				# print "Time difference: ", time.time() - t
				
				
				with self.lock_cb_higher:
					self.last_cb_higher = t
					self.higher_count = self.higher_count + 1
				print "Higher Reed contact count: ", self.higher_count
				print
			else:
				# interference
				print "Interference detected on higher Reed Contact on Pin: ", self.higherReedPin 
		
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
			

		
			
			
			
			
			