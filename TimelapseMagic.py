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
        rotator1 = VoltageInput()
        rotator2 = VoltageInput()
        rotator3 = VoltageInput()
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
    # Standard phidget attach handler for Rotator1
    def inferfaceKitAttached1(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = rotator1.getDeviceSerialNumber()
            channelClass = rotator1.getChannelClassName()
            channel = rotator1.getChannel()

            deviceClass = rotator1.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator1.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget attach handler for Rotator2
    def inferfaceKitAttached2(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = rotator2.getDeviceSerialNumber()
            channelClass = rotator2.getChannelClassName()
            channel = rotator2.getChannel()

            deviceClass = rotator2.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator2.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget attach handler for Rotator3
    def inferfaceKitAttached3(e):
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = rotator3.getDeviceSerialNumber()
            channelClass = rotator3.getChannelClassName()
            channel = rotator3.getChannel()

            deviceClass = rotator3.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator3.getHubPort()
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
            serialNumber = rotator3.getDeviceSerialNumber()
            channelClass = rotator3.getChannelClassName()
            channel = rotator3.getChannel()

            deviceClass = rotator3.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator3.getHubPort()
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
            serialNumber = rotator3.getDeviceSerialNumber()
            channelClass = rotator3.getChannelClassName()
            channel = rotator3.getChannel()

            deviceClass = rotator3.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator3.getHubPort()
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
            serialNumber = rotator3.getDeviceSerialNumber()
            channelClass = rotator3.getChannelClassName()
            channel = rotator3.getChannel()

            deviceClass = rotator3.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator3.getHubPort()
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
            serialNumber = rotator1.getDeviceSerialNumber()
            channelClass = rotator1.getChannelClassName()
            channel = rotator1.getChannel()

            deviceClass = rotator1.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator1.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget detach handler for rotator2
    def interfaceKitDetached2(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = rotator2.getDeviceSerialNumber()
            channelClass = rotator2.getChannelClassName()
            channel = rotator2.getChannel()

            deviceClass = rotator2.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator2.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            #DisplayError(e)
            traceback.print_exc()
            return

    # Standard phidget detach handler for rotator3
    def interfaceKitDetached3(e):

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = rotator3.getDeviceSerialNumber()
            channelClass = rotator3.getChannelClassName()
            channel = rotator3.getChannel()

            deviceClass = rotator3.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator3.getHubPort()
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
            serialNumber = rotator3.getDeviceSerialNumber()
            channelClass = rotator3.getChannelClassName()
            channel = rotator3.getChannel()

            deviceClass = rotator3.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator3.getHubPort()
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
            serialNumber = rotator3.getDeviceSerialNumber()
            channelClass = rotator3.getChannelClassName()
            channel = rotator3.getChannel()

            deviceClass = rotator3.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator3.getHubPort()
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
            serialNumber = rotator3.getDeviceSerialNumber()
            channelClass = rotator3.getChannelClassName()
            channel = rotator3.getChannel()

            deviceClass = rotator3.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = rotator3.getHubPort()
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
    def TextLCDAttached(e):
        attached = e.device
        print("TextLCD %i Attached!" % (attached.getSerialNum()))

    def TextLCDDetached(e):
        detached = e.device
        print("TextLCD %i Detached!" % (detached.getSerialNum()))

    def TextLCDError(e):
        try:
            source = e.device
            print("TextLCD %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

    #Digital Input functions
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

    def runButtonErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def killButtonErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def toggleErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def runButtonStateChangeHandler(self, state):
        if(state == 1):
            if (toggle1.getState() == 0):
                runCapture()
            elif (toggle1.getState() == 1):
                runRecord()

        text = str(state)
        # textLCD.writeText(LCDFont.FONT_5x8, 7, 1, text)
        # textLCD.flush()

    def killButtonStateChangeHandler(self, state):
        if(state == 1):
            killAll()

        text = str(state)
        # textLCD.writeText(LCDFont.FONT_5x8, 10, 1, text)
        # textLCD.flush()

    def toggle1StateChangeHandler(self, state):
        text = str(state)
        if (state == 0):
            text = "CAP"
        elif (state == 1):
            text = "REC"
        textLCD.writeText(LCDFont.FONT_5x8, 19, 0, text)
        textLCD.flush()

    def toggle2StateChangeHandler(self, state):
        text = str(state)
        # textLCD.writeText(LCDFont.FONT_5x8, 16, 1, text)
        # textLCD.flush()

    def toggle3StateChangeHandler(self, state):
        text = str(state)
        # textLCD.writeText(LCDFont.FONT_5x8, 19, 1, text)
        # textLCD.flush()

    def runCapture():
        print("Run")
        # relay.setDutyCycle(1.0)
        # sleep(1)
        # relay.setDutyCycle(0.0)

        now = datetime.datetime.now()
        dir_name = now.strftime("%Y%m%d_%Hh%Mm%Ss")

        try:
            os.chdir(str(dir_name))
        except:
            make_dir = subprocess.Popen(["mkdir", str(dir_name)])
            make_dir.wait()
            os.chdir(str(dir_name))

        interval = int(rotator1.getSensorValue() * 10)
        total_time = int(rotator2.getSensorValue() * 10)

        if (toggle2.getState() == 1):
            interval = interval * 60
        elif (toggle2.getState() == 0 and interval < 4):
            interval = 4

        if (toggle3.getState() == 1):
            total_time = total_time * 3600
        elif (toggle3.getState() == 0):
            total_time = total_time * 60

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

        camera_ports = []

        ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
        ports_strings_split = ports_strings.split()


        for item in ports_strings_split:
            item = item.decode('utf-8')
            if item[0] == 'u':
                camera_ports.append(item)

        number_of_cameras = len(camera_ports)

        number_of_photos = str(math.ceil(int(total_time)/int(interval)))

        processes = []
        i = 0
        x = 0

        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'PREP')
        textLCD.flush()
        camera_ports.sort(reverse = True)
        for port in camera_ports:
            print(port)
            subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + shutterSpeedValue, "--set-config-value", "iso=" + isoValue])

        files = []
        while x < int(number_of_photos):
            status = str(x + 1) + '/' + str(number_of_photos) + '   '
            textLCD.writeText(LCDFont.FONT_5x8, 13, 1, status)
            textLCD.flush()
            while i < number_of_cameras:
                process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/capture.py", str(x), str(i)])
                processes.append(process)
                i = i + 1

            x = x + 1
            relay.setDutyCycle(1.0)
            sleep(int(interval))
            relay.setDutyCycle(0.0)
            i = 0

        os.chdir("../")

    def runRecord():
        print('record')
        video_length = int(rotator3.getSensorValue() * 10) * 60
        total_time = int(rotator2.getSensorValue() * 10)

        interval = int(rotator1.getSensorValue() * 10)

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

        rawLength = rotator3.getSensorValue() * 10
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
            video_length = 29         # where 30 = 29.5 'cause the cameras can't record that long

        video_length = video_length * 60

        if (toggle2.getState() == 1):
            interval = interval * 60

        if (toggle3.getState() == 1):
            total_time = total_time * 3600
        elif (toggle3.getState() == 0):
            total_time = total_time * 60

        number_of_videos = int(math.ceil(total_time / interval))


        camera_ports = []

        ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
        ports_strings_split = ports_strings.split()


        for item in ports_strings_split:
            item = item.decode('utf-8')
            if item[0] == 'u':
                camera_ports.append(item)

        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'PREP')
        textLCD.flush()
        for port in camera_ports:
            print(port)
            subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + shutterSpeedValue, "--set-config-value", "iso=" + isoValue])

        textLCD.writeText(LCDFont.FONT_5x8, 15, 1, 'ON  ')
        textLCD.flush()
        subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/record2.py", str(video_length), str(number_of_videos), str(interval)])

    def killAll():
        print('Kill all processes')
        try:
            rotator1.setOnVoltageChangeHandler(None)
            rotator1.setOnSensorChangeHandler(None)
            rotator1.close()
            rotator2.setOnVoltageChangeHandler(None)
            rotator2.setOnSensorChangeHandler(None)
            rotator2.close()
            rotator3.setOnVoltageChangeHandler(None)
            rotator3.setOnSensorChangeHandler(None)
            rotator3.close()
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

        process = subprocess.Popen(['ls'])
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

    # Digital output functions
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

    def relayErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def relayStateChangeHandler(self, state):
        if(state == 1):
            print('relay')

        text = str(state)
        textLCD.writeText(LCDFont.FONT_5x8, 13, 1, text)
        textLCD.flush()

    #Main Program Code for IFkit
    try:
        rotator1.setOnAttachHandler(inferfaceKitAttached1)
        rotator1.setOnDetachHandler(interfaceKitDetached1)
        rotator1.setOnErrorHandler(interfaceKitError)
        rotator1.setOnVoltageChangeHandler(interfaceKitVoltageChange1)
        rotator2.setOnAttachHandler(inferfaceKitAttached2)
        rotator2.setOnDetachHandler(interfaceKitDetached2)
        rotator2.setOnErrorHandler(interfaceKitError)
        rotator2.setOnVoltageChangeHandler(interfaceKitVoltageChange2)
        rotator3.setOnAttachHandler(inferfaceKitAttached3)
        rotator3.setOnDetachHandler(interfaceKitDetached3)
        rotator3.setOnErrorHandler(interfaceKitError)
        rotator3.setOnVoltageChangeHandler(interfaceKitVoltageChange3)
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

    def LCDDetached(self):
        detached = self
        try:
            print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)

    def ErrorEvent(self, eCode, description):
        print("Error %i : %s" % (eCode, description))

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

    textLCD.setBacklight(1)

    #### New code for GPS
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

#    def gpsErrorHandler(self, errorCode, errorString):
#
#        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")
#
#    def gpsPositionChangeHandler(self, latitude, longitude, altitude):

        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information

#        print("\n[Position Event] -> Latitude:  %7.3f\n", latitude)
#        print("                 -> Longitude: %7.3f\n", longitude)
#        print("                 -> Altitude:  %7.3f\n", altitude)


#    try:
#        gps.setDeviceSerialNumber(131151)
#        gps.setChannel(0)
#        gps.setOnAttachHandler(gpsAttachHandler)
#        gps.setOnDetachHandler(gpsDetachHandler)
#        gps.setOnErrorHandler(gpsErrorHandler)
#        print('Wait for GPS attach...')
#        gps.openWaitForAttachment(5000)
#    except PhidgetException as e:
#        print("Phidget Exception %i: %s" % (e.code, e.details))
#        print("Exiting....")
#        exit(1)

    try:
        rotator1.setDeviceSerialNumber(120683)
        rotator1.setChannel(0)
        rotator1.open()
        print('Wait for rotator 0 attach...')
        rotator1.openWaitForAttachment(5000)
        sleep(1)
        rotator2.setDeviceSerialNumber(120683)
        rotator2.setChannel(2)
        rotator2.open()
        print('Wait for rotator 2 attach...')
        rotator2.openWaitForAttachment(5000)
        sleep(1)
        rotator3.setDeviceSerialNumber(120683)
        rotator3.setChannel(5)
        rotator3.open()
        print('Wait for rotator 5 attach...')
        rotator3.openWaitForAttachment(5000)
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

    print("Press Enter to quit....")
    # print(str(gps.getLongitude()))

    char = sys.stdin.read(1)

    print("Closing...")

    try:
        rotator1.setOnVoltageChangeHandler(None)
        rotator1.setOnSensorChangeHandler(None)
        rotator1.close()
        rotator2.setOnVoltageChangeHandler(None)
        rotator2.setOnSensorChangeHandler(None)
        rotator2.close()
        rotator3.setOnVoltageChangeHandler(None)
        rotator3.setOnSensorChangeHandler(None)
        rotator3.close()
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
    exit(0)

main()
