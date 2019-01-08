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


def main():

    # Create objects for toggles, sensors, rotators, and sliders on the rig
    try:
        interval_rotator = VoltageInput()
        total_time_rotator = VoltageInput()
        video_length_rotator = VoltageInput()
        shutterSpeed = VoltageInput()
        iso = VoltageInput()
        lightSensor = VoltageInput()
        runButton = DigitalInput()
        killButton = DigitalInput()
        toggle1 = DigitalInput()
        toggle2 = DigitalInput()
        toggle3 = DigitalInput()
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


    # Rotation Sensor Funtions
    # Standard phidget attach handler for interval_rotator
    def inferfaceKitAttached1(e):
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

    # Standard phidget attach handler for total_time_rotator
    def inferfaceKitAttached2(e):
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

    # Standard phidget attach handler for video_length_rotator
    def inferfaceKitAttached3(e):
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

    # Standard phidget attach handler for the light sensor
    def lightSensorAttached(e):
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

    # Standard phidget attach handler for the shutter speed
    def shutterSpeedAttached(e):
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

    # Standard phidget attach handler for the iso slider
    def isoAttached(e):
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

    # Standard phidget detach handler for rotator 1
    def interfaceKitDetached1(e):

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

    # Standard phidget detach handler for total_time_rotator
    def interfaceKitDetached2(e):

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

    # Standard phidget detach handler for video_length_rotator
    def interfaceKitDetached3(e):

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

    # Standard phidget detach handler for the light sensor
    def lightSensorDetached(e):

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

    # Standard phidget detach handler for the shutter speed slider
    def shutterSpeedDetached(e):

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

    # Standard phidget detach handler for the iso slider
    def isoDetached(e):

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

    # Standard interface kit error handler
    # Shared by all the interface kits
    def interfaceKitError(e):
        try:
            source = e.device
            print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

    # Voltage change handler for toggle2
    def interfaceKitVoltageChange1(interfaceKit, voltage):
        # This is the handler for the interval variable

        output = int(voltage*10)
        # If the toggle is off, the units are in seconds
        if (toggle2.getState() == 0):
            units = 's'
        # If the toggle is on, the units are in minutes
        elif (toggle2.getState() == 1):
            units = 'm'

        # This quickest we can take photos is 4 seconds apart
        # due to download speeds
        if (toggle2.getState() == 0 and output < 4):
            output = 4

        # Update the LCD display to reflect the changes made
        text = "I:" + str(output) + units + " "
        textLCD.writeText(LCDFont.FONT_5x8, 0, 0, text)
        textLCD.flush()     # Don't forget this!

    # This is the handler for when the total time rotator is changed
    def interfaceKitVoltageChange2(interfaceKit, voltage):
        # This affects the total time the program runs for,
        # whether that's for video or stills

        output = int(voltage*10)
        # If the toggle is off, the units are in minutes
        if (toggle3.getState() == 0):
            units = 'm'
        # If the toggle is on, the units are in hours
        elif (toggle3.getState() == 1):
            units = 'h'

        # Update the LCD display to reflect the changes made
        text = "T:" + str(output) + units + " "
        textLCD.writeText(LCDFont.FONT_5x8, 6, 0, text)
        textLCD.flush()     # This is important!

    # This is the phidget handler for the length of video
    # This function is responsive, but does not affect anything when
    # the system is set to capture stills
    def interfaceKitVoltageChange3(interfaceKit, voltage):
        volt = int(voltage*10)  # easier to handle larger numbers

        # This lovely if-else chunk decides how long the video will be
        # in minutes, with the smallest chunk available being 1 minute
        # and the largest being 29 minutes 'cause that's the max record length
        if (volt <= 4.9):
            output = 1
        elif (4.9 < volt <= 9.8):
            output = 2
        elif (9.8 < volt <= 14.7):
            output = 3
        elif (14.7 < volt <= 19.6):
            output = 4
        elif (19.6 < volt <= 24.5):
            output = 5
        elif (24.5 < volt <= 29.4):
            output = 10
        elif (29.4 < volt <= 34.3):
            output = 15
        elif (34.3 < volt <= 39.2):
            output = 20
        elif (39.2 < volt <= 44.1):
            output = 25
        elif (44.1 < volt):
            output = 29

        # Update the display with the new value
        text = "L:" + str(output) + "m "
        textLCD.writeText(LCDFont.FONT_5x8, 12, 0, text)
        textLCD.flush()     # The display doesn't update without this

    # This function gets called every time the value the light sensor
    # detects changes. It doesn't do much right now
    def lightSensorChanged(interfaceKit, voltage):
        exponent = (0.02470) * (voltage * 200) + (-0.5727)
        lux = pow(math.e, exponent)
        # print("Lux = " + str(lux))

    # This function gets called every time the shutter speed slider is moved
    def shutterSpeedChanged(interfaceKit, voltage):
        output = voltage    # just in case there's an unaccounted-for edge case

        # This section decides the shutter speed of the cameras based
        # on the position of the shutter speed slider. These values were
        # selected from a list provided by Ryan, and the intervals were decided
        # with math. The extra spaces in "output" are there to ensure no
        # trailing characters remain on the display when the value changes
        if (voltage <= 0.357):
            output = "10    "
        elif (0.357 < voltage <= 0.714):
            output = "4     "
        elif (0.714 < voltage <= 1.071):
            output = "2     "
        elif (1.071 < voltage <= 1.428):
            output = "1     "
        elif (1.428 < voltage <= 1.785):
            output = "1/30  "
        elif (1.785 < voltage <= 2.142):
            output = "1/50  "
        elif (2.142 < voltage <= 2.499):
            output = "1/100 "
        elif (2.499 < voltage <= 2.856):
            output = "1/250 "
        elif (2.856 < voltage <= 3.213):
            output = "1/400 "
        elif (3.213 < voltage <= 3.57):
            output = "1/500 "
        elif (3.57 < voltage <= 3.927):
            output = "1/800 "
        elif (3.927 < voltage <= 4.284):
            output = "1/1000"
        elif (4.284 < voltage <= 4.641):
            output = "1/1600"
        elif (4.641 < voltage):
            output = "1/2000"

        # Update the output!
        text = str(output)
        textLCD.writeText(LCDFont.FONT_5x8, 0, 1, text)
        textLCD.flush()     # You must know how important this is by now

    # This function gets called every time the iso slider is moved
    def isoChanged(interfaceKit, voltage):
        output = voltage

        # This is very similar to the shutter speed function above
        if (voltage <= 0.714):
            output = "100   "
        elif (0.714 < voltage <= 1.428):
            output = "800   "
        elif (0.1428 < voltage <= 2.142):
            output = "1600  "
        elif (2.142 < voltage <= 2.856):
            output = "3200  "
        elif (2.856 < voltage <= 3.57):
            output = "6400  "
        elif (3.57 < voltage <= 4.284):
            output = "12800 "
        elif (4.2824 < voltage):
            output = "25600 "

        # Update the display
        text = str(output)
        textLCD.writeText(LCDFont.FONT_5x8, 7, 1, text)
        textLCD.flush()     # Make sure the new text appears

    ### new code for LCD

    #Event Handler Callback Functions
    # Standard phidget LCD attach handler
    def TextLCDAttached(e):
        attached = e.device
        print("TextLCD %i Attached!" % (attached.getSerialNum()))

    # Standard phidget LCD detach handler
    def TextLCDDetached(e):
        detached = e.device
        print("TextLCD %i Detached!" % (detached.getSerialNum()))

    # Standard phidget LCD error handler
    def TextLCDError(e):
        try:
            source = e.device
            print("TextLCD %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

    #Digital Input functions
    # Run button attach handler
    def runButtonAttachHandler(e):

        ph = runButton
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

    # Kill button attach handler
    def killButtonAttachHandler(e):

        ph = killButton
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

    # Toggle1 attach handler
    def toggle1AttachHandler(e):

        ph = toggle1
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

    # Toggle 2 attach handler
    def toggle2AttachHandler(e):

        ph = toggle2
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

    # Toggle 3 attach handler
    def toggle3AttachHandler(e):

        ph = toggle3
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

        ph = runButton

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

    # Kill button detach handler
    def killButtonDetachHandler(e):

        ph = killButton

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

    # Toggle 1 detach handler
    def toggle1DetachHandler(e):

        ph = toggle1

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

    # Toggle 2 detach handler
    def toggle2DetachHandler(e):

        ph = toggle2

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

    # Toggle 3 detach handler
    def toggle3DetachHandler(e):

        ph = toggle3

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

    # Kill button error handler
    def killButtonErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    # Toggle error handler, shared by all toggles
    def toggleErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    # Run button state change handler
    # This gets called every time the run button's state changes
    def runButtonStateChangeHandler(self, state):
        if(state == 1):
            # Run the appropriate function
            if (toggle1.getState() == 0):
                runCapture()
            elif (toggle1.getState() == 1):
                runRecord()

    # Kill button state handler
    # This gets called every time the kill button is pressed
    def killButtonStateChangeHandler(self, state):
        if(state == 1):
            # If pressed, properly shut down all running processes
            killAll()


    # State change handler for toggle 1
    def toggle1StateChangeHandler(self, state):
        # Toggle 1 decides if the system will record video or capture stills
        text = str(state)
        if (state == 0):
            text = "CAP"
        elif (state == 1):
            text = "REC"
        textLCD.writeText(LCDFont.FONT_5x8, 19, 0, text)
        textLCD.flush()

    # Toggle 2 state handler
    def toggle2StateChangeHandler(self, state):
        # This doesn't do anything, but you need it so the program
        # doesn't get upset and throw errors
        text = str(state)
        # textLCD.writeText(LCDFont.FONT_5x8, 16, 1, text)
        # textLCD.flush()

    # Toggle 3 state handler
    def toggle3StateChangeHandler(self, state):
        # This doesn't do anything either, but the system
        # gets upset without it
        text = str(state)
        # textLCD.writeText(LCDFont.FONT_5x8, 19, 1, text)
        # textLCD.flush()

    # User-define function to capture stills
    def runCapture():
        print("Run")

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

        # Get the interval between photos and
        # the total time the system should run for
        # from their respective rotators
        interval = int(interval_rotator.getSensorValue() * 10)
        total_time = int(total_time_rotator.getSensorValue() * 10)

        # Determine if the interval is in seconds or minutes
        # by getting the value from the correct toggle
        if (toggle2.getState() == 1):
            # Convert the interval to minutes
            interval = interval * 60
        elif (toggle2.getState() == 0 and interval < 4):
            # The smallest interval possible is 4 seconds
            interval = 4

        # Determine if the total time the program runs is in minutes or hours
        if (toggle3.getState() == 1):
            # Convert the time to hours
            total_time = total_time * 3600
        elif (toggle3.getState() == 0):
            # Conver the time to minutes
            total_time = total_time * 60

        # Get the shutter speed from the shutter speed slider
        # and do the necessary math to get the proper shutter speed value
        shutterSpeedVoltage = shutterSpeed.getSensorValue()
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

        # Get the iso value from the iso slider
        # and do math to get the proper iso value
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

        camera_ports = []       # this will store all relevant camera ports

        # Detect all connected cameras and split the output
        ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
        ports_strings_split = ports_strings.split()

        # Decode the output and find all entries with the format "usb:xxx,xxx"
        # then add those entries to the list of camera ports
        for item in ports_strings_split:
            item = item.decode('utf-8')
            if item[0] == 'u':
                camera_ports.append(item)

        # These are for use in the while loops below
        number_of_cameras = len(camera_ports)
        number_of_photos = str(math.ceil(int(total_time)/int(interval)))

        i = 0       # counts how many cameras we've activated
        x = 0       # counts how many pictures we've taken

        # Inform the user to wait while we adjust the settings
        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'WAIT')
        textLCD.flush()

        camera_ports.sort(reverse = True)   # sorted so they capture in the correct order

        # Update the shutter speed and iso of each camera, one at a time
        for port in camera_ports:
            print(port)
            subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + shutterSpeedValue, "--set-config-value", "iso=" + isoValue])

        # So long as we haven't taken the desired number of photos,
        # keep running this loop and taking photos
        while x < int(number_of_photos):
            # Update the display to indicate progress
            status = str(x + 1) + '/' + str(number_of_photos) + '   '
            textLCD.writeText(LCDFont.FONT_5x8, 13, 1, status)
            textLCD.flush()

            # Open the capture program for each camera
            while i < number_of_cameras:
                process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/capture.py", str(x), str(i)])
                processes.append(process)
                i = i + 1

            # Trigger the relay so all cameras capture at the same time
            relay.setDutyCycle(1.0)
            # Pause so the relay doesn't get confused
            sleep(int(interval))
            relay.setDutyCycle(0.0)

            # Update the counters
            x = x + 1
            i = 0

        # Naviagte to the previous directory to prevent nested directories
        os.chdir("../")

    # User-defined function for recording
    def runRecord():
        print('record')

        # Get the video length, total time the program should run for,
        # and the interval between videos from the appropriate rotators
        video_length = int(video_length_rotator.getSensorValue() * 10) * 60
        total_time = int(total_time_rotator.getSensorValue() * 10)

        interval = int(interval_rotator.getSensorValue() * 10)

        # Get the shutter speed and convert it from voltage to shutter speed
        shutterSpeedVoltage = shutterSpeed.getSensorValue()
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

        # Get the iso and convert it from voltage to iso
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

        # Get the total length the program should run for and convert it from
        # voltage to an integer
        rawLength = video_length_rotator.getSensorValue() * 10
        if (rawLength <= 4.9):
            video_length = 1
        elif (4.9 < rawLength <= 9.8):
            video_length = 2
        elif (9.8 < rawLength <= 14.7):
            video_length = 3
        elif (14.7 < rawLength <= 19.6):
            video_length = 4
        elif (19.6 < rawLength <= 24.5):
            video_length = 5
        elif (24.5 < rawLength <= 29.4):
            video_length = 10
        elif (29.4 < rawLength <= 34.3):
            video_length = 15
        elif (34.3 < rawLength <= 39.2):
            video_length = 20
        elif (39.2 < rawLength <= 44.1):
            video_length = 25
        elif (44.1 < rawLength):
            video_length = 29

        video_length = video_length * 60    # convert the video length to minutes

        # Determine if the interval is in seconds or minutes
        if (toggle2.getState() == 1):
            interval = interval * 60    # convert to minutes

        # Determine if the total time is in minutes or hours
        if (toggle3.getState() == 1):
            total_time = total_time * 3600  # convert to hours
        elif (toggle3.getState() == 0):
            total_time = total_time * 60    # convert to minutes

        # Determine the total number of videos to take
        number_of_videos = int(math.ceil(total_time / interval))


        camera_ports = []       # all relevant camera ports

        # Detect all the cameras
        ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
        ports_strings_split = ports_strings.split()

        # Find all the ports of format "usb:xxx,xxx"
        for item in ports_strings_split:
            item = item.decode('utf-8')
            if item[0] == 'u':
                camera_ports.append(item)

        # Inform the user to wait while we update the settings
        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'WAIT')
        textLCD.flush()

        # Update the shutter speed and iso on each camera
        for port in camera_ports:
            print(port)
            subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + shutterSpeedValue, "--set-config-value", "iso=" + isoValue])

        # Inform the user that the system is running
        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'ON  ')
            # the extra space after "ON" is to erase the lingering
            # characters from "WAIT"
        textLCD.flush()

        # Open record2.py, which does the rest of the recording from there
        subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/record2.py", str(video_length), str(number_of_videos), str(interval)])

    # User-defined function to end all processes with the click of a button
    def killAll():
        print('Kill all processes')

        # Try to close everything by setting all their handlers to None
        # and the closing them. Catch and return any errors that occur
        try:
            interval_rotator.setOnVoltageChangeHandler(None)
            interval_rotator.setOnSensorChangeHandler(None)
            interval_rotator.close()
            total_time_rotator.setOnVoltageChangeHandler(None)
            total_time_rotator.setOnSensorChangeHandler(None)
            total_time_rotator.close()
            video_length_rotator.setOnVoltageChangeHandler(None)
            video_length_rotator.setOnSensorChangeHandler(None)
            video_length_rotator.close()
            shutterSpeed.setOnVoltageChangeHandler(None)
            shutterSpeed.setOnSensorChangeHandler(None)
            shutterSpeed.close()
            iso.setOnVoltageChangeHandler(None)
            iso.setOnSensorChangeHandler(None)
            iso.close()
            lightSensor.setOnVoltageChangeHandler(None)
            lightSensor.setOnSensorChangeHandler(None)
            lightSensor.close()
            runButton.setOnStateChangeHandler(None)
            runButton.close()
            killButton.setOnStateChangeHandler(None)
            killButton.close()
            toggle1.setOnStateChangeHandler(None)
            toggle1.close()
            toggle2.setOnStateChangeHandler(None)
            toggle2.close()
            toggle3.setOnStateChangeHandler(None)
            toggle3.close()
            textLCD.close()
            relay.close()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        # This closes the terminal window that the program was running in,
        # it should essentially emulate pressing CTRL-C
        process = subprocess.Popen(['ls'])
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

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

    #Main Program Code for IFkit
    # Attach all the handlers to the proper phidgets,
    # catch and return any errors
    try:
        interval_rotator.setOnAttachHandler(inferfaceKitAttached1)
        interval_rotator.setOnDetachHandler(interfaceKitDetached1)
        interval_rotator.setOnErrorHandler(interfaceKitError)
        interval_rotator.setOnVoltageChangeHandler(interfaceKitVoltageChange1)
        total_time_rotator.setOnAttachHandler(inferfaceKitAttached2)
        total_time_rotator.setOnDetachHandler(interfaceKitDetached2)
        total_time_rotator.setOnErrorHandler(interfaceKitError)
        total_time_rotator.setOnVoltageChangeHandler(interfaceKitVoltageChange2)
        video_length_rotator.setOnAttachHandler(inferfaceKitAttached3)
        video_length_rotator.setOnDetachHandler(interfaceKitDetached3)
        video_length_rotator.setOnErrorHandler(interfaceKitError)
        video_length_rotator.setOnVoltageChangeHandler(interfaceKitVoltageChange3)
        shutterSpeed.setOnAttachHandler(shutterSpeedAttached)
        shutterSpeed.setOnDetachHandler(shutterSpeedDetached)
        shutterSpeed.setOnErrorHandler(interfaceKitError)
        shutterSpeed.setOnVoltageChangeHandler(shutterSpeedChanged)
        iso.setOnAttachHandler(isoAttached)
        iso.setOnDetachHandler(isoDetached)
        iso.setOnErrorHandler(interfaceKitError)
        iso.setOnVoltageChangeHandler(isoChanged)
        lightSensor.setOnAttachHandler(lightSensorAttached)
        lightSensor.setOnDetachHandler(lightSensorDetached)
        lightSensor.setOnErrorHandler(interfaceKitError)
        lightSensor.setOnVoltageChangeHandler(lightSensorChanged)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    #Setup for digital input
    # More of what's above, attaching handlers to phidgets
    try:
        runButton.setOnAttachHandler(runButtonAttachHandler)
        runButton.setOnDetachHandler(runButtonDetachHandler)
        runButton.setOnErrorHandler(runButtonErrorHandler)
        runButton.setOnStateChangeHandler(runButtonStateChangeHandler)
        killButton.setOnAttachHandler(killButtonAttachHandler)
        killButton.setOnDetachHandler(killButtonDetachHandler)
        killButton.setOnErrorHandler(killButtonErrorHandler)
        killButton.setOnStateChangeHandler(killButtonStateChangeHandler)
        toggle1.setOnAttachHandler(toggle1AttachHandler)
        toggle1.setOnDetachHandler(toggle1DetachHandler)
        toggle1.setOnErrorHandler(toggleErrorHandler)
        toggle1.setOnStateChangeHandler(toggle1StateChangeHandler)
        toggle2.setOnAttachHandler(toggle2AttachHandler)
        toggle2.setOnDetachHandler(toggle2DetachHandler)
        toggle2.setOnErrorHandler(toggleErrorHandler)
        toggle2.setOnStateChangeHandler(toggle2StateChangeHandler)
        toggle3.setOnAttachHandler(toggle3AttachHandler)
        toggle3.setOnDetachHandler(toggle3DetachHandler)
        toggle3.setOnErrorHandler(toggleErrorHandler)
        toggle3.setOnStateChangeHandler(toggle3StateChangeHandler)
        relay.setOnAttachHandler(relayAttachHandler)
        relay.setOnDetachHandler(relayDetachHandler)
        relay.setOnErrorHandler(relayErrorHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)


    #### new code for LCD
    #Main Program Code

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

    # Set the serial number and port for all phidgets, give them each
    # 5 seconds to be found before returning an error
    # The serial number for the 8/8/8, to which everything is attached,
    # is 120683. The channel mentioned for everything is either
    # a digital or analog port that it's plugged in to. If something else
    # gets plugged into that port, it will behave like the thing that's
    # supposed to be plugged into that port, or there will be an error
    try:
        runButton.setDeviceSerialNumber(120683)
        runButton.setChannel(0)
        runButton.open()
        print('Wait for button 0 attach...')
        runButton.openWaitForAttachment(5000)
        killButton.setDeviceSerialNumber(120683)
        killButton.setChannel(1)
        killButton.open()
        print('Wait for button 1 attach...')
        killButton.openWaitForAttachment(5000)
        toggle1.setDeviceSerialNumber(120683)
        toggle1.setChannel(2)
        toggle1.open()
        print('Wait for toggle 2 attach...')
        toggle1.openWaitForAttachment(5000)
        toggle2.setDeviceSerialNumber(120683)
        toggle2.setChannel(3)
        toggle2.open()
        print('Wait for toggle 3 attach...')
        toggle2.openWaitForAttachment(5000)
        toggle3.setDeviceSerialNumber(120683)
        toggle3.setChannel(4)
        toggle3.open()
        print('Wait for toggle 4 attach...')
        toggle3.openWaitForAttachment(5000)
        relay.setDeviceSerialNumber(120683)
        relay.setChannel(0)
        relay.open()
        print('Wait for relay attach...')
        relay.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Digital Input Open Failed")

    textLCD.setBacklight(1)     # Give it some light! (also very important)

    #### New code for GPS
    # Standard Phidget attach handler for the gps
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

    # Set the serial number and channel for each phidget, then open it
    # and wait for 5 seconds for it to attach before returning an error
    try:
        interval_rotator.setDeviceSerialNumber(120683)
        interval_rotator.setChannel(0)
        interval_rotator.open()
        print('Wait for rotator 0 attach...')
        interval_rotator.openWaitForAttachment(5000)
        sleep(1)
        total_time_rotator.setDeviceSerialNumber(120683)
        total_time_rotator.setChannel(2)
        total_time_rotator.open()
        print('Wait for rotator 2 attach...')
        total_time_rotator.openWaitForAttachment(5000)
        sleep(1)
        video_length_rotator.setDeviceSerialNumber(120683)
        video_length_rotator.setChannel(5)
        video_length_rotator.open()
        print('Wait for rotator 5 attach...')
        video_length_rotator.openWaitForAttachment(5000)
        sleep(1)
        shutterSpeed.setDeviceSerialNumber(120683)
        shutterSpeed.setChannel(4)
        shutterSpeed.open()
        print('Wait for shutter speed 4 attach...')
        shutterSpeed.openWaitForAttachment(5000)
        sleep(1)
        iso.setDeviceSerialNumber(120683)
        iso.setChannel(3)
        iso.open()
        print('Wait for iso 3 attach...')
        iso.openWaitForAttachment(5000)
        lightSensor.setDeviceSerialNumber(120683)
        lightSensor.setChannel(6)
        lightSensor.open()
        print('Wait for light sensor 6 attach...')
        lightSensor.openWaitForAttachment(5000)
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
        interval_rotator.setOnVoltageChangeHandler(None)
        interval_rotator.setOnSensorChangeHandler(None)
        interval_rotator.close()
        total_time_rotator.setOnVoltageChangeHandler(None)
        total_time_rotator.setOnSensorChangeHandler(None)
        total_time_rotator.close()
        video_length_rotator.setOnVoltageChangeHandler(None)
        video_length_rotator.setOnSensorChangeHandler(None)
        video_length_rotator.close()
        shutterSpeed.setOnVoltageChangeHandler(None)
        shutterSpeed.setOnSensorChangeHandler(None)
        shutterSpeed.close()
        iso.setOnVoltageChangeHandler(None)
        iso.setOnSensorChangeHandler(None)
        iso.close()
        lightSensor.setOnVoltageChangeHandler(None)
        lightSensor.setOnSensorChangeHandler(None)
        lightSensor.close()
        runButton.setOnStateChangeHandler(None)
        runButton.close()
        killButton.setOnStateChangeHandler(None)
        killButton.close()
        toggle1.setOnStateChangeHandler(None)
        toggle1.close()
        toggle2.setOnStateChangeHandler(None)
        toggle2.close()
        toggle3.setOnStateChangeHandler(None)
        toggle3.close()
        textLCD.close()
#        gps.close()
        relay.close()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Done.")
    exit(0)     # close the program

main()
