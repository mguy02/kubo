#!/usr/bin/python

import numpy as np
import time
from KuBo import KuBo

kubo = KuBo()

######################### Jumping and Sound Tests ##############################
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
print "Listening for interrupts..."

while True:
	try:		
		time.sleep(2)
	except KeyboardInterrupt:
		kubo.stop_voice()
		kubo.stop_listening()
		raise


