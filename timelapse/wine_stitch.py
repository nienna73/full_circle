import subprocess
import os
import sys
import time
from video_stitch import video_stitch, first_stitch
from copy_to_drive import copy_to_drive
from wine_ptgui import wine_ptgui

x = int(sys.argv[1])        # number of the photo one before the one we just took
dir_name = sys.argv[2]      # location where all .arw files are stored

filename = sys.argv[3]
move_to_drive = sys.argv[4]
camera_ports = int(sys.argv[5])


full_dir_name = "/home/ryan/Documents/full_circle/timelapse/" + dir_name + "/"

# Try editing and renaming the .pts file
try:
    if x > 0:

        # Look for the new stitched image before creating the video
        txt_file_check = subprocess.check_output(["ls", full_dir_name])
        txt_file_check = txt_file_check.decode('utf-8')
        txt_file_check = txt_file_check.splitlines()

        old_number = "%06d" % (x)
        new_number = "%06d" % (x+1)
        old_path = full_dir_name + old_number + "-A.pts"
        new_path = full_dir_name + new_number + "-A.pts"
        command = "sed 's/%s/%s/g' %s > %s" % (old_number, new_number, old_path, new_path)
        process = subprocess.call([command], shell=True)
    else:
        new_location = full_dir_name + "000001-A.pts"
        subprocess.call(["cp", "-f", "/home/ryan/Documents/full_circle/template.pts", new_location])
except NameError as e:
    # Print error to the screen and to the log file
    print("Error in renaming .pts file")
    print(e)
    log_file = open(filename, "a+")
    log_file.write("Error in renaming .pts file")
    log_file.close()
except AttributeError as e:
    print(e)

# Stitch the current panorama
# wait for a successful stitch before moving on
did_stitch = wine_ptgui(x, dir_name, filename)
while did_stitch < 0:
    did_stitch = wine_ptgui(x, dir_name, filename)

vid_stitch = -1
while vid_stitch < 0:
    # Update the current video, if it exists
    if x > 0:
        vid_stitch = video_stitch(x, "/home/ryan/Documents/full_circle/timelapse/" + str(dir_name) + "/", "/home/ryan/Documents/full_circle/timelapse/" + str(dir_name) + "_preview/", filename)
    elif x == 0:
        vid_stitch = first_stitch("/home/ryan/Documents/full_circle/timelapse/" + str(dir_name) + "/", "/home/ryan/Documents/full_circle/timelapse/" + str(dir_name) + "_preview/", filename)

# Log the action
jpg_name = "%06d" % (x+1) + "-A.jpg"
log_file = open(filename, "a+")
message = "Stitched " + jpg_name + "\n\n"
log_file.write(message)
log_file.close()

# Move the files to the external drive, if applicable
if move_to_drive.lower() == 'y':
    if x > 0:
        copy_to_drive(dir_name, x, camera_ports)
