import subprocess
import os
import sys
import time


def copy_to_drive(dir_name, x, number_of_cameras, drive_dir):
    full_dir_name = drive_dir + "/" + dir_name

    image_number = "%06d" % (x)

    j = 0
    while j < number_of_cameras:
        photo_name = "%06d" % (x) + "-" + chr(j+65) + ".arw"
        photo_location = "/home/ryan/Documents/full_circle/timelapse/" + dir_name + "/" + photo_name
        print("Move " + photo_name + " to external drive")
        process = subprocess.call(["mv", "-f", photo_location, full_dir_name])
        j += 1

    time.sleep(2)

    return
