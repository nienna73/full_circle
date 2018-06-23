#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack and Ryan Jackson and LUCAS TIMMONS'
__version__ = '2.1.8'
__date__ = 'November 14 2014'

#Basic imports
from ctypes import *
import sys
import random
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Phidget import PhidgetID #added
from Phidgets.Devices.TextLCD import TextLCD, TextLCD_ScreenSize #added for LCD
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS

#Create an interfacekit object
try:
    interfaceKit = InterfaceKit()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Create an TextLCD object
try:
    textLCD = TextLCD()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function   #IFkit8/8/8
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

#Information Display Function  #added LCD
def DisplayDeviceInfo():
    try:
        isAttached = textLCD.isAttached()
        name = textLCD.getDeviceName()
        serialNo = textLCD.getSerialNum()
        version = textLCD.getDeviceVersion()
        rowCount = textLCD.getRowCount()
        columnCount = textLCD.getColumnCount()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        return 1
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (isAttached, name, serialNo, version))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Rows: %i -- Number of Columns: %i" % (rowCount, columnCount))


#Event Handler Callback Functions
def interfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))

def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))

def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def interfaceKitInputChanged(e):
    source = e.index
    print(source)
    if source == 0:
    	textLCD.setDisplayString(0, "Button pushed")
    	#set interfaceKit_Relay output to 1
    	interfaceKit_Relay.setOnAttachHandler(interfaceKitAttached)
    	interfaceKit_Relay.setOutputState(0, 1)
    	sleep(1)
    	interfaceKit_Relay.setOutputState(0, 0)
    else:
    	print("Lucas is okay")
    #print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))
#Calculate by diving by 1000. Find the total number of steps for what you want. EG 120 steps is 8.333. Make sure when you divide 1000/8.333 that the result is less than the total number of steps. So 1000/8.333 is 120.000x you want it under 120, so increase the step to 8.334 and you're good.

def interfaceKitSensorChanged(e):
    source = e.device
    stepper = 8.334
    position = e.value/stepper
    advancedServo.setEngaged(0, True)
    advancedServo.setPosition(0, position)
    textLCD.setBacklight(1)
    newstringdata = round(position, 2)
    newstring = str(newstringdata)
    textLCD.setDisplayString(1, newstring)
    print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))

def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

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

try:
    interfaceKit_Relay = InterfaceKit()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Create an advancedServo object
try:
    advancedServo = AdvancedServo()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#stack to keep current values in
currentList = [0,0,0,0,0,0,0,0]
velocityList = [0,0,0,0,0,0,0,0]

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (advancedServo.isAttached(), advancedServo.getDeviceName(), advancedServo.getSerialNum(), advancedServo.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of motors: %i" % (advancedServo.getMotorCount()))

#Event Handler Callback Functions
def Attached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))

def Detached(e):
    detached = e.device
    print("Servo %i Detached!" % (detached.getSerialNum()))

def Error(e):
    try:
        source = e.device
        print("Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def CurrentChanged(e):
    global currentList
    currentList[e.index] = e.current

def PositionChanged(e):
    source = e.device
    print("AdvancedServo %i: Motor %i Position: %f - Velocity: %f - Current: %f" % (source.getSerialNum(), e.index, e.position, velocityList[e.index], currentList[e.index]))
    if advancedServo.getStopped(e.index) == True:
        print("Motor %i Stopped" % (e.index))

def VelocityChanged(e):
    global velocityList
    velocityList[e.index] = e.velocity

#Main Program Code

try:
    advancedServo.setOnAttachHandler(Attached)
    advancedServo.setOnDetachHandler(Detached)
    advancedServo.setOnErrorhandler(Error)
    advancedServo.setOnCurrentChangeHandler(CurrentChanged)
    advancedServo.setOnPositionChangeHandler(PositionChanged)
    advancedServo.setOnVelocityChangeHandler(VelocityChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    advancedServo.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    advancedServo.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        advancedServo.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    print("Setting the servo type for motor 0 to HITEC_HS322HD")
    advancedServo.setServoType(0, ServoTypes.PHIDGET_SERVO_HITEC_HS322HD)
    #Setting custom servo parameters example - 600us-2000us == 120 degrees, velocity max 1500
    #advancedServo.setServoParameters(0, 600, 2000, 120, 1500)
    print("Speed Ramping state: %s" % advancedServo.getSpeedRampingOn(0))
    print("Stopped state: %s" % advancedServo.getStopped(0))
    print("Engaged state: %s" % advancedServo.getEngaged(0))

    print("Working with motor 0 only...")

    #print("Adjust Acceleration to maximum: %f" % advancedServo.getAccelerationMax(0))
    #advancedServo.setAcceleration(0, advancedServo.getAccelerationMax(0))
    #sleep(2)

    #print("Adjust Velocity Limit to maximum: %f" % advancedServo.getVelocityMax(0))
    #advancedServo.setVelocityLimit(0, advancedServo.getVelocityMax(0))
    #sleep(2)

    #print("Engage the motor...")
    #advancedServo.setEngaged(0, True)
    #sleep(2)

    #print("Engaged state: %s" % advancedServo.getEngaged(0))

    #print("Move to position positionMin...")
    #advancedServo.setPosition(0, advancedServo.getPositionMin(0))
    #sleep(5)

    #print("Move to position PositionMax...")
    #advancedServo.setPosition(0, advancedServo.getPositionMax(0))
    #sleep(5)

    #print("Adjust Acceleration to 50...")
    #advancedServo.setAcceleration(0, 50.00)
    #sleep(2)

    #print("Adjust Velocity Limit to 50...")
    #advancedServo.setVelocityLimit(0, 50.00)
    #sleep(2)

    #print("Move to position PositionMin...")
    #advancedServo.setPosition(0, advancedServo.getPositionMin(0))
    #sleep(5)

    #print("Disengage the motor...")
    #advancedServo.setEngaged(0, False)
    #sleep(2)

    #print("Engaged state: %s" % advancedServo.getEngaged(0))

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        advancedServo.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKit.setOnAttachHandler(interfaceKitAttached)
    interfaceKit_Relay.setOnAttachHandler(interfaceKitAttached) #added
    interfaceKit.setOnDetachHandler(interfaceKitDetached)
    interfaceKit_Relay.setOnDetachHandler(interfaceKitDetached) #added
    interfaceKit.setOnErrorhandler(interfaceKitError)
    interfaceKit_Relay.setOnErrorhandler(interfaceKitError) #added
    interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)  #update info when an input changes
    interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
    interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    interfaceKit.openPhidget(120683)
    interfaceKit_Relay.openPhidget(352936) #added
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    interfaceKit.waitForAttach(10000)
    interfaceKit_Relay.waitForAttach(10000) #added
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget(120683)
       # interfaceKit_Relay.closePhidget(352936) #added
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Setting the data rate for each sensor index to 4ms....")
for i in range(interfaceKit.getSensorCount()):
    try:

        interfaceKit.setDataRate(i, 4)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

#end IFkit stuff

#### new code for LCD

try:
    textLCD.setOnAttachHandler(TextLCDAttached)
    textLCD.setOnDetachHandler(TextLCDDetached)
    textLCD.setOnErrorhandler(TextLCDError)


except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    textLCD.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    textLCD.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        textLCD.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    if textLCD.getDeviceID()==PhidgetID.PHIDID_TEXTLCD_ADAPTER:
        textLCD.setScreenIndex(0)
        textLCD.setScreenSize(TextLCD_ScreenSize.PHIDGET_TEXTLCD_SCREEN_2x8)

    print("Writing to first row....")
    #textLCD.setDisplayString(0, "benhuah")
    #sleep(2)

    print("Writing to second row....")
    #textLCD.setDisplayString(1, "what")



except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

try:

    sleep(2)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)
#end LCD stuff

#Create an accelerometer object
try:
    gps = GPS()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (gps.isAttached(), gps.getDeviceName(), gps.getSerialNum(), gps.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")

#Event Handler Callback Functions
def GPSAttached(e):
    attached = e.device
    print("GPS %i Attached!" % (attached.getSerialNum()))

def GPSDetached(e):
    detached = e.device
    print("GPS %i Detached!" % (detached.getSerialNum()))

def GPSError(e):
    try:
        source = e.device
        print("GPS %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def GPSPositionChanged(e):
    source = e.device
    print("GPS %i: Latitude: %F, Longitude: %F, Altitude: %F, Date: %s, Time: %s" % (source.getSerialNum(), e.latitude, e.longitude, e.altitude, source.getDate().toString(), source.getTime().toString()))

def GPSPositionFixStatusChanged(e):
    source = e.device
    if e.positionFixStatus:
        status = "FIXED"
    else:
        status = "NOT FIXED"
    print("GPS %i: Position Fix Status: %s" % (source.getSerialNum(), status))

#Main Program Code
try:
    gps.setOnAttachHandler(GPSAttached)
    gps.setOnDetachHandler(GPSDetached)
    gps.setOnErrorhandler(GPSError)
    gps.setOnPositionChangeHandler(GPSPositionChanged)
    gps.setOnPositionFixStatusChangeHandler(GPSPositionFixStatusChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    gps.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        gps.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Press Enter to quit....")

try:
    print("GPS Current Time: %s" %(gps.getTime().toString()))
    print("GPS Current Date: %s" %(gps.getDate().toString()))
    print("GPS Current Latitude: %F" %(gps.getLatitude()))
    print("GPS Current Longitude: %F" %(gps.getLongitude()))
    print("GPS Current Altitude: %F" %(gps.getAltitude()))
    print("GPS Current Heading: %F" %(gps.getHeading()))
    print("GPS Current Velocity: %F" % (gps.getVelocity()))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

chr = sys.stdin.read(1)

print("Closing...")

try:
    gps.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)


#
# Code to DO something will go here
#
print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKit.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
