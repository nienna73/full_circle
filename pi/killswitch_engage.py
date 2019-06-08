#! /usr/env/python

'''
# Killswitch Engage is meant to run on a Raspberry Pi in the field with a timelapse camera
# It uses a relay, which is wired to be always on.
# When this program is used, it opens the relay, waits 10 seconds, then closes the relay again
# effectively hard resetting the program.

# This file was created by Jolene Poulin on February 22, 2019
# for use by Full Circle Visuals Inc.
'''


"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Jolene Poulin'
__version__ = '0.1.2'
__date__ = 'June 8, 2019'

#Basic imports
from ctypes import *
import sys
import os
import random
import signal
import subprocess
import datetime
import math
from time import sleep

#Phidget specific imports
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *


from open_relay import open_relay

def engage():
    relay_left = open_relay(0)
    relay_right = open_relay(1)
    
    sleep(5)
    
    relay_left.setDutyCycle(1.0)
    print("relay on")
    sleep(10)
    relay_left.setDutyCycle(0.0)
    print("relay off")
    
    relay_right.setDutyCycle(1.0)
    print("relay on")
    sleep(10)
    relay_right.setDutyCycle(0.0)
    print("relay off")
    
    relay_left.close()
    relay_right.close()
    
def engage0():
    relay_left = open_relay(0)
    
    sleep(5)
    
    relay_left.setDutyCycle(1.0)
    print("relay on")
    sleep(10)
    relay_left.setDutyCycle(0.0)
    print("relay off")
    
    relay_left.close()
    
def engage1():
    relay_right = open_relay(1)
    
    sleep(5)
    
    relay_right.setDutyCycle(1.0)
    print("relay on")
    sleep(10)
    relay_right.setDutyCycle(0.0)
    print("relay off")

    relay_right.close()
    
    

