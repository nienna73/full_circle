#!/usr/bin/env python

# This is the main file used to run the Phidget Timelapse program
# This file has a desktop shortcut, TimelapseMagic.desktop, which is
# started on machine startup. There's a file in the Google Drive that
# gives an overview of this file:
# https://docs.google.com/document/d/11WEyHnqQRX04gypeKa7C_SSdZmS9sN6zzPuxRPaHsrA/edit?ts=5c34e415

# This file provides an interface to phidget objects, gphoto2, the cameras,
# the system, and subprocesses running on the machine
# Further description can be found at each function

# This file was adapated from the files in the "reference_files" folder,
# which was initially created by Adam Stelmack and Ryan Jackson
# This file was created by Jolene Poulin with great help from Ryan Jackson
# and Sam Brooks, starting around April 30th, 2018

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'May 17 2010'

#Basic imports
from ctypes import *
import sys
import os
import random
import signal
import subprocess
import datetime
import math
from time import sleep

#Phidget specific imports
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.LCD import *
#from Phidget22.Devices.GPS import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageInput import *

# Local imports
from video_stitch import video_stitch
# this is a local filepath


def main():

### Start User-Defined functions

    # These need to be at the beginning of the file to prevent reference errors

    # User-defined function to convert the voltage from shutter_speed
    # to a usable shutter speed value
    # It returns the shutter speed
    def getShutterSpeed():
        # Get the shutter speed and convert it from voltage to shutter speed

        # This section decides the shutter speed of the cameras based
        # on the position of the shutter speed slider. These values were
        # selected from a list provided by Ryan, and the intervals were decided
        # with math. The extra spaces in "output" are there to ensure no
        # trailing characters remain on the display when the value changes
        shutterSpeedVoltage = shutter_speed.getSensorValue()
        shutterSpeedValue = ""
        if (shutterSpeedVoltage <= 0.357):
            shutterSpeedValue = "10"
        elif (0.357 < shutterSpeedVoltage <= 0.714):
            shutterSpeedValue = "4"
        elif (0.714 < shutterSpeedVoltage <= 1.071):
            shutterSpeedValue = "2"
        elif (1.071 < shutterSpeedVoltage <= 1.428):
            shutterSpeedValue = "1"
        elif (1.428 < shutterSpeedVoltage <= 1.785):
            shutterSpeedValue = "1/30"
        elif (1.785 < shutterSpeedVoltage <= 2.142):
            shutterSpeedValue = "1/50"
        elif (2.142 < shutterSpeedVoltage <= 2.499):
            shutterSpeedValue = "1/100"
        elif (2.499 < shutterSpeedVoltage <= 2.856):
            shutterSpeedValue = "1/250"
        elif (2.856 < shutterSpeedVoltage <= 3.213):
            shutterSpeedValue = "1/400"
        elif (3.213 < shutterSpeedVoltage <= 3.57):
            shutterSpeedValue = "1/500"
        elif (3.57 < shutterSpeedVoltage <= 3.927):
            shutterSpeedValue = "1/800"
        elif (3.927 < shutterSpeedVoltage <= 4.284):
            shutterSpeedValue = "1/1000"
        elif (4.284 < shutterSpeedVoltage <= 4.641):
            shutterSpeedValue = "1/1600"
        elif (4.641 < shutterSpeedVoltage):
            shutterSpeedValue = "1/2000"

        return shutterSpeedValue

    # User-defined function to get the iso value from the slider voltage
    # It returns the iso
    def getIso():

        # This is very similar to the shutter speed function above
        isoSensorValue = iso.getSensorValue()
        isoValue = ""
        if (isoSensorValue <= 0.714):
            isoValue = "100"
        elif (0.714 < isoSensorValue <= 1.428):
            isoValue = "800"
        elif (0.1428 < isoSensorValue <= 2.142):
            isoValue = "1600"
        elif (2.142 < isoSensorValue <= 2.856):
            isoValue = "3200"
        elif (2.856 < isoSensorValue <= 3.57):
            isoValue = "6400"
        elif (3.57 < isoSensorValue <= 4.284):
            isoValue = "12800"
        elif (4.2824 < isoSensorValue):
            isoValue = "25600"

        return isoValue

    # User-defined function to get the video length from the raw voltage input
    # It returns the video length in minutes
    def getVideoLength():
        # Get the total length the program should run for and convert it from
        # voltage to an integer
        rawLength = video_length_rotator.getSensorValue() * 10
        if (rawLength <= 4.9):
            length = 1
        elif (4.9 < rawLength <= 9.8):
            length = 2
        elif (9.8 < rawLength <= 14.7):
            length = 3
        elif (14.7 < rawLength <= 19.6):
            length = 4
        elif (19.6 < rawLength <= 24.5):
            length = 5
        elif (24.5 < rawLength <= 29.4):
            length = 10
        elif (29.4 < rawLength <= 34.3):
            length = 15
        elif (34.3 < rawLength <= 39.2):
            length = 20
        elif (39.2 < rawLength <= 44.1):
            length = 25
        elif (44.1 < rawLength):
            length = 29

        return length

    # User-defined function to get the video delay from the raw voltage input
    # It returns the video delay as a string
    def getVideoDelayStr():
        # Get the total length the program should run for and convert it from
        # voltage to an integer
        rawLength = video_delay_rotator.getSensorValue() * 10
        if (rawLength <= 1.0):
            length = '0'
        elif (1.0 < rawLength <= 9.9):
            length = '10s'
        elif (9.9 < rawLength <= 19.9):
            length = '30s'
        elif (19.9 < rawLength <= 29.9):
            length = '1m '
        elif (29.9 < rawLength <= 39.9):
            length = '2m '
        elif (39.9 < rawLength):
            length = '5m '

        return length

    # User-defined function to get the video delay from the raw voltage input
    # It returns the video delay as an integer in seconds
    def getVideoDelayInt():
        # Get the total length the program should run for and convert it from
        # voltage to an integer
        rawLength = video_delay_rotator.getSensorValue() * 10
        if (rawLength <= 1.0):
            length = 0
        elif (1.0 < rawLength <= 9.9):
            length = 10
        elif (9.9 < rawLength <= 19.9):
            length = 30
        elif (19.9 < rawLength <= 29.9):
            length = 60
        elif (29.9 < rawLength <= 39.9):
            length = 120
        elif (39.9 < rawLength):
            length = 300

        return length

    # User-defined function to locate and update the settings on all cameras
    # It returns a list of camera ports
    def locateAndUpdateCameras(s_speed, i_value):
        cameras = []    # to hold ports, to be returned
        # Detect all the cameras
        ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
        ports_strings_split = ports_strings.split()

        # Find all the ports of format "usb:xxx,xxx"
        for item in ports_strings_split:
            item = item.decode('utf-8')
            if item[0] == 'u':
                cameras.append(item)

        # Inform the user to wait while we update the settings
        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'WAIT')
        textLCD.flush()

        if "." in s_speed:
            if "3" in s_speed or "4" in s_speed:
                s_speed = "1/3"
            elif "5" in s_speed or "6" in s_speed:
                s_speed = "1/2"
            elif "8" in s_speed:
                s_speed = "1"
            print(s_speed)

        # Update the shutter speed and iso on each camera
        for port in cameras:
            print(port)
            subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + s_speed, "--set-config-value", "iso=" + i_value])

        return cameras

    # User-defined function to close all phidgets
    def closeAllPhidgets():
        interval_rotator.setOnVoltageChangeHandler(None)
        interval_rotator.setOnSensorChangeHandler(None)
        interval_rotator.close()
        total_time_rotator.setOnVoltageChangeHandler(None)
        total_time_rotator.setOnSensorChangeHandler(None)
        total_time_rotator.close()
        video_length_rotator.setOnVoltageChangeHandler(None)
        video_length_rotator.setOnSensorChangeHandler(None)
        video_length_rotator.close()
        video_delay_rotator.setOnVoltageChangeHandler(None)
        video_delay_rotator.setOnSensorChangeHandler(None)
        video_delay_rotator.close()
        shutter_speed.setOnVoltageChangeHandler(None)
        shutter_speed.setOnSensorChangeHandler(None)
        shutter_speed.close()
        iso.setOnVoltageChangeHandler(None)
        iso.setOnSensorChangeHandler(None)
        iso.close()
        light_sensor.setOnVoltageChangeHandler(None)
        light_sensor.setOnSensorChangeHandler(None)
        light_sensor.close()
        run_button.setOnStateChangeHandler(None)
        run_button.close()
        kill_button.setOnStateChangeHandler(None)
        kill_button.close()
        mode_toggle.setOnStateChangeHandler(None)
        mode_toggle.close()
        interval_unit_toggle.setOnStateChangeHandler(None)
        interval_unit_toggle.close()
        total_time_unit_toggle.setOnStateChangeHandler(None)
        total_time_unit_toggle.close()
        LCD_on_off_toggle.setOnStateChangeHandler(None)
        LCD_on_off_toggle.close()
        textLCD.close()
        relay.close()
        #gps.close()

### End User-Defined functions

#####################################################################################################################################


    # Create objects for toggles, sensors, rotators, and sliders on the rig
    try:
        interval_rotator = VoltageInput()
        total_time_rotator = VoltageInput()
        video_length_rotator = VoltageInput()
        video_delay_rotator = VoltageInput()
        shutter_speed = VoltageInput()
        iso = VoltageInput()
        light_sensor = VoltageInput()
        run_button = DigitalInput()
        kill_button = DigitalInput()
        mode_toggle = DigitalInput()
        interval_unit_toggle = DigitalInput()
        total_time_unit_toggle = DigitalInput()
        LCD_on_off_toggle = DigitalInput()
        relay = DigitalOutput()
    except RuntimeError as e:
        print("Runtime Exception: %s" % e.details)
        print("Exiting....")
        exit(1)

    #Create an TextLCD object and a GPS object
    try:
        textLCD = LCD()
        #gps = GPS()
    except RuntimeError as e:
        print("Runtime Exception: %s" % e.details)
        print("Exiting....")
        exit(1)

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

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        textLCD.setOnAttachHandler(LCDAttached)
        textLCD.setOnDetachHandler(LCDDetached)
        textLCD.setOnErrorHandler(ErrorEvent)
        textLCD.openWaitForAttachment(5000)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End LCD functions

#####################################################################################################################################

### Error handler for the phidgets below

    # Standard interface kit error handler
    # Shared by all the interface kits
    def interfaceKitError(e):
        try:
            source = e.device
            print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

#####################################################################################################################################

### Start interval rotator functions
    # Standard phidget attach handler for interval_rotator
    def intervalRotatorAttached(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = interval_rotator.getDeviceSerialNumber()
            channelClass = interval_rotator.getChannelClassName()
            channel = interval_rotator.getChannel()

            deviceClass = interval_rotator.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = interval_rotator.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget detach handler for interval rotator
    def intervalRotatorDetached(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = interval_rotator.getDeviceSerialNumber()
            channelClass = interval_rotator.getChannelClassName()
            channel = interval_rotator.getChannel()

            deviceClass = interval_rotator.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = interval_rotator.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Voltage change handler for interval_unit_toggle
    def intervalRotatorVoltageChange(interfaceKit, voltage):
        # This is the handler for the interval variable

        output = int(voltage*10)
        # If the toggle is off, the units are in seconds
        if (interval_unit_toggle.getState() == 0):
            units = 's'
        # If the toggle is on, the units are in minutes
        elif (interval_unit_toggle.getState() == 1):
            units = 'm'

        # This quickest we can take photos is 4 seconds apart
        # due to download speeds
        if (interval_unit_toggle.getState() == 0 and output < 4):
            output = 4

        # Update the LCD display to reflect the changes made
        text = "I:" + str(output) + units + " "
        textLCD.writeText(LCDFont.FONT_5x8, 0, 0, text)
        textLCD.flush()     # Don't forget this!

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        interval_rotator.setOnAttachHandler(intervalRotatorAttached)
        interval_rotator.setOnDetachHandler(intervalRotatorDetached)
        interval_rotator.setOnErrorHandler(interfaceKitError)
        interval_rotator.setOnVoltageChangeHandler(intervalRotatorVoltageChange)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End interval rotator functions

#####################################################################################################################################

### Start total time rotator functions

    # Standard phidget attach handler for total_time_rotator
    def totalTimeRotatorAttached(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = total_time_rotator.getDeviceSerialNumber()
            channelClass = total_time_rotator.getChannelClassName()
            channel = total_time_rotator.getChannel()

            deviceClass = total_time_rotator.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = total_time_rotator.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget detach handler for total_time_rotator
    def totalTimeRotatorDetached(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = total_time_rotator.getDeviceSerialNumber()
            channelClass = total_time_rotator.getChannelClassName()
            channel = total_time_rotator.getChannel()

            deviceClass = total_time_rotator.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = total_time_rotator.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # This is the handler for when the total time rotator is changed
    def totalTimeRotatorVoltageChange(interfaceKit, voltage):
        # This affects the total time the program runs for,
        # whether that's for video or stills

        output = int(voltage*10)
        # If the toggle is off, the units are in minutes
        if (total_time_unit_toggle.getState() == 0):
            units = 'm'
        # If the toggle is on, the units are in hours
        elif (total_time_unit_toggle.getState() == 1):
            units = 'h'

        # Update the LCD display to reflect the changes made
        text = "T:" + str(output) + units + " "
        textLCD.writeText(LCDFont.FONT_5x8, 6, 0, text)
        textLCD.flush()     # This is important!

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        total_time_rotator.setOnAttachHandler(totalTimeRotatorAttached)
        total_time_rotator.setOnDetachHandler(totalTimeRotatorDetached)
        total_time_rotator.setOnErrorHandler(interfaceKitError)
        total_time_rotator.setOnVoltageChangeHandler(totalTimeRotatorVoltageChange)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End total time rotator functions

#####################################################################################################################################

### Start video length rotator functions

    # Standard phidget attach handler for video_length_rotator
    def videoLengthRotatorAttached(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = video_length_rotator.getDeviceSerialNumber()
            channelClass = video_length_rotator.getChannelClassName()
            channel = video_length_rotator.getChannel()

            deviceClass = video_length_rotator.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = video_length_rotator.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # Standard phidget detach handler for video_length_rotator
    def videoLengthRotatorDetached(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = video_length_rotator.getDeviceSerialNumber()
            channelClass = video_length_rotator.getChannelClassName()
            channel = video_length_rotator.getChannel()

            deviceClass = video_length_rotator.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = video_length_rotator.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # This is the phidget handler for the length of video
    # This function is responsive, but does not affect anything when
    # the system is set to capture stills
    def videoLengthRotatorVoltageChange(interfaceKit, voltage):
        # Call to local function to get video length
        output = getVideoLength()

        # Update the display with the new value
        text = "L:" + str(output) + "m "
        textLCD.writeText(LCDFont.FONT_5x8, 12, 0, text)
        textLCD.flush()     # The display doesn't update without this

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        video_length_rotator.setOnAttachHandler(videoLengthRotatorAttached)
        video_length_rotator.setOnDetachHandler(videoLengthRotatorDetached)
        video_length_rotator.setOnErrorHandler(interfaceKitError)
        video_length_rotator.setOnVoltageChangeHandler(videoLengthRotatorVoltageChange)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End video length rotator functions

#####################################################################################################################################

### Start video delay rotator functions

    # Standard phidget attach handler for video_delay_rotator
    def videoDelayRotatorAttached(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = video_delay_rotator.getDeviceSerialNumber()
            channelClass = video_delay_rotator.getChannelClassName()
            channel = video_delay_rotator.getChannel()

            deviceClass = video_delay_rotator.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = video_delay_rotator.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # Standard phidget detach handler for video_delay_rotator
    def videoDelayRotatorDetached(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = video_delay_rotator.getDeviceSerialNumber()
            channelClass = video_delay_rotator.getChannelClassName()
            channel = video_delay_rotator.getChannel()

            deviceClass = video_delay_rotator.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = video_delay_rotator.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # This is the phidget handler for the length of video
    # This function is responsive, but does not affect anything when
    # the system is set to capture stills
    def videoDelayRotatorVoltageChange(interfaceKit, voltage):
        # Call to local function to get video length
        output = getVideoDelayStr()

        # Update the display with the new value
        text = "D:" + str(output)
        textLCD.writeText(LCDFont.FONT_5x8, 13, 1, text)
        textLCD.flush()     # The display doesn't update without this

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        video_delay_rotator.setOnAttachHandler(videoDelayRotatorAttached)
        video_delay_rotator.setOnDetachHandler(videoDelayRotatorDetached)
        video_delay_rotator.setOnErrorHandler(interfaceKitError)
        video_delay_rotator.setOnVoltageChangeHandler(videoDelayRotatorVoltageChange)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End video delay rotator functions

#####################################################################################################################################

### Start light sensor functions

    # Standard phidget attach handler for the light sensor
    def lightSensorAttached(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = light_sensor.getDeviceSerialNumber()
            channelClass = light_sensor.getChannelClassName()
            channel = light_sensor.getChannel()

            deviceClass = light_sensor.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = light_sensor.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # Standard phidget detach handler for the light sensor
    def lightSensorDetached(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = light_sensor.getDeviceSerialNumber()
            channelClass = light_sensor.getChannelClassName()
            channel = light_sensor.getChannel()

            deviceClass = light_sensor.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = light_sensor.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # This function gets called every time the value the light sensor
    # detects changes. It doesn't do much right now
    def lightSensorChanged(interfaceKit, voltage):
        exponent = (0.02470) * (voltage * 200) + (-0.5727)
        lux = pow(math.e, exponent)
        # print("Lux = " + str(lux))

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        light_sensor.setOnAttachHandler(lightSensorAttached)
        light_sensor.setOnDetachHandler(lightSensorDetached)
        light_sensor.setOnErrorHandler(interfaceKitError)
        light_sensor.setOnVoltageChangeHandler(lightSensorChanged)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End light sensor functions

#####################################################################################################################################

### Start shutter speed functions

    # Standard phidget attach handler for the shutter speed
    def shutterSpeedAttached(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = shutter_speed.getDeviceSerialNumber()
            channelClass = shutter_speed.getChannelClassName()
            channel = shutter_speed.getChannel()

            deviceClass = shutter_speed.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = shutter_speed.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget detach handler for the shutter speed rotator
    def shutterSpeedDetached(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = shutter_speed.getDeviceSerialNumber()
            channelClass = shutter_speed.getChannelClassName()
            channel = shutter_speed.getChannel()

            deviceClass = shutter_speed.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = shutter_speed.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # This function gets called every time the shutter speed rotator is moved
    def shutterSpeedChanged(interfaceKit, voltage):
        # Call to local function to get shutter speed
        output = getShutterSpeed()

        output = "{:6s}".format(output)

        # Update the output!
        text = str(output)
        textLCD.writeText(LCDFont.FONT_5x8, 0, 1, text)
        textLCD.flush()     # You must know how important this is by now

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        shutter_speed.setOnAttachHandler(shutterSpeedAttached)
        shutter_speed.setOnDetachHandler(shutterSpeedDetached)
        shutter_speed.setOnErrorHandler(interfaceKitError)
        shutter_speed.setOnVoltageChangeHandler(shutterSpeedChanged)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End shutter speed functions

#####################################################################################################################################

### Start ISO functions

    # Standard phidget attach handler for the iso rotator
    def isoAttached(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = iso.getDeviceSerialNumber()
            channelClass = iso.getChannelClassName()
            channel = iso.getChannel()

            deviceClass = iso.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = iso.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # Standard phidget detach handler for the iso rotator
    def isoDetached(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = iso.getDeviceSerialNumber()
            channelClass = iso.getChannelClassName()
            channel = iso.getChannel()

            deviceClass = iso.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = iso.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # This function gets called every time the iso rotator is moved
    def isoChanged(interfaceKit, voltage):
        # Call to local function to get iso
        output = getIso()

        output = "{:5s}".format(output)

        # Update the display
        text = str(output)
        textLCD.writeText(LCDFont.FONT_5x8, 7, 1, text)
        textLCD.flush()     # Make sure the new text appears

    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        iso.setOnAttachHandler(isoAttached)
        iso.setOnDetachHandler(isoDetached)
        iso.setOnErrorHandler(interfaceKitError)
        iso.setOnVoltageChangeHandler(isoChanged)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

### End ISO Functions

#####################################################################################################################################

### Start run button functions

    # Run button attach handler
    def runButtonAttachHandler(e):

        ph = run_button
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Run button detach handler
    def runButtonDetachHandler(e):

        ph = run_button

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Run button error handler
    def runButtonErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    # Run button state change handler
    # This gets called every time the run button's state changes
    def runButtonStateChangeHandler(self, state):
        if(state == 1):
            # Run the appropriate function
            if (mode_toggle.getState() == 0):
                runCapture()
            elif (mode_toggle.getState() == 1):
                runRecord()

    try:
        run_button.setOnAttachHandler(runButtonAttachHandler)
        run_button.setOnDetachHandler(runButtonDetachHandler)
        run_button.setOnErrorHandler(runButtonErrorHandler)
        run_button.setOnStateChangeHandler(runButtonStateChangeHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        run_button.setDeviceSerialNumber(120683)
        run_button.setChannel(0)
        run_button.open()
        print('Wait for run button, port 0 attach...')
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Run Button Open Failed")

### End run button functions

#####################################################################################################################################

### Start kill button functions

    # Kill button attach handler
    def killButtonAttachHandler(e):

        ph = kill_button
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return


    # Kill button detach handler
    def killButtonDetachHandler(e):

        ph = kill_button

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Kill button error handler
    def killButtonErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")


    # Kill button state handler
    # This gets called every time the kill button is pressed
    def killButtonStateChangeHandler(self, state):
        if(state == 1):
            # If pressed, properly shut down all running processes
            killAll()

    try:
        kill_button.setOnAttachHandler(killButtonAttachHandler)
        kill_button.setOnDetachHandler(killButtonDetachHandler)
        kill_button.setOnErrorHandler(killButtonErrorHandler)
        kill_button.setOnStateChangeHandler(killButtonStateChangeHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        kill_button.setDeviceSerialNumber(120683)
        kill_button.setChannel(1)
        kill_button.open()
        print('Wait for kill button, port 1 attach...')
        kill_button.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Kill Button Open Failed")

### End kill button functions

#####################################################################################################################################

### Error handler for all the toggles


    # Toggle error handler, shared by all toggles
    def toggleErrorHandler(button, errorCode, errorString):
        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

#####################################################################################################################################

### Start mode toggle functions

    # mode_toggle attach handler
    def modeToggleAttachHandler(e):

        ph = mode_toggle
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # mode_toggle detach handler
    def modeToggleDetachHandler(e):

        ph = mode_toggle

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # State change handler for mode_toggle
    def modeToggleStateChangeHandler(self, state):
        # Toggle 1 decides if the system will record video or capture stills
        text = str(state)
        if (state == 0):
            text = "C"
        elif (state == 1):
            text = "R"
        textLCD.writeText(LCDFont.FONT_5x8, 19, 0, text)
        textLCD.flush()

    # Attach the handlers to the mode toggle, catch and return any errors
    try:
        mode_toggle.setOnAttachHandler(modeToggleAttachHandler)
        mode_toggle.setOnDetachHandler(modeToggleDetachHandler)
        mode_toggle.setOnErrorHandler(toggleErrorHandler)
        mode_toggle.setOnStateChangeHandler(modeToggleStateChangeHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Mode toggle")
        print("Exiting....")
        exit(1)

    try:
        mode_toggle.setDeviceSerialNumber(120683)
        mode_toggle.setChannel(2)
        mode_toggle.open()
        print('Wait for mode toggle, port 2 attach...')
        mode_toggle.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Mode Toggle Open Failed")

### End mode toggle functions

#####################################################################################################################################

### Start interval unit toggle functions

    # interval_unit_toggle attach handler
    def intervalUnitToggleAttachHandler(e):

        ph = interval_unit_toggle
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # interval_unit_toggle detach handler
    def intervalUnitToggleDetachHandler(e):

        ph = interval_unit_toggle

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # interval_unit_toggle state handler
    def intervalUnitToggleStateChangeHandler(self, state):
        # This doesn't do anything, but you need it so the program
        # doesn't get upset and throw errors
        text = str(state)
        # textLCD.writeText(LCDFont.FONT_5x8, 16, 1, text)
        # textLCD.flush()

    try:
        interval_unit_toggle.setOnAttachHandler(intervalUnitToggleAttachHandler)
        interval_unit_toggle.setOnDetachHandler(intervalUnitToggleDetachHandler)
        interval_unit_toggle.setOnErrorHandler(toggleErrorHandler)
        interval_unit_toggle.setOnStateChangeHandler(intervalUnitToggleStateChangeHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        interval_unit_toggle.setDeviceSerialNumber(120683)
        interval_unit_toggle.setChannel(3)
        interval_unit_toggle.open()
        print('Wait for interval unit toggle, port 3 attach...')
        interval_unit_toggle.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Interval Unit Open Failed")

### End interval unit toggle functions

#####################################################################################################################################

### Start total time until toggle functions

    # total_time_unit_toggle attach handler
    def totalTimeUnitToggleAttachHandler(e):

        ph = total_time_unit_toggle
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # total_time_unit_toggle detach handler
    def totalTimeUnitToggleDetachHandler(e):

        ph = total_time_unit_toggle

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # total_time_unit_toggle state handler
    def totalTimeUnitToggleStateChangeHandler(self, state):
        # This doesn't do anything either, but the system
        # gets upset without it
        text = str(state)
        # textLCD.writeText(LCDFont.FONT_5x8, 19, 1, text)
        # textLCD.flush()

    try:
        total_time_unit_toggle.setOnAttachHandler(totalTimeUnitToggleAttachHandler)
        total_time_unit_toggle.setOnDetachHandler(totalTimeUnitToggleDetachHandler)
        total_time_unit_toggle.setOnErrorHandler(toggleErrorHandler)
        total_time_unit_toggle.setOnStateChangeHandler(totalTimeUnitToggleStateChangeHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        total_time_unit_toggle.setDeviceSerialNumber(120683)
        total_time_unit_toggle.setChannel(4)
        total_time_unit_toggle.open()
        print('Wait for total time unit toggle, port 4 attach...')
        total_time_unit_toggle.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Total Time Unit Open Failed")

### End total time unit toggle functions

#####################################################################################################################################

### Start relay functions

    # Standard phidget attach handler for the relay
    def relayAttachHandler(e):

        ph = relay
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget detach handler for the relay
    def relayDetachHandler(e):

        ph = relay

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard error handler for the relay
    def relayErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    # Change handler for the relay
    def relayStateChangeHandler(self, state):
        # Output the state in two locations to indicate that things are working
        if(state == 1):
            print('relay')

        text = str(state)
        textLCD.writeText(LCDFont.FONT_5x8, 13, 1, text)
        textLCD.flush()

    try:
        relay.setOnAttachHandler(relayAttachHandler)
        relay.setOnDetachHandler(relayDetachHandler)
        relay.setOnErrorHandler(relayErrorHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        relay.setDeviceSerialNumber(120683)
        relay.setChannel(0)
        relay.open()
        print('Wait for relay, port 0 attach...')
        relay.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Relay Open Failed")

### End relay functions

#####################################################################################################################################

### Start GPS functions

#    # Standard Phidget attach handler for the gps

#    def gpsAttachHandler(self):

#        ph = gps
#        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

#            print("\nAttach Event:")

#            """
#            * Get device information and display it.
#            """
#            channelClassName = ph.getChannelClassName()
#            serialNumber = ph.getDeviceSerialNumber()
#            channel = ph.getChannel()
#            if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
#                hubPort = ph.getHubPort()
#                print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
#                    "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
#            else:
#                print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
#                        "\n\t-> Channel:  " + str(channel) + "\n")

#        except PhidgetException as e:
#            print("\nError in Attach Event:")
#            #DisplayError(e)
#            traceback.print_exc()
#            return

#    # Standard phidget detach handler for the gps
#    def gpsDetachHandler(self):
#
#        ph = gps
#        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

#            print("\nDetach Event:")

#            """
#            * Get device information and display it.
#            """
#            serialNumber = ph.getDeviceSerialNumber()
#            channelClass = ph.getChannelClassName()
#            channel = ph.getChannel()

#            deviceClass = ph.getDeviceClass()
#            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
#                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
#                      "\n\t-> Channel:  " + str(channel) + "\n")
#            else:
#                hubPort = ph.getHubPort()
#                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
#                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
#
#        except PhidgetException as e:
#            print("\nError in Detach Event:")
#            #DisplayError(e)
#            traceback.print_exc()
#            return

#    # Standard phidget error handler for the gps
#    def gpsErrorHandler(self, errorCode, errorString):
#
#        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")
#
#    # Change handler for the gps
#    def gpsPositionChangeHandler(self, latitude, longitude, altitude):

        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
#        # Print the current coordinates to the terminal
#        print("\n[Position Event] -> Latitude:  %7.3f\n", latitude)
#        print("                 -> Longitude: %7.3f\n", longitude)
#        print("                 -> Altitude:  %7.3f\n", altitude)

#    # Attach everything to the gps
#    try:
#        gps.setDeviceSerialNumber(120683)
#        gps.setChannel(0)      # THIS IS WRONG as far as I know, it needs a different channel
#        gps.setOnAttachHandler(gpsAttachHandler)
#        gps.setOnDetachHandler(gpsDetachHandler)
#        gps.setOnErrorHandler(gpsErrorHandler)
#        print('Wait for GPS attach...')
#        gps.openWaitForAttachment(5000)
#    except PhidgetException as e:
#        print("Phidget Exception %i: %s" % (e.code, e.details))
#        print("Exiting....")
#        exit(1)

### End GPS functions

#####################################################################################################################################

### Start total time until toggle functions

    # total_time_unit_toggle attach handler
    def LCDOnOffToggleAttachHandler(e):

        ph = LCD_on_off_toggle
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # LCD_on_off_toggle detach handler
    def LCDOnOffToggleDetachHandler(e):

        ph = LCD_on_off_toggle

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # LCD_on_off_toggle state handler
    def LCDOnOffToggleStateChangeHandler(self, state):

        if state == 0:
            textLCD.setBacklight(0)
        elif state == 1:
            textLCD.setBacklight(1)
        print(state)
        textLCD.setBacklight(1.0)
        # textLCD.writeText(LCDFont.FONT_5x8, 19, 1, text)
        # textLCD.flush()

    try:
        LCD_on_off_toggle.setOnAttachHandler(LCDOnOffToggleAttachHandler)
        LCD_on_off_toggle.setOnDetachHandler(LCDOnOffToggleDetachHandler)
        LCD_on_off_toggle.setOnErrorHandler(toggleErrorHandler)
        LCD_on_off_toggle.setOnStateChangeHandler(LCDOnOffToggleStateChangeHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        LCD_on_off_toggle.setDeviceSerialNumber(120683)
        LCD_on_off_toggle.setChannel(5)
        LCD_on_off_toggle.open()
        print('Wait for LCD on/off button, port 5 attach...')
        LCD_on_off_toggle.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Total Time Unit Open Failed")

### End total time unit toggle functions

#####################################################################################################################################

    # User-define function to capture stills
    def runCapture():
        print("Capture")

        # Get the current date and time and format it
        now = datetime.datetime.now()
        dir_name = now.strftime("%Y%m%d_%Hh%Mm%Ss")

        # Try opening a directory with the name created above
        # If the directory can't be opened, create a directory
        # with that name and navigate to it
        try:
            os.chdir(str(dir_name))
        except:
            make_dir = subprocess.Popen(["mkdir", str(dir_name)])
            make_dir.wait()
            os.chdir(str(dir_name))

        # Create a log file, write to it, then close it
        filename = str(dir_name) + "_log.txt"
        error_file = open(filename, "w+")
        error_file.write("Start of Error logs from " + str(dir_name))
        error_file.close()

        # Re-open the log file in append mode
        log_file = open(filename, "a+")

        # Get the interval between photos and
        # the total time the system should run for
        # from their respective rotators
        interval = int(interval_rotator.getSensorValue() * 10)
        total_time = int(total_time_rotator.getSensorValue() * 10)

        # Determine if the interval is in seconds or minutes
        # by getting the value from the correct toggle
        if (interval_unit_toggle.getState() == 1):
            # Convert the interval to minutes
            interval = interval * 60
        elif (interval_unit_toggle.getState() == 0 and interval < 4):
            # The smallest interval possible is 4 seconds
            interval = 4

        # Determine if the total time the program runs is in minutes or hours
        if (total_time_unit_toggle.getState() == 1):
            # Convert the time to hours
            total_time = total_time * 3600
        elif (total_time_unit_toggle.getState() == 0):
            # Conver the time to minutes
            total_time = total_time * 60

        # Call to local function to return the shutter speed
        shutterSpeedValue = getShutterSpeed()

        # Call to local function to get iso
        isoValue = getIso()

        # Call to local funtion to locate the cameras
        # and update their settings
        camera_ports = locateAndUpdateCameras(shutterSpeedValue, isoValue)


        # These are for use in the while loops below
        number_of_cameras = len(camera_ports)
        number_of_photos = str(math.ceil(int(total_time)/int(interval)))

        i = 0       # counts how many cameras we've activated
        x = 0       # counts how many pictures we've taken

        # Inform the user to wait while we adjust the settings
        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'WAIT')
        textLCD.flush()

        camera_ports.sort(reverse = True)   # sorted so they capture in the correct order

        try:
            # So long as we haven't taken the desired number of photos,
            # keep running this loop and taking photos
            while x < int(number_of_photos):
                # Update the display to indicate progress
                status = str(x + 1) + '/' + str(number_of_photos) + '   '
                textLCD.writeText(LCDFont.FONT_5x8, 13, 1, status)
                textLCD.flush()

                # Open the capture program for each camera
                while i < number_of_cameras:
                    process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/capture.py", str(x), str(i)])
                    i = i + 1

                # Trigger the relay so all cameras capture at the same time
                relay.setDutyCycle(1.0)
                # Pause so the relay doesn't get confused
                sleep(int(interval))
                relay.setDutyCycle(0.0)


                # Try editing and renaming the .pts file
                try:
                    subprocess.call(["sed", "'s/00000" + str(x), "/00000" + str(x+1), "/g'", "00000" + str(x) + "-A.pts", ">", "00000" + str(x+1) + "-A.pts"])
                except:
                    print("Error in renaming .pts file")

                # Update the current video, if it exists
                # video_stitch(x, "/home/ryan/" + str(dir_name), log_file)

                # Update the counters
                x = x + 1
                i = 0
        except Error as e:
            print("oops")
            log_file.write(str(e))

        # Close the log file
        error_file.close()
        # Navigate to the previous directory to prevent nested directories
        os.chdir("../")


    # User-defined function for recording
    def runRecord():
        print('record')

        # Get the total time the program should run for
        # and the interval between videos from the appropriate rotators
        total_time = int(total_time_rotator.getSensorValue() * 10)
        interval = int(interval_rotator.getSensorValue() * 10)

        # Call to local function to get shutter speed value
        shutterSpeedValue = getShutterSpeed()

        # Call to local function to get iso value
        isoValue = getIso()

        # Call to local function to get video length
        video_length = getVideoLength()
        video_length = video_length * 60        # convert to minutes

        # Call to local function to get video delay
        video_delay = getVideoDelayInt()

        sleep(video_delay)

        textLCD.writeText(LCDFont.FONT_5x8, 13, 1, "     ")
        textLCD.flush()     # The display doesn't update without this

        # Determine if the interval is in seconds or minutes
        if (interval_unit_toggle.getState() == 1):
            interval = interval * 60    # convert to minutes

        # Determine if the total time is in minutes or hours
        if (total_time_unit_toggle.getState() == 1):
            total_time = total_time * 3600  # convert to hours
        elif (total_time_unit_toggle.getState() == 0):
            total_time = total_time * 60    # convert to minutes

        # Determine the total number of videos to take
        number_of_videos = int(math.ceil(total_time / interval))

        # Call to local function to locate and update
        # the cameras and their settings
        camera_ports = locateAndUpdateCameras(shutterSpeedValue, isoValue)

        # Inform the user that the system is running
        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'ON  ')
            # the extra space after "ON" is to erase the lingering
            # characters from "WAIT"
        textLCD.flush()

        # Open record2.py, which does the rest of the recording from there
        subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/record2.py", str(video_length), str(number_of_videos), str(interval)])

    # User-defined function to end all proces        text = str(state)ses with the click of a button
    def killAll():
        print('Kill all processes')

        # Try to close everything by setting all their handlers to None
        # and the closing them. Catch and return any errors that occur
        try:
            closeAllPhidgets()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        # This closes the terminal window that the program was running in,
        # it should essentially emulate pressing CTRL-C
        process = subprocess.Popen(['ls'])
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)


    textLCD.setBacklight(1)     # Give it some light! (also very important)


    # Set the serial number and channel for each phidget, then open it
    # and wait for 5 seconds for it to attach before returning an error
    # So far, I haven't been able to move this code to somewhere more sensible
    try:
        interval_rotator.setDeviceSerialNumber(120683)
        interval_rotator.setChannel(0)
        interval_rotator.open()
        print('Wait for interval rotator, port 0 attach...')
        interval_rotator.openWaitForAttachment(5000)
        sleep(1)
        total_time_rotator.setDeviceSerialNumber(120683)
        total_time_rotator.setChannel(2)
        total_time_rotator.open()
        print('Wait for total time rotator, port 2 attach...')
        total_time_rotator.openWaitForAttachment(5000)
        sleep(1)
        video_length_rotator.setDeviceSerialNumber(120683)
        video_length_rotator.setChannel(5)
        video_length_rotator.open()
        print('Wait for video length rotator, port 5 attach...')
        video_length_rotator.openWaitForAttachment(5000)
        sleep(1)
        video_delay_rotator.setDeviceSerialNumber(120683)
        video_delay_rotator.setChannel(1)
        video_delay_rotator.open()
        print('Wait for video delay rotator, port 5 attach...')
        video_delay_rotator.openWaitForAttachment(5000)
        sleep(1)
        shutter_speed.setDeviceSerialNumber(120683)
        shutter_speed.setChannel(4)
        shutter_speed.open()
        print('Wait for shutter speed, port 4 attach...')
        shutter_speed.openWaitForAttachment(5000)
        sleep(1)
        iso.setDeviceSerialNumber(120683)
        iso.setChannel(3)
        iso.open()
        print('Wait for iso, port 3 attach...')
        iso.openWaitForAttachment(5000)
        light_sensor.setDeviceSerialNumber(120683)
        light_sensor.setChannel(6)
        light_sensor.open()
        print('Wait for light sensor, port 6 attach...')
        light_sensor.openWaitForAttachment(5000)
        sleep(1)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    sleep(10)

    # From the initial phidget library
    print("Press Enter to quit....")
    # print(str(gps.getLongitude()))

    char = sys.stdin.read(1)

    print("Closing...")

    # Release everything! Close all the active phidgets, return an
    # error if one is found
    try:
        closeAllPhidgets()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Done.")
    exit(0)     # close the program


main()
