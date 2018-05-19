import subprocess
import time
import threading

camera_ports = []
images_to_capture = 2   # the total number of photos you want to take (indexed from 1)
x = 0
wait_interval = 5   # time to wait between taking each photo in seconds

ports_string = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_string_split = ports_string.split()

for port in ports_string_split:
    if port[0] == 'u':
        camera_ports.append(port)

while x < images_to_capture:
    for port in camera_ports:
        subprocess.call(["gphoto2", "--port=" + port, "--capture-image-and-download", "--filename=" + port + str(x)])
        time.sleep(wait_interval)
        x = x + 1
