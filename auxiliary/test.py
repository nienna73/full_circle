
import sys
import os
import subprocess
import time
import signal

from operator import itemgetter

processes = subprocess.check_output(["ps", "aux"])
break_char = "\n".encode('ascii')
processes = processes.split(break_char)
for process in processes:
    process = process.decode("utf-8")
    print(process)
    # process = str(process)
    if "ffplay" in process.lower():
        split_process = process.split()
        subprocess.call(["sudo", "kill", split_process[1]])
        print ("Killed process ", split_process[-1])

# full_dir_name = "/home/ryan/Documents/full_circle/timelapse/20190504_11h30m30s/"
#
# jpg_img_check = subprocess.check_output((["ls", full_dir_name]))
# jpg_img_check = jpg_img_check.decode('utf-8')
# print(jpg_img_check)
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

# camera_ports = []       # stores relevant ports
#
# # Locate all cameras and split results into readable strings
# ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
# ports_strings_split = ports_strings.splitlines()
#
# for string in ports_strings_split:
#     string_decode = string.decode('utf-8')
#     if 'sony' not in string_decode.lower():
#         ports_strings_split.remove(string)
#
# for string in ports_strings_split:
#     string = string.decode('utf-8').split()
#     for item in string:
#         if item[0].lower() == 'u':
#             camera_ports.append(item)
#
# print(camera_ports)

# def locateAndUpdateCameras(s_speed, i_value):
#     cameras = []    # to hold ports, to be returned
#     # Detect all the cameras
#     ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
#     ports_strings_split = ports_strings.split()
#
#     # Find all the ports of format "usb:xxx,xxx"
#     for item in ports_strings_split:
#         item = item.decode('utf-8')
#         if item[0] == 'u':
#             cameras.append(item)
#
#     if "." in s_speed:
#         if "3" in s_speed or "4" in s_speed:
#             s_speed = "1/3"
#         elif "5" in s_speed or "6" in s_speed:
#             s_speed = "1/2"
#         elif "8" in s_speed:
#             s_speed = "1"
#         print(s_speed)
#
#
#     # Update the shutter speed and iso on each camera
#     for port in cameras:
#         print(port)
#         subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + s_speed, "--set-config-value", "iso=" + i_value])
#
#     i = 0
#     x = 0
#     while i < len(cameras):
#         process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/capture.py", str(x), str(i)])
#         i = i + 1
#
# locateAndUpdateCameras("0.3", "100")




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
