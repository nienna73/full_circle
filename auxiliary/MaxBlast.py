#!/usr/bin/env python

# This program captures as many images as possible with as little
# delay as possible between the images. It takes the delay, in seconds,
# as a command line argument
# It is not configured to work with phidgets

__author__ = 'Jolene Poulin'
__version__ = '0.1.1'
__date__ = 'January 19th, 2019'

#standard imports
import sys
import time
import subprocess
import os
import datetime

i = int(sys.argv[1])

def main():

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

    while True:
        j = 0
        while j < len(camera_ports):
            process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/auxiliary/max_capture.py", str(j)])
            j = j + 1
        time.sleep(i)


main()
