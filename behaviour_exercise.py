import numpy as np
import time
from array import *
import pyglet
import time

''''
In this file we realaborate from the input received by the user hopw to behave kubo in the gym.
Basically we try to map any situation to a number and call the proper function.
We separated the speed in 3 ranges, so we have:
- low speed, when the speed is lowere than low_speed_limit
- medium spedd, when the speed is bounded between low_speed_limit and high_speed_limit
- high speed when it is higher than high_speed_limit

WUsing the same logic we create two group for the weight:
- low weight, when it is lower than low_weight_limit
- high weight, when it is higher than the low_weight_limit

another information received from the user is the type of motivation he prefers, we divide the users in two main groups,
- intrinsic
- extrinsic
we get this information by some survey based on the type of user we have kubo play different sounds...

all this variable for now are set as static but of course they dipende by the user's history during his exercises.

'''
low_speed_limit = 7
high_speed_limit = 20
low_weight_limit = 20
num_speed = 3 # number of total renges for the speed we have low - medium - high, in total are 3 for the moment
num_weight = 2
num_weightspeed_combination = num_speed*num_weight
counter = array('b', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # array which count how many repetition with the same speed and same weight are executed by the user


class Behaviour_exercise(object):
    def __init__(self, kubo):
        self.speed = 0
        self.weight = 0
        self.motivation = 0
        self.relax = 0
		self.kubo = kubo

    '''
    Set&Get functions of the varibles
    '''

    def set_speed(self, value):
        self.speed = value

    def set_weight(self, value):
        self.weight = value

    def set_motivation(self, value):
        self.motivation = value

    def set_relax(self,value):
        self.relax = value

    def get_speed(self):
        return self.speed

    def get_weight(self):
        return self.weight

    def get_motivation(self):
        return self.motivation

    def get_relax(self):
        return self.relax

    '''
    from_parametrs_to_number:
    map the different value of the states into a integer value bounded between 0 and (num_speed*num_weight*num_motivation - 1)
    '''
    def from_parameters_to_number(self):
        if (self.get_speed < low_speed_limit):
            parameter_speed = 0
        elif (self.get_speed > high_speed_limit):
            parameter_speed = 1
        else:
            parameter_speed = 2
        if (self.get_weight < low_weight_limit):
            parameter_weight = 0
        else:
            parameter_weight = 1

        if (self.get_relax()==1):
            count_len = int(len(counter))
            return  count_len + self.get_motivation()
        else:
            print ' here YEAH '
            number = (parameter_weight * num_speed + parameter_speed) + (self.get_motivation() * num_weightspeed_combination)
            return number
    '''
    update_behaviour_exercise
    call the proper function related with the actual situation of the exercise
    '''
    def update_behaviour_exercise(self, sensor_low, sensor_up):
        switcher = {
            0: intr_lowweight_lowspeed,
            1: intr_lowweight_medspeed,
            2: intr_lowweight_highspeed,
            3: intr_highweight_lowspeed,
            4: intr_highweight_medspeed,
            5: intr_highweight_highspeed,
            6: extr_lowweight_lowspeed,
            7: extr_lowweight_medspeed,
            8: extr_lowweight_highspeed,
            9: extr_highweight_lowspeed,
            10: extr_highweight_medspeed,
            11: extr_highweight_highspeed,
            12: intr_relax,
            13: extr_relax,
        }  # Get the function from switcher dictionary
        status = self.from_parameters_to_number()
        "{}".format(status)
        update_counter(status)
        func = switcher.get(status, lambda: "nothing")
        # Execute the function
        return func(status, sensor_low, sensor_up)

'''
List of function for the different situation
'''
def intr_lowweight_lowspeed(status):
    if (counter[status] == 3):
        kubo.say('i_l_l.mp3')
    return


def intr_lowweight_medspeed(status):
    if (counter[status] == 3):
        kubo.say('i_l_m.mp3')
    return


def intr_lowweight_highspeed(status):
    if (counter[status] == 3):
        kubo.say('i_l_h.mp3')
    return


def intr_highweight_lowspeed(status):
    if (counter[status] == 3):
        kubo.say('i_h_l.mp3')
    return


def intr_highweight_medspeed(status):
    if (counter[status] == 3):
        kubo.say('i_h_m.mp3')
    return


def intr_highweight_highspeed(status):
    if (counter[status] == 3):
        kubo.say('i_h_h.mp3')
    return


def extr_lowweight_lowspeed(status):
    if (counter[status] == 3):
        kubo.say('e_l_l.mp3')
    return


def extr_lowweight_medspeed(status):
    if (counter[status] == 3):
        kubo.say('e_l_m.mp3')
    return



def extr_lowweight_highspeed(status):
    if (counter[status] == 3):
        kubo.say('e_l_h.mp3')
    return



def extr_highweight_lowspeed(status):
    if (counter[status] == 3):
        kubo.say('e_h_l.mp3')
    return


def extr_highweight_medspeed(status):
    if (counter[status] == 3):
        kubo.say('e_h_m.mp3')
    return


def extr_highweight_highspeed(status):
    if (counter[status] == 3):
        kubo.say('e_h_h.mp3')
    return


def extr_relax(status):
    kubo.say('i_relax.mp3')
    return


def intr_relax(status):
    kubo.say('i_relax.mp3')
    return

'''
Everytime the trainer conclude a repetition of the exercise we update the counter array
after three times he repeat the same exercise 3 times Kubo react give some suggestions to the user
'''
def update_counter(status):
    i = 0
    while (i < len(counter)):
        if (i == status):
            counter[status] = counter[status] + 1
        else:
            counter[i] = 0
        i=i+1
    return



