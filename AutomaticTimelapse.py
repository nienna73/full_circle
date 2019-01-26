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
# This is a local file path,
# if file_monitor is ever in a different directory
# than this file, it will need a full file path

def main():

    # Battery monitor voltage input to notify when batteries are dying
    try:
        battery_monitor = VoltageInput()
        textLCD = LCD()
    except RuntimeError as e:
        print("Runtime Exception: %s" % e.details)
        print("Exiting....")
        exit(1)

#####################################################################################################################################

### Error handler for battery monitor

    # Standard interface kit error handler
    # Shared by all the interface kits
    def interfaceKitError(e):
        try:
            source = e.device
            print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

#####################################################################################################################################

### Start battery monitor functions
    # Standard phidget attach handler for interval_rotator
    def BatteryMonitorAttached(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = battery_monitor.getDeviceSerialNumber()
            channelClass = battery_monitor.getChannelClassName()
            channel = battery_monitor.getChannel()

            deviceClass = battery_monitor.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = battery_monitor.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget detach handler for interval rotator
    def BatteryMonitorDetached(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = battery_monitor.getDeviceSerialNumber()
            channelClass = battery_monitor.getChannelClassName()
            channel = battery_monitor.getChannel()

            deviceClass = battery_monitor.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = battery_monitor.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Voltage change handler for interval_unit_toggle
    def BatteryMonitorVoltageChange(interfaceKit, voltage):
        # This is the handler for the interval variable
        output = (voltage - 2.5) / 0.06810
        # print(output)

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        battery_monitor.setOnAttachHandler(BatteryMonitorAttached)
        battery_monitor.setOnDetachHandler(BatteryMonitorDetached)
        battery_monitor.setOnErrorHandler(interfaceKitError)
        battery_monitor.setOnVoltageChangeHandler(BatteryMonitorVoltageChange)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End battery monitor functions

#####################################################################################################################################

### Start LCD functions

    # Standard attach handler for the LCD
    def LCDAttached(self):
        try:
            attached = self
            print("\nAttach Event Detected (Information Below)")
            print("===========================================")
            print("Library Version: %s" % attached.getLibraryVersion())
            print("Serial Number: %d" % attached.getDeviceSerialNumber())
            print("Channel: %d" % attached.getChannel())
            print("Channel Class: %s" % attached.getChannelClass())
            print("Channel Name: %s" % attached.getChannelName())
            print("Device ID: %d" % attached.getDeviceID())
            print("Device Version: %d" % attached.getDeviceVersion())
            print("Device Name: %s" % attached.getDeviceName())
            print("Device Class: %d" % attached.getDeviceClass())
            print("\n")

        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)

    # Standard detach handler for the LCD
    def LCDDetached(self):
        detached = self
        try:
            print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)

    # Standard error handler for the LCD
    def ErrorEvent(self, eCode, description):
        print("Error %i : %s" % (eCode, description))

    # Attach the handlers to the LCD, catch and return any errors
    try:
        textLCD.setOnAttachHandler(LCDAttached)
        textLCD.setOnDetachHandler(LCDDetached)
        textLCD.setOnErrorHandler(ErrorEvent)
        print("Waiting for the Phidget LCD Object to be attached...")
        textLCD.openWaitForAttachment(5000)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

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

    try:
        battery_monitor.setDeviceSerialNumber(120683)
        battery_monitor.setChannel(7)
        battery_monitor.open()
        print('Wait for rotator 0 attach...')
        battery_monitor.openWaitForAttachment(5000)
        time.sleep(1)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)


### Start monitor and timelapse functions

    # Force the user to confirm the settings
    ppoff = input("Is picutre profile off? ")
    raw_mode = input("Shooting in raw? ")
    pc_remote = input("Are the cameras in PC remote? ")


    # Define variables for use in the loop
    now = datetime.datetime.now()
    dir_name = now.strftime("%Y%m%d_%Hh%Mm%Ss")
    # path = "/home/ryan/" + str(dir_name)
    path = "/home/ryan/watchfile"       # This is where the program will look
                                        # for new images

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
        # Call to local import
        results = check_shutter_and_iso(filenames, path)

        # iso = results['iso']
        # shutter = results['shutter']

        iso = "100"
        shutter = "3"


        # Default is 0, !0 means new iso and shutter speed values
        # were found in the new file
        if iso != 0 and shutter != 0:
            print(iso)
            print(shutter)

            try:
                # Try to open the directory where the photos are stored,
                # if it doesn't exist, create it then navigate to it
                try:
                    os.chdir(str(dir_name))
                except:
                    make_dir = subprocess.Popen(["mkdir", str(dir_name)])
                    make_dir.wait()
                    os.chdir(str(dir_name))

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
                for port in camera_ports:
                    print(port)
                    subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + str(shutter), "--set-config-value", "iso=" + str(iso)])
                    # subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + str(shutter)])

                # Open an instance of capture.py for each camera, where:
                # x is the number-th photo taken (used for the filename)
                # i is the index of the camera port in a sorted list of ports
                i = 0
                process = ""
                while i < number_of_cameras:
                    process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/capture.py", str(x), str(i)])
                    i = i + 1
                process.wait()


                # Trigger the relay for simultaneous image capture
                # relay.setDutyCycle(1.0)
                # time.sleep(1)
                # relay.setDutyCycle(0.0)
                filenames = results['files']    # Update our records with the filename
                                                # of the picture we just used so we don't
                                                # take the same picture more than once

                x += 1
                os.chdir("../")                 # Change back a directory to prevent
                                                # creating multiple nested ones

                delay = 0
                if '/' in shutter:
                    delay = 1
                else:
                    delay = int(shutter)
                time.sleep(delay)
            except:
                print("\n error \n")
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
