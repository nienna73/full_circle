#!/usr/bin/env python

# This function was designed for MaxBlast
# It triggers the capture on the cameras without downloading the images
# to the computer; images are stored in the camera's memory
# It takes the port location in the camera_ports list as
# a command line argument. This file only accesses one camera at a time 

__author__ = 'Jolene Poulin'
__version__ = '0.1.1'
__date__ = 'January 19th, 2019'

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


# Sets the camera to tethered mode and tells it to wait 1s for instructions
# before gphoto2 releases the camera. It's very important
# that the camera is released, otherwise it won't be accessible
# until it is restarted (very not ideal for remote triggering)
# subprocess.call(["gphoto2", "--port=" + camera_ports[int(sys.argv[2])], "--capture-tethered", "1s", "--filename=" + filename])

# Sets the camera to usb-capture mode
# This tells the camera to immediately capture an image
subprocess.call(["gphoto2", "--port=" + camera_ports[int(sys.argv[1])], "--trigger-capture"])
