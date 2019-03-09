
import sys
import os
import subprocess
import time
import signal

from operator import itemgetter
#
# frequency = sys.argv[1]
# duration = sys.argv[2]
#
# print("\nFrequency: " + str(frequency))
# print("Duration: " + str(duration) + "\n")
# os.system("for(int i=0;i<3;i++)); do echo hi & done")


# path = "/home/ryan/"
# time.sleep(5)
# print("end")
# # os.killpg(p.pid, signal.SIGTERM)
# exit()

# x=1
# old_number = "%06d" % (x)
# new_number = "%06d" % (x+1)
# old_path = "/home/ryan/Documents/full_circle/stitchwatch/" + old_number + "-A.pts"
# new_path = "/home/ryan/Documents/full_circle/stitchwatch/" + new_number + "-A.pts"
# command = "sed 's/%s/%s/g' %s > %s" % (old_number, new_number, old_path, new_path)
# process = subprocess.call([command], shell=True)

# files = subprocess.check_output(["ls", "-al", "/home/ryan/Documents/full_circle/20190210_14h10m27s/"])
# files = files.decode('utf-8')
# files = files.splitlines()
# for file in files:
#     if ".jpg" in file.lower():
#         file = file.split()
#         print(file[4])

camera_ports = []       # stores relevant ports

# Locate all cameras and split results into readable strings
ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_strings_split = ports_strings.splitlines()

for string in ports_strings_split:
    string_decode = string.decode('utf-8')
    if 'sony' not in string_decode.lower():
        ports_strings_split.remove(string)

for string in ports_strings_split:
    string = string.decode('utf-8').split()
    for item in string:
        if item[0].lower() == 'u':
            camera_ports.append(item)

print(camera_ports)




# # new_files = os.listdir(path)
# new_files = subprocess.check_output((["ls", "-al", path]))
# new_files = new_files.decode('utf-8')
# new_files = new_files.splitlines()
#
#
# filenames = []
#
# for item in new_files:
#     item = item.split()
#     if len(item) > 2:
#         entry = [item[7], item[8]]
#         filenames.append(entry)
# filenames = sorted(filenames, key=itemgetter(0))
#
# for item in filenames:
#     print(item)
