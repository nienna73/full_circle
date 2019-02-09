import subprocess
import os
import sys
import time
from video_stitch import video_stitch, first_stitch


x = int(sys.argv[1])
dir_name = sys.argv[2]
log_file = sys.argv[3]


# Look for the new stitched image before creating the video
jpgs = subprocess.check_output((["ls", "/home/ryan/Documents/full_circle/stitchwatch/"]))
jpgs = jpgs.decode('utf-8')
jpgs = jpgs.splitlines()

jpg_name = "%06d" % (x+1) + "-A.jpg"

while not jpg_name in jpgs:
    jpgs = subprocess.check_output((["ls", "/home/ryan/Documents/full_circle/stitchwatch/"]))
    jpgs = jpgs.decode('utf-8')
    jpgs = jpgs.splitlines()

time.sleep(60)

# Update the current video, if it exists
if x > 0:
    video_stitch(x, "/home/ryan/Documents/full_circle/" + str(dir_name) + "_preview/", log_file)
elif x == 0:
    first_stitch("/home/ryan/Documents/full_circle/stitchwatch/", "/home/ryan/Documents/full_circle/" + str(dir_name) + "_preview/", log_file)

log_file = open(filename, "a+")
log_file.write("Stitched", jpg_name)
log_file.close()
