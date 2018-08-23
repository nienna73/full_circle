import sys
import subprocess
import datetime
import os
import math

total_time = sys.argv[1]
interval = sys.argv[2]

camera_ports = []

ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_strings_split = ports_strings.split()


for item in ports_strings_split:
    item = item.decode('utf-8')
    if item[0] == 'u':
        camera_ports.append(item)

number_of_cameras = len(camera_ports)

number_of_photos = str(math.ceil(int(total_time)/int(interval)))

processes = []
i = 0
while i < number_of_cameras:
    print(i)
    process = subprocess.Popen(["python3", "../capture.py", str(i), number_of_photos, interval])
    processes.append(process)
    i = i + 1

# for process in processes:
#         process.wait()
# subprocess.call(["for(int i=0;i<" + str(number_of_cameras) + ";i++));", "do", "python3", "capture.py", "${i}", "done"], shell=True)
# os.system("(for (int i=0;i<" + str(number_of_cameras) + ";i++)); do python3 capture.py ${i} 2 3 done")
