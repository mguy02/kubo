#!/usr/bin/python

import numpy as np
import time
from KuBo import KuBo

# Instantiate KuBo --> activates listener on sensors
kubo = KuBo()

print "Listening for interrupts..."

######################### Jumping and Sound Tests ##############################
# Do the jumping routine from the video

"""
print "Kubo says KuBo and jumps"
kubo.say('kuuu.mp3')
time.sleep(1)

kubo.say('bo.mp3')
# Frequency = 0 means kubo jumps only once and exits the thread automatically
# No stop_jumping() needed
kubo.start_jumping(1500, 0)
time.sleep(2)


print "Kubo is more dramatic"
kubo.say('kuuu.mp3')
time.sleep(3)

kubo.say('bo.mp3')
kubo.start_jumping(2000, 0)
time.sleep(2)

# Kill potential open omx-processes
kubo.stop_voice()
"""

######################### Interrupt Tests #################################


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
			
		if higher_data[0]:
			print "==== Weight block detected at higher sensor ===="
			print "Time: ", higher_data[1]
			print "Weight: ", higher_data[2]
			print "Speed: ", higher_data[3]
			print
			
		time.sleep(0.5)
	except KeyboardInterrupt:
		kubo.stop_voice()
		kubo.stop_listening()
		raise

