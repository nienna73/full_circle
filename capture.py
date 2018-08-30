#!/usr/bin/env python

import subprocess
import time
import threading
import sys
import datetime
import os

camera_ports = []
images_to_capture = int(sys.argv[2])   # the total number of panoramic photos you want to take (indexed from 1)
x = int(sys.argv[1])
wait_interval = int(sys.argv[3])   # time to wait between taking each photo in seconds, this is not currently being used
filename = "placeholder"

number_of_ports = len(sys.argv)

ports_string = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_string_split = ports_string.split()

for port in ports_string_split:
    port = port.decode('utf-8')
    if port[0] == 'u':
        camera_ports.append(port)


filename = "%06d" % (x + 1) + "-" + str(chr(65 + int(sys.argv[2]))) + ".arw"
interval = str(int(wait_interval) / 2)
subprocess.call(["gphoto2", "--port=" + camera_ports[int(sys.argv[2])], "--capture-tethered", "1s", "--filename=" + filename])


# while x < images_to_capture:
#     filename = "%06d" % (x + 1) + "-" + str(chr(65 + int(sys.argv[1]))) + ".arw"
#     subprocess.call(["gphoto2", "--port=" + camera_ports[int(sys.argv[1])], "--capture-image-and-download", "--filename=" + filename])
#     x = x + 1
#     time.sleep(wait_interval)
