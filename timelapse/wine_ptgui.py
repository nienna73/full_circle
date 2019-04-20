import subprocess
import os
import sys
import time
from video_stitch import video_stitch, first_stitch

# x = int(sys.argv[1])        # number of the photo one before the one we just took
# dir_name = sys.argv[2]      # location where all .arw files are stored
#
# filename = sys.argv[3]

def wine_ptgui(x, dir_name, filename):
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

    return
