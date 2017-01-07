#!/usr/bin/python

import numpy as np
import time
from behaviour_exercise import Behaviour_exercise
from pynput.keyboard import Key, Listener
from flags import Flags
from time import time

timeStart = 0
timeEnd = 0
distance=1
f = Flags()
behaviour = Behaviour_exercise(f)

def set_global():
    global timeStart
    global timeEnd
    timeStart = 0
    timeEnd = 0
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
set_global()

def calculate_speed(start,end,lenght):
    return float (end - start)/lenght

def on_press(key):
    if (key == Key.page_up):
        f.set_sensor_low(1)
        f.set_sensor_up(0)
        print 'page UP pressed'
        behaviour.update_behaviour_exercise(f.get_sensor_low(),f.get_sensor_up())
        f.update_sound()
    elif (key == Key.f2):
        f.set_sensor_low(0)
        f.set_sensor_up(1)
        timeEnd = time()
        print 'F2 pressed'
        speed = calculate_speed(timeEnd-5,timeEnd,distance)
        print 'The speed is %.2f' % speed
        behaviour.set_speed(speed)
        behaviour.update_behaviour_exercise(f.get_sensor_low(),f.get_sensor_up())
        f.update_sound()
    elif (key == Key.page_down):
        f.set_sensor_low(0)
        f.set_sensor_up(2)
        print 'page DOWN pressed'
        behaviour.update_behaviour_exercise(f.get_sensor_low(),f.get_sensor_up())
        f.update_sound()
    elif (key == Key.f4):
        f.set_sensor_low(2)
        f.set_sensor_up(0)
        timeEnd = time()
        print 'f4 pressed'
        speed = calculate_speed(timeEnd-5,timeEnd,distance)
        print 'The speed is %.2f' % speed
        behaviour.set_speed(speed)
        behaviour.update_behaviour_exercise(f.get_sensor_low(),f.get_sensor_up())
        f.update_sound()
    elif (key== Key.f5):
        behaviour.set_motivation(0)
    elif (key== Key.f6):
        behaviour.set_motivation(1)
    elif (key== Key.f7):
        behaviour.set_weight(5)
    elif (key== Key.f8):
        behaviour.set_weight(30)
    elif (key== Key.caps_lock):
        behaviour.set_relax(0)
        behaviour.update_behaviour_exercise(f.get_sensor_low(), f.get_sensor_up())
    elif (key== Key.backspace):
        behaviour.set_relax(1)
        behaviour.update_behaviour_exercise(f.get_sensor_low(), f.get_sensor_up())


# Collect events until released
with Listener(
        on_press=on_press) as listener:
    listener.join()


