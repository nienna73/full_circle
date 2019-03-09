#!/usr/bin/env python

# Killswitch Engage is meant to run on a Raspberry Pi in the field with a timelapse camera
# It uses a relay, which is wired to be always on.
# When this program is used, it opens the relay, waits 10 seconds, then closes the relay again
# effectively hard resetting the program.

# This file was created by Jolene Poulin on February 22, 2019
# for use by Full Circle Visuals Inc.


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
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *



def main():

    try:
        relay_left = DigitalOutput()
        relay_right = DigitalOutput()
    except RuntimeError as e:
        print("Runtime Exception: %s" % e.details)
        print("Exiting....")
        exit(1)

#####################################################################################################################################

### Start relay_left functions

    # Standard phidget attach handler for the relay
    def relayLeftAttachHandler(e):

        ph = relay_left

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
    def relayLeftDetachHandler(e):

        ph = relay_left

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
    def relayLeftStateChangeHandler(self, state):
        # Output the state in two locations to indicate that things are working
        if(state == 1):
            print('relay left')

        text = str(state)
        textLCD.writeText(LCDFont.FONT_5x8, 13, 1, text)
        textLCD.flush()

    try:
        relay_left.setOnAttachHandler(relayLeftAttachHandler)
        relay_left.setOnDetachHandler(relayLeftDetachHandler)
        relay_left.setOnErrorHandler(relayErrorHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        relay_left.setDeviceSerialNumber(271638)
        relay_left.setChannel(0)
        relay_left.open()
        print('Wait for relay left to attach...')
        relay_left.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Relay Open Failed")

### End relay_left functions

#####################################################################################################################################

### Start relay_right functions

    # Standard phidget attach handler for the relay
    def relayRightAttachHandler(e):

        ph = relay_right

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
    def relayRightDetachHandler(e):

        ph = relay_right

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


    # Change handler for the relay
    def relayRightStateChangeHandler(self, state):
        # Output the state in two locations to indicate that things are working
        if(state == 1):
            print('relay right')

        text = str(state)
        textLCD.writeText(LCDFont.FONT_5x8, 13, 1, text)
        textLCD.flush()

    try:
        relay_right.setOnAttachHandler(relayRightAttachHandler)
        relay_right.setOnDetachHandler(relayRightDetachHandler)
        relay_right.setOnErrorHandler(relayErrorHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        relay_right.setDeviceSerialNumber(271638)
        relay_right.setChannel(1)
        relay_right.open()
        print('Wait for relay right to attach...')
        relay_right.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Relay Open Failed")

### End relay_right functions

#####################################################################################################################################
    def kill_process():
        sleep(5)
        try:
            relay_left.setDutyCycle(0.0)
            print("relay off")
            #sleep(10)
            #relay_left.setDutyCycle(0.0)
            #print("relay off")

            #minCycle = relay_left.getMinDutyCycle()
            #print(minCycle + '\t')
            #maxCycle = relay_left.getMaxDutyCycle()
            #print(maxCycle)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            print(e)
            exit(1)
            return

    kill_process()

    # Release everything! Close all the active phidgets, return an
    # error if one is found
    try:
        relay.close()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Done.")
    exit(0)     # close the program


main()
