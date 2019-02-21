import subprocess
import os
import sys
import time
from video_stitch import video_stitch, first_stitch


x = int(sys.argv[1])
dir_name = sys.argv[2]
filename = sys.argv[3]
dir_name = sys.argv[4]
number_of_cameras = int(sys.argv[5])

filename = "/home/ryan/Documents/full_circle/" + dir_name + "/" + filename

# Try moving the .arw files to stitchwatch so they can
# be stitched
try:
    j = 0
    while j < number_of_cameras:
        photo_name = "%06d" % (x+1) + "-" + chr(j+65) + ".arw"
        photo_location = "/home/ryan/Documents/full_circle/" + dir_name + "/" + photo_name
        print(photo_name)
        process = subprocess.call(["cp", "-f", photo_location, "/home/ryan/Documents/full_circle/stitchwatch/"])
        j += 1
except NameError as e:
    # Print error to the screen and to the log file
    print("\nError in moving files to stitchwatch\n")
    print(e)
    log_file = open(filename, "a+")
    log_file.write("Error in moving files to /stitchwatch")
    log_file.close()

# Try editing and renaming the .pts file
try:
    if x > 0:

        # Look for the new stitched image before creating the video
        txt_file_check = subprocess.check_output(["ls", "/home/ryan/Documents/full_circle/stitchwatch/"])
        txt_file_check = txt_file_check.decode('utf-8')
        txt_file_check = txt_file_check.splitlines()

        txt_file = "%06d" % (x) + "-A.txt"

        while not txt_file in txt_file_check:
            txt_file_check = subprocess.check_output((["ls", "/home/ryan/Documents/full_circle/stitchwatch/"]))
            txt_file_check = txt_file_check.decode('utf-8')
            txt_file_check = txt_file_check.splitlines()

        old_number = "%06d" % (x)
        new_number = "%06d" % (x+1)
        old_path = "/home/ryan/Documents/full_circle/stitchwatch/" + old_number + "-A.txt"
        new_path = "/home/ryan/Documents/full_circle/stitchwatch/" + new_number + "-A.pts"
        command = "sed 's/%s/%s/g' %s > %s" % (old_number, new_number, old_path, new_path)
        process = subprocess.call([command], shell=True)
    else:
        subprocess.call(["cp", "-f", "/home/ryan/Documents/full_circle/template.txt", "/home/ryan/Documents/full_circle/stitchwatch/000001-A.pts"])
except NameError as e:
    # Print error to the screen and to the log file
    print("Error in renaming .pts file")
    print(e)
    log_file = open(filename, "a+")
    log_file.write("Error in renaming .pts file")
    log_file.close()
except AttributeError as e:
    print(e)


# Look for the new stitched image before creating the video
jpgs = subprocess.check_output(["ls", "/home/ryan/Documents/full_circle/stitchwatch/"])
jpgs = jpgs.decode('utf-8')
jpgs = jpgs.splitlines()

jpg_name = "%06d" % (x+1) + "-A.jpg"

while not jpg_name in jpgs:
    jpgs = subprocess.check_output(["ls", "/home/ryan/Documents/full_circle/stitchwatch/"])
    jpgs = jpgs.decode('utf-8')
    jpgs = jpgs.splitlines()

size = 0
while size < 200000:
    files = subprocess.check_output(["ls", "-al", "/home/ryan/Documents/full_circle/stitchwatch/"])
    files = files.decode('utf-8')
    files = files.splitlines()
    for file in files:
        if jpg_name.lower() in file.lower():
            file = file.split()
            size = int(file[4])

# Wait for the image to finish being stitched
time.sleep(25)

# Update the current video, if it exists
if x > 0:
    video_stitch(x, "/home/ryan/Documents/full_circle/" + str(dir_name) + "_preview/", filename)
elif x == 0:
    first_stitch("/home/ryan/Documents/full_circle/stitchwatch/", "/home/ryan/Documents/full_circle/" + str(dir_name) + "_preview/", filename)

# Log the success
log_file = open(filename, "a+")
message = "\nStitched " + jpg_name + "\n"
log_file.write(message)
log_file.close()
