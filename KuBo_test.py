#!/usr/bin/python

import numpy as np
import time
from KuBo import KuBo

kubo = KuBo()
print "Kubo is jumping: ", kubo.is_jumping()
kubo.start_jumping(1500, 1.06)

time.sleep(10)
print "Kubo is jumping: ", kubo.is_jumping()
kubo.change_jumping(2100, 0.53)

time.sleep(10)
print "Kubo is jumping: ", kubo.is_jumping()	
kubo.stop_jumping()

time.sleep(1)
print "Kubo is jumping: ", kubo.is_jumping()