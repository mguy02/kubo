'''
SENSORS:
LOW - it is positionated close to the low weights
UP - it is positionated on top

Values:
LOW = 0 -> no magnets
LOW = 1 -> the weights passed the sensors and start to go up (SOUND: KUUUUUU)
LOW = 2 -> the weights passed the sensors and are going down (NOTHING)

TOP = 0 -> no magnets
TOP = 1 -> they weights passed the sensors and are going up (NOTHING)
TOP = 2 -> the weights passed the sensors and start to go down (SOUND: BO)
'''
import numpy as np
import time
#from KuBo import KuBo
from array import *

from behaviour_exercise  import playSound
#kubo = KuBo()

class Flags(object):
    def __init__(self):
        self.sensor_low = 0
        self.sensor_up = 0
        self.observers = []

    def get_sensor_low(self):
        return self.sensor_low

    def get_sensor_up(self):
        return self.sensor_up

    def set_sensor_low(self, value):
        self.sensor_low = value

    def set_sensor_up(self, value):
        self.sensor_up = value

    def update_sound(self):
            if (self.get_sensor_low() == 1):
                playSound('ku.mp3')  #kubo.say(Ku.mp3)
                self.set_sensor_low(0)
            elif (self.get_sensor_up() == 2):
                playSound('bo.mp3')  #kubo.say(Bo.mp3)
                self.set_sensor_up(0)





