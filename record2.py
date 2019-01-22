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
import datetime

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

    has_audio = False                       # a bool to store whether or not
                                            # we can record with the Zoom device

    # Get a string of all connected audio devices,
    # decode the string to remove strange characters,
    # split the string into a list to be treated
    audio_devices = subprocess.check_output(["arecord", "--list-devices"])
    audio_devices = audio_devices.decode('utf-8')
    audio_devices = audio_devices.split()

    for device in audio_devices:
        if device.lower() == "h2n":
            has_audio = True

    # Record video based on the criteria passed in
    while (x < total_videos):
        print("Running record")

        if has_audio:
            print("Recording with audio")
            # If the Zoom device is connected, take all the steps to record
            # audio, otherwise continue with just video

            # Make a new folder here as YYYYMMDD_SCENE-0X if that
            # folder doesn't already exist

            # Get the current date and format it
            now = datetime.datetime.now()
            dir_name = now.strftime("%Y%m%d")

            dir_name = dir_name + "_SCENE" + "%02d" % (x + 1)
            # Try opening a directory with the name created above
            # If the directory can't be opened, create a directory
            # with that name and navigate to it
            try:
                os.chdir(str(dir_name))
            except:
                make_dir = subprocess.Popen(["mkdir", str(dir_name)])
                make_dir.wait()
                os.chdir(str(dir_name))

            subprocess.Popen(["arecord", "-d", str(video_length), "-t", "wav", "--use-strftime", "%Y%m%d_%Hh%Mm%vs.wav", "-c", "4", "-f", "S24_LE", "-r48000"])
            # The preferred format is:
            # arecord -d 10 -t wav --use-strftime %Y%m%d_%Hh%Mm%vs.wav -c 4 -f S24_LE -r48000

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

        if has_audio:
            # Naviagte to the previous directory to prevent nested directories
            # Only do this is recording with audio as new folders are
            # only created for audio
            os.chdir("../")

main()
