import subprocess
import os
import sys
import time
from video_stitch import video_stitch, first_stitch

x = int(sys.argv[1])        # number of the photo one before the one we just took
dir_name = sys.argv[2]      # location where all .arw files are stored

filename = sys.argv[3]


full_dir_name = "/home/ryan/Documents/full_circle/" + dir_name + "/"

# Run wine and wait for it to finish
did_stitch = False
while not did_stitch:
    try:
        stitch_file = "%06d" % (x+1) + "-A.pts"
        process = subprocess.Popen(["wine", "/home/ryan/Desktop/PTGui.exe", "-batch", "-x", stitch_file])
        did_complete = process.wait(45)
        did_stitch = True
    except:
        did_stitch = False

# Update the current video, if it exists
if x > 0:
    video_stitch(x, "/home/ryan/Documents/full_circle/" + str(dir_name) + "/", "/home/ryan/Documents/full_circle/" + str(dir_name) + "_preview/", filename)
elif x == 0:
    first_stitch("/home/ryan/Documents/full_circle/" + str(dir_name) + "/", "/home/ryan/Documents/full_circle/" + str(dir_name) + "_preview/", filename)

# Log the success
jpg_name = "%06d" % (x+1) + "-A.jpg"
log_file = open(filename, "a+")
message = "Stitched " + jpg_name + "\n\n"
log_file.write(message)
log_file.close()