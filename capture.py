import subprocess
import time
import threading
import sys
import datetime

camera_ports = []
images_to_capture = 2   # the total number of panoramic photos you want to take (indexed from 1)
x = 1
wait_interval = 5   # time to wait between taking each photo in seconds, this is not currently being used
filename = "placeholder"

number_of_ports = len(sys.argv)

ports_string = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_string_split = ports_string.split()

for port in ports_string_split:
    if port[0] == 'u':
        camera_ports.append(port)

now = datetime.datetime.now()
# filename = str(now.year) +"-"+  str(now.month) +"-"+  str(now.day) +"_"+  str(now.hour) + str(now.minute) + str(now.second) + "_" + sys.argv[1]
filename = now.strftime("%Y-%m-%d_%H-%M-%S") + "_" + str(sys.argv[1])
subprocess.call(["gphoto2", "--port=" + camera_ports[int(sys.argv[1])], "--capture-tethered", "--filename=" + filename])
