import subprocess
import os
import sys
import time


def wine_ptgui(x, dir_name, filename):
    full_dir_name = "/home/ryan/Documents/full_circle/timelapse/" + dir_name + "/"

    # Run wine and wait for it to finish

    stitch_file = "%06d" % (x+1) + "-A.pts"
    process = subprocess.Popen(["wine", "/home/ryan/Desktop/PTGui.exe", "-batch", "-x", stitch_file])
    process.wait(45)

    # Check for the stitched image in the directory
    jpg_img_check = subprocess.check_output(["ls", "-al", full_dir_name])
    jpg_img_check = jpg_img_check.decode('utf-8')

    jpg_img_name = "%06d" % (x+1) + "-A.jpg"

    # Return 0 if the image is found,
    # return -1 otherwise
    if jpg_img_name in jpg_img_check:
        return 0
    else:
        return -1
