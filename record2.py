import subprocess
import time
import sys


video_length = int(sys.argv[1])
# 29 minutes = 1740s
total_videos = int(sys.argv[2])
interval = int(sys.argv[3])


camera_ports = []
x = 0

ports_string = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_string_split = ports_string.split()
for item in ports_string_split:
    item = item.decode('utf-8')
    if item[0] == 'u':
        camera_ports.append(item)

while (x < total_videos):
    print('running record')
    for port in camera_ports:
        subprocess.call(["gphoto2", "--port=" + port, "--set-config", "movie=1"])

    time.sleep(video_length)

    for port in camera_ports:
        subprocess.call(["gphoto2", "--port=" + port, "--set-config", "movie=0"])

    x = x + 1
    time.sleep(interval)
