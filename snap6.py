import subprocess
import os
import datetime

now = datetime.datetime.now()
dir_name = now.strftime("%Y%m%d_%Hh%Mm%Ss_snap6")

# Try to open the directory where the photos are stored,
# if it doesn't exist, create it then navigate to it
try:
    os.chdir(str(dir_name))
except:
    make_dir = subprocess.Popen(["mkdir", str(dir_name)])
    make_dir.wait()
    os.chdir(str(dir_name))

# Locate all cameras and split results into readable strings
# Remove the Canon camera
ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_strings_split = ports_strings.splitlines()
camera_ports = []

for string in ports_strings_split:
    string_decode = string.decode('utf-8')
    if 'sony' not in string_decode.lower():
        ports_strings_split.remove(string)

for string in ports_strings_split:
    string = string.decode('utf-8').split()
    for item in string:
        if item[0].lower() == 'u':
            camera_ports.append(item)

# Set the ISO and shutter speed of each camera
number_of_cameras = len(camera_ports)

i = 0
process = ''
while i < number_of_cameras:
    process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/capture.py", '0', str(i)])
    i = i + 1
process.wait()
