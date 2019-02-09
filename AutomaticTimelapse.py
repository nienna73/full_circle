#!/usr/bin/env python

# This program runs parallel to another camera taking timelapse image
# at the same time. That camera passes along ISO and shutter speed
# information that is used for this system. Each time a new image is
# detected in the "watchfile" folder, the 360 rig is triggered
# to take a new photo with the new settings.

__author__ = 'Jolene Poulin'
__version__ = '0.1.2'
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

# This is a local file path,
# if file_monitor is ever in a different directory
# than this file, it will need a full file path

def main():

    # Battery monitor voltage input to notify when batteries are dying
    # try:
    #     battery_monitor = VoltageInput()
    #     textLCD = LCD()
    # except RuntimeError as e:
    #     print("Runtime Exception: %s" % e.details)
    #     print("Exiting....")
    #     exit(1)

#####################################################################################################################################

### Error handler for battery monitor

    # Standard interface kit error handler
    # Shared by all the interface kits
    # def interfaceKitError(e):
    #     try:
    #         source = e.device
    #         print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    #     except PhidgetException as e:
    #         print("Phidget Exception %i: %s" % (e.code, e.details))

#####################################################################################################################################

### Start battery monitor functions
    # Standard phidget attach handler for interval_rotator
    # def BatteryMonitorAttached(e):
    #     try:
    #         #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #         #www.phidgets.com/docs/Using_Multiple_Phidgets for information
    #
    #         print("\nAttach Event:")
    #
    #         """
    #         * Get device information and display it.
    #         """
    #         serialNumber = battery_monitor.getDeviceSerialNumber()
    #         channelClass = battery_monitor.getChannelClassName()
    #         channel = battery_monitor.getChannel()
    #
    #         deviceClass = battery_monitor.getDeviceClass()
    #         if (deviceClass != DeviceClass.PHIDCLASS_VINT):
    #             print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
    #                   "\n\t-> Channel " + str(channel) + "\n")
    #         else:
    #             hubPort = battery_monitor.getHubPort()
    #             print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
    #                   "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")
    #
    #     except PhidgetException as e:
    #         print("\nError in Attach Event:")
    #         #DisplayError(e)
    #         traceback.print_exc()
    #         return

    # Standard phidget detach handler for interval rotator
    # def BatteryMonitorDetached(e):
    #
    #     try:
    #         #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #         #www.phidgets.com/docs/Using_Multiple_Phidgets for information
    #
    #         print("\nDetach Event:")
    #
    #         """
    #         * Get device information and display it.
    #         """
    #         serialNumber = battery_monitor.getDeviceSerialNumber()
    #         channelClass = battery_monitor.getChannelClassName()
    #         channel = battery_monitor.getChannel()
    #
    #         deviceClass = battery_monitor.getDeviceClass()
    #         if (deviceClass != DeviceClass.PHIDCLASS_VINT):
    #             print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
    #                   "\n\t-> Channel " + str(channel) + "\n")
    #         else:
    #             hubPort = battery_monitor.getHubPort()
    #             print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
    #                   "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")
    #
    #     except PhidgetException as e:
    #         print("\nError in Detach Event:")
    #         #DisplayError(e)
    #         traceback.print_exc()
    #         return

    # Voltage change handler for interval_unit_toggle
    # def BatteryMonitorVoltageChange(interfaceKit, voltage):
    #     # This is the handler for the interval variable
    #     output = (voltage - 2.5) / 0.06810
        # print(output)

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    # try:
    #     battery_monitor.setOnAttachHandler(BatteryMonitorAttached)
    #     battery_monitor.setOnDetachHandler(BatteryMonitorDetached)
    #     battery_monitor.setOnErrorHandler(interfaceKitError)
    #     battery_monitor.setOnVoltageChangeHandler(BatteryMonitorVoltageChange)
    # except PhidgetException as e:
    #     print("Phidget Exception %i: %s" % (e.code, e.details))
    #     print("Exiting....")
    #     exit(1)

### End battery monitor functions

#####################################################################################################################################

### Start LCD functions

    # Standard attach handler for the LCD
    # def LCDAttached(self):
    #     try:
    #         attached = self
    #         print("\nAttach Event Detected (Information Below)")
    #         print("===========================================")
    #         print("Library Version: %s" % attached.getLibraryVersion())
    #         print("Serial Number: %d" % attached.getDeviceSerialNumber())
    #         print("Channel: %d" % attached.getChannel())
    #         print("Channel Class: %s" % attached.getChannelClass())
    #         print("Channel Name: %s" % attached.getChannelName())
    #         print("Device ID: %d" % attached.getDeviceID())
    #         print("Device Version: %d" % attached.getDeviceVersion())
    #         print("Device Name: %s" % attached.getDeviceName())
    #         print("Device Class: %d" % attached.getDeviceClass())
    #         print("\n")
    #
    #     except PhidgetException as e:
    #         print("Phidget Exception %i: %s" % (e.code, e.details))
    #         print("Press Enter to Exit...\n")
    #         readin = sys.stdin.read(1)
    #         exit(1)

    # Standard detach handler for the LCD
    # def LCDDetached(self):
    #     detached = self
    #     try:
    #         print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    #     except PhidgetException as e:
    #         print("Phidget Exception %i: %s" % (e.code, e.details))
    #         print("Press Enter to Exit...\n")
    #         readin = sys.stdin.read(1)
    #         exit(1)
    #
    # # Standard error handler for the LCD
    # def ErrorEvent(self, eCode, description):
    #     print("Error %i : %s" % (eCode, description))
    #
    # # Attach the handlers to the LCD, catch and return any errors
    # try:
    #     textLCD.setOnAttachHandler(LCDAttached)
    #     textLCD.setOnDetachHandler(LCDDetached)
    #     textLCD.setOnErrorHandler(ErrorEvent)
    #     print("Waiting for the Phidget LCD Object to be attached...")
    #     textLCD.openWaitForAttachment(5000)
    # except PhidgetException as e:
    #     print("Phidget Exception %i: %s" % (e.code, e.details))
    #     print("Exiting....")
    #     exit(1)

### End LCD functions

#####################################################################################################################################


    # The relay phidget was broken when I made this on Jan. 5th
    # so all the relay code is commented out for now

    # IMPORTANT:
    # This file is missing all the LCD screen handlers, will add them
    # later today (Jan 8th) if I have time,
    # otherwise will add later this week.

### Start relay functions

    # Connect to the relay, return an error if unsuccessful
    # try:
    #     relay = DigitalOutput()
    # except RuntimeError as e:
    #     print("Runtime Exception: %s" % e.details)
    #     print("Exiting....")
    #     exit(1)
    #
    # # Standard Phidget attach handler
    # def relayAttachHandler(e):
    #
    #     ph = relay
    #     try:
    #         #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #         #www.phidgets.com/docs/Using_Multiple_Phidgets for information
    #
    #         print("\nAttach Event:")
    #
    #         """
    #         * Get device information and display it.
    #         """
    #         serialNumber = ph.getDeviceSerialNumber()
    #         channelClass = ph.getChannelClassName()
    #         channel = ph.getChannel()
    #
    #         deviceClass = ph.getDeviceClass()
    #         if (deviceClass != DeviceClass.PHIDCLASS_VINT):
    #             print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
    #                   "\n\t-> Channel " + str(channel) + "\n")
    #         else:
    #             hubPort = ph.getHubPort()
    #             print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
    #                   "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")
    #
    #     except PhidgetException as e:
    #         print("\nError in Attach Event:")
    #         traceback.print_exc()
    #         return
    #
    # # Standard Phidget detach handler
    # def relayDetachHandler(e):
    #
    #     ph = relay
    #
    #     try:
    #         #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #         #www.phidgets.com/docs/Using_Multiple_Phidgets for information
    #
    #         print("\nDetach Event:")
    #
    #         """
    #         * Get device information and display it.
    #         """
    #         serialNumber = ph.getDeviceSerialNumber()
    #         channelClass = ph.getChannelClassName()
    #         channel = ph.getChannel()
    #
    #         deviceClass = ph.getDeviceClass()
    #         if (deviceClass != DeviceClass.PHIDCLASS_VINT):
    #             print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
    #                   "\n\t-> Channel " + str(channel) + "\n")
    #         else:
    #             hubPort = ph.getHubPort()
    #             print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
    #                   "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")
    #
    #     except PhidgetException as e:
    #         print("\nError in Detach Event:")
    #         #DisplayError(e)          # This line returns errors sometimes
    #         traceback.print_exc()
    #         return
    #
    # # Standard Phidget error handler
    # def relayErrorHandler(button, errorCode, errorString):
    #
    #     sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")
    #
    # # If the relay is connected/on,
    # # print a 1 to the LCD display
    # def relayStateChangeHandler(self, state):
    #     if(state == 1):
    #         print('relay')
    #
    #     text = str(state)
    #     textLCD.writeText(LCDFont.FONT_5x8, 13, 1, text)
    #     textLCD.flush()
    #
    #
    # #Setup for digital input
    # try:
    #     relay.setOnAttachHandler(relayAttachHandler)
    #     relay.setOnDetachHandler(relayDetachHandler)
    #     relay.setOnErrorHandler(relayErrorHandler)
    # except PhidgetException as e:
    #     print("Phidget Exception %i: %s" % (e.code, e.details))
    #     print("Exiting....")
    #     exit(1)
    #
    # try:
    #     relay.setDeviceSerialNumber(120683)   # Serial number for the 8/8/8
    #     relay.setChannel(0)                   # Looks for relay in port 0
    #     relay.open()
    #     print('Wait for relay attach...')
    #     relay.openWaitForAttachment(5000)     # Waits 5 seconds before timeout error
    # except PhidgetException as e:
    #     PrintOpenErrorMessage(e, ch)
    #     raise EndProgramSignal("Program Terminated: Digital Input Open Failed")


### End relay functions
### General Phidget Functions

    # try:
    #     battery_monitor.setDeviceSerialNumber(120683)
    #     battery_monitor.setChannel(7)
    #     battery_monitor.open()
    #     print('Wait for rotator 0 attach...')
    #     battery_monitor.openWaitForAttachment(5000)
    #     time.sleep(1)
    # except PhidgetException as e:
    #     print("Phidget Exception %i: %s" % (e.code, e.details))
    #     print("Exiting....")
    #     exit(1)


### Start monitor and timelapse functions

    # Force the user to confirm the settings
    ppoff = input("Is picutre profile off? ")
    raw_mode = input("Shooting in raw? ")
    pc_remote = input("Are the cameras in PC remote? ")
    # bulb_on = input("Are the cameras in BULB mode? ")
    with_audio = input("Are you recording with audio? (y/n): ")
    # add question for stitching as you go
    stitching = input("Do you want to stitch as you go? (y/n): ")


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
        input_files = open("/home/ryan/Documents/full_circle/stitchwatch/input_files.txt", "w+")
        input_files.truncate(0)
        input_files.write("file '/home/ryan/Documents/full_circle/" + str(dir_name) + "_preview/full-stitched-video.mp4'\n")
        input_files.write("file '/home/ryan/Documents/full_circle/" + str(dir_name) + "_preview/newest-video-frame.mp4'\n")
        input_files.close()

    # Start recording audio if specified
    if with_audio.lower() == 'y':
        subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/capture_audio.py", str(dir_name)])

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

        # If we're recording with audio,
        # check to see if the audio record program is running,
        # restart it if it isn't

        # Get a list of all processes that are currently running
        # and decode them so they can be easily processed
        processes = subprocess.check_output(["ps", "-ef"])
        processes_list = processes.split()
        for i in range(0, len(processes_list)):
            processes_list[i] = processes_list[i].decode('utf-8')

        if with_audio.lower() == 'y':
            if not '/home/ryan/Documents/full_circle/capture_audio.py' in processes_list:
                subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/capture_audio.py", str(dir_name)])
                print('Relaunching Audio')


        # Default is 0, !0 means new iso and shutter speed values
        # were found in the new file
        if iso != 0 and shutter != 0:
            print(iso)
            print(shutter)

            camera_ports = []       # stores relevant ports

            # Locate all cameras and split results into readable strings
            ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
            ports_strings_split = ports_strings.split()


            # Locate all ports of format usb:xxx,xxx
            # as they're needed for gphoto2
            for item in ports_strings_split:
                item = item.decode('utf-8')
                if item[0] == 'u':
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

                for port in camera_ports:
                    print(port)
                    subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + str(shutter), "--set-config-value", "iso=" + str(iso)])

                # Open an instance of capture.py for each camera, where:
                # x is the number-th photo taken (used for the filename)
                # i is the index of the camera port in a sorted list of ports
                i = 0
                process = ''
                while i < number_of_cameras:
                    process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/capture.py", str(x), str(i), str(shutter)])
                    i = i + 1
                process.wait()


                # Trigger the relay for simultaneous image capture
                # relay.setDutyCycle(1.0)
                # time.sleep(1)
                # relay.setDutyCycle(0.0)
                filenames = results['files']    # Update our records with the filename
                                                # of the picture we just used so we don't
                                                # take the same picture more than once

                if stitching.lower() == 'y':
                    # Try moving the .arw files to stitchwatch so they can
                    # be stitched
                    try:
                        j = 0
                        while j < number_of_cameras:
                            photo_name = "%06d" % (x+1) + "-" + chr(j+65) + ".arw"
                            print(photo_name)
                            process = subprocess.call(["cp", "-f", photo_name, "/home/ryan/Documents/full_circle/stitchwatch/"])
                            j += 1
                        time.sleep(6)
                    except NameError as e:
                        # Print error to the screen and to the log file
                        print("\nError in moving files to stitchwatch\n")
                        print(e)
                        log_file = open(filename, "a+")
                        log_file.write("Error in moving files to /stitchwatch")
                        log_file.close()

                    # Try editing and renaming the .pts file
                    try:
                        if x > 0:
                            old_number = "%06d" % (x)
                            new_number = "%06d" % (x+1)
                            old_path = "/home/ryan/Documents/full_circle/stitchwatch/" + old_number + "-A.pts"
                            new_path = "/home/ryan/Documents/full_circle/stitchwatch/" + new_number + "-A.pts"
                            command = "sed 's/%s/%s/g' %s > %s" % (old_number, new_number, old_path, new_path)
                            process = subprocess.call([command], shell=True)
                        else:
                            subprocess.call(["cp", "-f", "/home/ryan/Documents/full_circle/template.pts", "/home/ryan/Documents/full_circle/stitchwatch/000001-A.pts"])
                    except NameError as e:
                        # Print error to the screen and to the log file
                        print("Error in renaming .pts file")
                        print(e)
                        log_file = open(filename, "a+")
                        log_file.write("Error in renaming .pts file")
                        log_file.close()
                    except AttributeError as e:
                        print(e)

                    subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/wait_for_stitch.py", str(x), str(dir_name), str(log_file)])



                x += 1
                # os.chdir("../")                 # Change back a directory to prevent
                                                # creating multiple nested ones

                delay = 0
                if '/' in shutter:
                    delay = 1
                else:
                    delay = float(shutter)
                time.sleep(delay)
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


    # Close the relay
    # This realistically never gets called as the program is only terminated
    # manually or by error, so the relay never gets properly closed
    # try:
    #
    #     relay.close()
    # except PhidgetException as e:
    #     print("Phidget Exception %i: %s" % (e.code, e.details))
    #     print("Exiting....")
    #     exit(1)


main()
