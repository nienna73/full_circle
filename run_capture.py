import sys
import subprocess


camera_ports = []

ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_strings_split = ports_strings.split()

for item in ports_strings_split:
    if item[0] == 'u':
        camera_ports.append(item)

number_of_cameras = len(camera_ports)

subprocess.call(["for(int i=0;i<" + str(number_of_cameras) + ";i++));", "do", "python", "capture.py", "${i}", "done"], shell=True)
