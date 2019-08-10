#!/usr/bin/env python

# This program runs parallel to another camera taking timelapse image
# at the same time. That camera passes along ISO and shutter speed
# information that is used for this system. Each time a new image is
# detected in the "watchfile" folder, the 360 rig is triggered
# to take a new photo with the new settings.

__author__ = 'Jolene Poulin'
__version__ = '0.1.7'
__date__ = 'January 5th, 2019'

#standard imports
import sys
import time
import subprocess
import os
import datetime

#phidget imports
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.LCD import *
from Phidget22.Phidget import *

#custom imports
from file_monitor import check_shutter_and_iso
from video_stitch import video_stitch, first_stitch
from copy_to_drive import copy_to_drive

# This is a local file path,
# if file_monitor is ever in a different directory
# than this file, it will need a full file path

def getDriveName():
    drive_names = subprocess.check_output(["df", "-T"])
    drive_names = drive_names.decode("utf-8")
    split_names = drive_names.split("\n")

    path = ""

    for name in split_names:
        if "fuseblk" in name:
            info = name.split()
            path = info[-1]
            return path

    return path

def main():

### Start monitor and timelapse functions

    # Force the user to confirm the settings
    ppoff = input("Is picture profile off? ")
    raw_mode = input("Shooting in raw? ")
    pc_remote = input("Are the cameras in PC remote? ")
    # bulb_on = input("Are the cameras in BULB mode? ")
    with_audio = input("Are you recording with audio? (y/n): ")
    # add question for stitching as you go
    stitching = input("Do you want to stitch as you go? (y/n): ")
    move_to_drive = input("Do you want to move the raws to an external drive? (y/n): ")
    drive_name = ""
    if move_to_drive.lower() == 'y':
        drive_connected = input("Is the 4TB drive connected? ")
        drive_name = getDriveName()
        if drive_name == "":
            cont = input("Could not locate external drive. Continue without moving to drive? (y/n): ")
            if cont.lower() == 'n':
                exit()

    print("Ready to go!\n")


    # Define variables for use in the loop
    now = datetime.datetime.now()
    dir_name = now.strftime("%Y%m%d_%Hh%Mm%Ss")
    # path = "/home/ryan/" + str(dir_name)
    path = "/home/ryan/watchfile"       # This is where the program will look
                                        # for new images

    # Try to open the directory where the photos are stored,
    # if it doesn't exist, create it then navigate to it
    try:
        os.chdir(str(dir_name))
    except:
        # Create a new folder to store the stitched preview
        if stitching.lower() == 'y':
            preview_dir = subprocess.Popen(["mkdir", str(dir_name) + "_preview"])
            preview_dir.wait()

        if move_to_drive.lower() == 'y':
            # The numbers in the drive name might change every time it's connected
            # look into this to prevent future issues
            full_dir_name = drive_name + "/" + str(dir_name)
            drive_dir = subprocess.Popen(["mkdir", full_dir_name])
            drive_dir.wait()



        make_dir = subprocess.Popen(["mkdir", str(dir_name)])
        make_dir.wait()
        os.chdir(str(dir_name))

        # Create a log file the first time the directory is opened,
        # write to it, then close it
        filename = str(dir_name) + "_log.txt"
        error_file = open(filename, "w+")
        error_file.write("Start of Error logs from " + str(dir_name))
        error_file.close()

        # Change the location of the mp4's to the correct filepath
        input_files = open("/home/ryan/watchfile/input_files.txt", "w+")
        input_files.truncate(0)
        input_files.write("file '/home/ryan/Documents/full_circle/timelapse/" + str(dir_name) + "_preview/full-stitched-video.mp4'\n")
        input_files.write("file '/home/ryan/Documents/full_circle/timelapse/" + str(dir_name) + "_preview/newest-video-frame.mp4'\n")
        input_files.close()

    # Start recording audio if specified
    if with_audio.lower() == 'y':
        subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/capture_audio.py", str(dir_name)])

    # Use this for sorting image files and to not skip images that are added
    # to the watchfile while the cameras are capturing
    # Get, treat, and sort the files in the directory
    files = subprocess.check_output((["ls", "-al", path]))
    files = files.decode('utf-8')
    files = files.splitlines()

    filenames = []

    for item in files:
        item = item.split()
        if len(item) > 2:
            entry = [item[7], item[8]]
            filenames.append(entry)
    filenames.sort()


    x = 0                               # Used to name images taken,
                                        # keeps track of how many images were taken
    while True:
        log_file = open(filename, "a+")
        # Call to local import
        results = check_shutter_and_iso(filenames, path, log_file)
        log_file.close()

        iso = results['iso']
        shutter = results['shutter']

        if with_audio.lower() == 'y':
            # If we're recording with audio,
            # check to see if the audio record program is running,
            # restart it if it isn't

            # Get a list of all processes that are currently running
            # and decode them so they can be easily processed
            processes = subprocess.check_output(["ps", "-ef"])
            processes_list = processes.split()
            for i in range(0, len(processes_list)):
                processes_list[i] = processes_list[i].decode('utf-8')

            if not '/home/ryan/Documents/full_circle/timelapse/capture_audio.py' in processes_list:
                subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/capture_audio.py", str(dir_name)])
                print('Relaunching Audio')


        # Default is 0, !0 means new iso and shutter speed values
        # were found in the new file
        if iso != 0 and shutter != 0:

            if "." in shutter:
                if "0.3" in shutter or "0.4" in shutter:
                    shutter = "1/3"
                elif "0.5" in shutter or "0.6" in shutter:
                    shutter = "1/2"
                elif "0.8" in shutter:
                    shutter = "1"

            print("Iso: " + iso)
            print("Shutter speed: " + shutter)

            camera_ports = []       # stores relevant ports

            # Locate all cameras and split results into readable strings
            # Remove the Canon camera
            ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
            ports_strings_split = ports_strings.splitlines()

            for string in ports_strings_split:
                string_decode = string.decode('utf-8')
                if 'sony' not in string_decode.lower():
                    ports_strings_split.remove(string)

            for string in ports_strings_split:
                string = string.decode('utf-8').split()
                for item in string:
                    if item[0].lower() == 'u':
                        camera_ports.append(item)

            # Set the ISO and shutter speed of each camera
            number_of_cameras = len(camera_ports)


            # Re-open the log file in append mode
            log_file = open(filename, "a+")
            log_file.write("Input ISO: " + iso + '\n')
            log_file.write("Input Shutter Speed: " + shutter + '\n')
            log_file.write("Output filename: " + "%06d" % (x + 1) + '\n\n')
            log_file.close()

            try:
                float_shutter = 0
                if '/' in shutter:
                    float_shutter = shutter.split('/')
                    float_shutter = int(float_shutter[0]) / int(float_shutter[1])
                else:
                    float_shutter = float(shutter)

                if float_shutter <= 1.0:
                    # Use standard capture if the shutter speed is fast enough
                    for port in camera_ports:
                        print(port)
                        subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + str(shutter), "--set-config-value", "iso=" + str(iso)])

                    # Open an instance of capture.py for each camera, where:
                    # x is the number-th photo taken (used for the filename)
                    # i is the index of the camera port in a sorted list of ports
                    i = 0
                    process = ''
                    while i < number_of_cameras:
                        process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/capture.py", str(x), str(i), str(shutter)])
                        i = i + 1
                    process.wait()

                else:
                    # Use bulb capture if the shutter speed is slow
                    for port in camera_ports:
                        print(port)
                        subprocess.call(["gphoto2", "--port=" + port, "--set-config", "shutterspeed=bulb", "--set-config-value", "iso=" + str(iso)])

                    i = 0
                    process = ""
                    while i < number_of_cameras:
                        process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/bulb_capture_on.py", str(i)])
                        i = i + 1
                    process.wait()

                    wait_time = 0
                    if '/' in shutter:
                        split_shutter = shutter.split('/')
                        wait_time = int(split_shutter[0]) / int(split_shutter[1])
                    else:
                        wait_time = float(shutter)

                    time.sleep(wait_time)

                    j = 0
                    while j < number_of_cameras:
                        process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/bulb_capture_off.py", str(x), str(j)])
                        j = j + 1
                    process.wait()

                    time.sleep(5)


                # Trigger the relay for simultaneous image capture
                # relay.setDutyCycle(1.0)
                # time.sleep(1)
                # relay.setDutyCycle(0.0)
                filenames = results['files']    # Update our records with the filename
                                                # of the picture we just used so we don't
                                                # take the same picture more than once

                # Check that 6 photos were taken
                # Print an error and exit if there are fewer than 6 images
                k = 0
                while k < 6:
                    f_name = "%06d" % (x + 1) + "-" + str(chr(65 + k)) + ".arw"
                    if not os.path.isfile(f_name):
                        print(f"\n\n\n****** ERROR ******\n\nThere was an error with camera {k}\nExiting to prevent further errors\n\n\n")
                        os._exit(1)
                    k += 1

                if stitching.lower() == 'y':
                    # Call the stitching function
                    wine_process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/wine_stitch.py", str(x), str(dir_name), str(filename), str(move_to_drive), str(len(camera_ports)), str(drive_name)])
                    # wine_process.wait()

                x += 1
                # os.chdir("../")                 # Change back a directory to prevent
                                                # creating multiple nested ones

                time.sleep(3)

            except:
                e = sys.exc_info()[0]
                print("\n error \n")
                print(e)
                print("\n")

                # Re-open the log file in append mode
                log_file = open(filename, "a+")
                log_file.write(str(e) + '\n\n')
                log_file.close()

                time.sleep(1)

        time.sleep(2)


main()
