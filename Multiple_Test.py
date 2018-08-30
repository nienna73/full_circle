#!/usr/bin/env python

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
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageInput import *


def main():

    #Create an interfacekit object
    try:
        rotator1 = VoltageInput()
        rotator2 = VoltageInput()
        rotator3 = VoltageInput()
        runButton = DigitalInput()
        killButton = DigitalInput()
        relay = DigitalOutput()
    except RuntimeError as e:
        print("Runtime Exception: %s" % e.details)
        print("Exiting....")
        exit(1)

    #Create an TextLCD object
    try:
        textLCD = LCD()
    except RuntimeError as e:
        print("Runtime Exception: %s" % e.details)
        print("Exiting....")
        exit(1)


    # Rotation Sensor Funtions
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
            DisplayError(e)
            traceback.print_exc()
            return

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
            DisplayError(e)
            traceback.print_exc()
            return

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
            DisplayError(e)
            traceback.print_exc()
            return

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
            DisplayError(e)
            traceback.print_exc()
            return

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
            DisplayError(e)
            traceback.print_exc()
            return

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
            DisplayError(e)
            traceback.print_exc()
            return

    def interfaceKitError(e):
        try:
            source = e.device
            print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

    def interfaceKitVoltageChange1(interfaceKit, voltage):
        output = int(voltage*10)
        text = "Wait: " + str(output)
        textLCD.writeText(LCDFont.FONT_5x8, 0, 0, text)
        textLCD.flush()

    def interfaceKitVoltageChange2(interfaceKit, voltage):
        output = int(voltage*10)
        text = "Total: " + str(output)
        textLCD.writeText(LCDFont.FONT_5x8, 10, 0, text)
        textLCD.flush()

    def interfaceKitVoltageChange3(interfaceKit, voltage):
        output = int(voltage*10)
        text = "3: " + str(output)
        textLCD.writeText(LCDFont.FONT_5x8, 0, 1, text)
        textLCD.flush()

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
            DisplayError(e)
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
            DisplayError(e)
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
            DisplayError(e)
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
            DisplayError(e)
            traceback.print_exc()
            return

    def runButtonErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def killButtonErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def runButtonStateChangeHandler(self, state):
        if(state == 1):
            runCapture()

        text = str(state)
        textLCD.writeText(LCDFont.FONT_5x8, 10, 1, text)
        textLCD.flush()

    def killButtonStateChangeHandler(self, state):
        if(state == 1):
            killAll()

        text = str(state)
        textLCD.writeText(LCDFont.FONT_5x8, 13, 1, text)
        textLCD.flush()

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
        while x < int(number_of_photos):

            while i < number_of_cameras:
                process = subprocess.Popen(["python3", "../capture.py", str(x), str(i), number_of_photos, str(interval)])
                processes.append(process)
                i = i + 1

            x = x + 1
            relay.setDutyCycle(1.0)
            sleep(3)
            relay.setDutyCycle(0.0)
            sleep(int(interval) - 3)
            i = 0

    def killAll():
        print('Kill all processes')
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
            DisplayError(e)
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
            DisplayError(e)
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
        runButton.openWaitForAttachment(5000)
        killButton.setDeviceSerialNumber(120683)
        killButton.setChannel(1)
        killButton.open()
        killButton.openWaitForAttachment(5000)
        relay.setDeviceSerialNumber(120683)
        relay.setChannel(0)
        relay.open()
        relay.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Digital Input Open Failed")

    textLCD.setBacklight(1)

    try:
        rotator1.setDeviceSerialNumber(120683)
        rotator1.setChannel(0)
        rotator1.open()
        rotator1.openWaitForAttachment(5000)
        sleep(2)
        rotator2.setDeviceSerialNumber(120683)
        rotator2.setChannel(2)
        rotator2.open()
        rotator2.openWaitForAttachment(5000)
        sleep(2)
        rotator3.setDeviceSerialNumber(120683)
        rotator3.setChannel(5)
        rotator3.open()
        rotator3.openWaitForAttachment(5000)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    sleep(10)

    print("Press Enter to quit....")

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
        runButton.setOnStateChangeHandler(None)
        runButton.close()
        killButton.setOnStateChangeHandler(None)
        killButton.close()
        textLCD.close()
        relay.close()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Done.")
    exit(0)

main()
