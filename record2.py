# Despite this file's name, this is the main file
# used to record videos. It takes in 3 arguments:
# 1. The length of each video, in seconds
# 2. The total number of videos to be taken, as an integer
# 3. The amount of time to wait between videos, in seconds
# This program gets called by TimelapseMagic

__author__ = 'Jolene Poulin'
__version__ = '0.2.1'
__date__ = 'April 30th, 2018'

# General imports
import subprocess
import time
import sys
import os

def main():
    # Gather information from arguments passed to function
    video_length = int(sys.argv[1])
    # 29 minutes = 1740s
    total_videos = int(sys.argv[2])
    interval = int(sys.argv[3])


    camera_ports = []       # A list of relevant camera ports
    x = 0                   # Number of videos already recorded

    # Detect all cameras
    ports_string = subprocess.check_output(["gphoto2", "--auto-detect"])
    ports_string_split = ports_string.split()

    # Decode strings and find entries of format "usb:xxx,xxx"
    # as these are the camera ports
    for item in ports_string_split:
        item = item.decode('utf-8')
        if item[0] == 'u':
            camera_ports.append(item)

    camera_ports.sort(reverse = True)       # Sort so the cameras are triggered
                                            # in a sensible order

    # Record video based on the criteria passed in
    while (x < total_videos):
        print('running record')

        dir_name = "SCENE" + "%02d" % (x + 1)
        # Try opening a directory with the name created above
        # If the directory can't be opened, create a directory
        # with that name and navigate to it
        try:
            os.chdir(str(dir_name))
        except:
            make_dir = subprocess.Popen(["mkdir", str(dir_name)])
            make_dir.wait()
            os.chdir(str(dir_name))

        subprocess.Popen(["arecord", "-d", str(video_length), "-f", "cd", "-t", "wav", "--use-strftime", "%Y%m%d_%Hh%Mm%vs.wav"])

        # Start recording on each camera
        for port in camera_ports:
            subprocess.call(["gphoto2", "--port=" + port, "--set-config", "movie=1"])

        # Wait for the desired video length
        time.sleep(video_length)

        # Stop recording on each camera
        for port in camera_ports:
            subprocess.call(["gphoto2", "--port=" + port, "--set-config", "movie=0"])

        # Increment the counter for how many videos have been taken
        # and wait for the desired interval between videos
        x = x + 1
        time.sleep(interval)

        # Naviagte to the previous directory to prevent nested directories
        os.chdir("../")

main()
