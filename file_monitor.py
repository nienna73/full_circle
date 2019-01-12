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

from operator import itemgetter

def check_shutter_and_iso(old_files, path):
    # Initialize the variables to be used
    shutter_speed = 0
    iso = 0

    # Get, treat, and sort new files
    new_files = subprocess.check_output((["ls", "-al", path]))
    new_files = new_files.decode('utf-8')
    new_files = new_files.splitlines()

    new_files.sort()

    filenames = []

    for item in new_files:
        item = item.split()
        if len(item) > 2:
            entry = [item[7], item[8]]
            filenames.append(entry)
    filenames = sorted(filenames, key=itemgetter(0))

    # Check for new files
    for file in filenames:
        if file not in old_files:
            print(file)
            old_files.append(file)      # add anything new we see to the list
            if ".jpg" in file[1].lower() or ".arw" in file[1].lower():

                # Check the ISO for the file
                iso = subprocess.check_output(["exiftool", "-iso", path+'/'+file[1]])
                # Decode it to remove strange characters
                iso = iso.decode('utf-8')
                # Split it on ':' to access the integer value of ISO
                iso = iso.split(':')
                # Take the second list entry and strip unnecessary spaces from it
                iso = iso[1].strip()

                # Repeat the steps above for shutter speed
                shutter_speed = subprocess.check_output(["exiftool", "-shutterspeed", path+'/'+file[1]]).decode('utf-8').split(':')[1].strip()

                # Return the ISO and shutter speed in dictionary format for easy access
                return {'iso':iso, 'shutter':shutter_speed, 'files':old_files}

    return {'iso':iso, 'shutter':shutter_speed, 'files':old_files}
