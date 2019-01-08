# This function is used by AutomaticTimelapse
# to check a folder at a given path and see if there are any new
# files in it that are not included in the initial list of files,
# which is also provided. If there is a new file and it contains
# the extension .jpg or .arw, we check its ISO and shutterspeed, which
# are returned as a dictionary for use by AutomaticTimelapse

# This function takes in two arguments:
# 1. A list of files that we know are in the folder/directory
# 2. The path to the directory to be checked

# This function assumes that only one new file is added each time we check

__author__ = 'Jolene Poulin'
__version__ = '0.1.2'
__date__ = 'January 5th, 2019'

# General imports
import sys
import time
import subprocess
import os

def check_shutter_and_iso(old_files, path):
    # Initialize the variables to be used
    shutter_speed = 0
    iso = 0
    new_files = os.listdir(path)

    # Check for new files
    for file in new_files:
        if file not in old_files:
            print(file)
            if ".jpg" in file.lower() or ".arw" in file.lower():

                # Check the ISO for the file
                iso = subprocess.check_output(["exiftool", "-iso", path+'/'+file])
                # Decode it to remove strange characters
                iso = iso.decode('utf-8')
                # Split it on ':' to access the integer value of ISO
                iso = iso.split(':')
                # Take the second list entry and strip unnecessary spaces from it
                iso = iso[1].strip()

                # Repeat the steps above for shutter speed
                shutter_speed = subprocess.check_output(["exiftool", "-shutterspeed", path+'/'+file]).decode('utf-8').split(':')[1].strip()

    # Return the ISO and shutter speed in dictionary format for easy access
    return {'iso':iso, 'shutter':shutter_speed}
