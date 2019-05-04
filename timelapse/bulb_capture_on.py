#!/usr/bin/env python

# This program triggers a to capture a still image in either tethered mode
# using the relay to capture tighter images, or usb-connect mode
# Tethered mode makes sure the images are captured at the exact
# same moment, usb mode has a bit of a delay between each camera of a few
# milliseconds
# This program is passed 2 values:
# 1. x, which is the number-th photo taken, used for the filename (int)
# 2. The index of the camera port to be accessed

# This version of this program uses the shutterspeed=bulb setting in gphoto2

__author__ = 'Jolene Poulin'
__version__ = '0.0.1'
__date__ = 'January 26th, 2018'

# General imports
import subprocess
import time
import threading
import sys
import datetime
import os


camera_ports = []           # relevant camera ports

# Detect all connected cameras
ports_string = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_string_split = ports_string.split()

# Decode strings and find entries of format "usb:xxx,xxx",
# these are the relevant camera ports
for port in ports_string_split:
    port = port.decode('utf-8')
    if port[0] == 'u':
        camera_ports.append(port)

# Sort the ports so the cameras are triggered in the proper order
camera_ports.sort(reverse = True)

# Sets the camera to usb-capture mode
# This tells the camera to immediately capture an image, download it with
# filename 'filename', then delete it from the camera


subprocess.call(["gphoto2", "--port=" + camera_ports[int(sys.argv[1])], "--set-config", "bulb=1"])