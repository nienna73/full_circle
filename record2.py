import subprocess
import time

video_length = 3
# 29 minutes = 1740
camera_ports = []
x = 0

ports_string = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_string_split = ports_string.split()
for item in ports_string_split: 
    if item[0] == 'u':
        camera_ports.append(item)

while (x < 3):
    for port in camera_ports:
        subprocess.call(["gphoto2", "--port=" + port, "--set-config", "movie=1"])
    
    time.sleep(video_length)
    
    for port in camera_ports:
        subprocess.call(["gphoto2", "--port=" + port, "--set-config", "movie=0"])

    x = x + 1

