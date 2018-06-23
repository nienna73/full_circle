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
import random
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.Stepper import Stepper
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Phidget import PhidgetID
from Phidgets.Devices.TextLCD import TextLCD, TextLCD_ScreenSize

#Create a stepper object
try:
    stepper = Stepper()
    stepper2 = Stepper()
    stepper3 = Stepper()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

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

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (stepper.isAttached(), stepper.getDeviceName(), stepper.getSerialNum(), stepper.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Motors: %i" % (stepper.getMotorCount()))

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

#Information Display Function
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
def StepperAttached(e):
    attached = e.device
    print("Stepper %i Attached!" % (attached.getSerialNum()))

def StepperDetached(e):
    detached = e.device
    print("Stepper %i Detached!" % (detached.getSerialNum()))

def StepperError(e):
    try:
        source = e.device
        print("Stepper %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def StepperCurrentChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Current Draw: %6f" % (source.getSerialNum(), e.index, e.current))

def StepperInputChanged(e):
    source = e.device
    print("Stepper %i: Input %i -- State: %s" % (source.getSerialNum(), e.index, e.state))

def StepperPositionChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Position: %f" % (source.getSerialNum(), e.index, e.position))

def StepperVelocityChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))

#Event Handler Callback Functions
def inferfaceKitAttached(e):
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
    source = e.device
    print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

def interfaceKitSensorChanged(e):
    source = e.device
    print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))

def interfaceKitOutputChanged(e):
    sleep(1)
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))
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



#Main Program Code for IFkit
try:
    interfaceKit.setOnAttachHandler(inferfaceKitAttached)
    interfaceKit.setOnDetachHandler(interfaceKitDetached)
    interfaceKit.setOnErrorhandler(interfaceKitError)
    #interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
    #interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
    #interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    interfaceKit.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    interfaceKit.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
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

#### new code for LCD
#Main Program Code
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
    textLCD.setDisplayString(0, "benhuah")
    sleep(2)
    
    print("Writing to second row....")
    textLCD.setDisplayString(1, "what")
    
    
    
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


#Main Program Code for STEPPERS
try:
    stepper.setOnAttachHandler(StepperAttached)
    stepper.setOnDetachHandler(StepperDetached)
    stepper.setOnErrorhandler(StepperError)
    stepper2.setOnAttachHandler(StepperAttached)
    stepper2.setOnDetachHandler(StepperDetached)
    stepper2.setOnErrorhandler(StepperError)
    stepper3.setOnAttachHandler(StepperAttached)
    stepper3.setOnDetachHandler(StepperDetached)
    stepper3.setOnErrorhandler(StepperError)
    stepper.setOnCurrentChangeHandler(StepperCurrentChanged)
    stepper.setOnInputChangeHandler(StepperInputChanged)
    stepper.setOnPositionChangeHandler(StepperPositionChanged)
    stepper.setOnVelocityChangeHandler(StepperVelocityChanged)
    stepper2.setOnCurrentChangeHandler(StepperCurrentChanged)
    stepper2.setOnInputChangeHandler(StepperInputChanged)
    stepper2.setOnPositionChangeHandler(StepperPositionChanged)
    stepper2.setOnVelocityChangeHandler(StepperVelocityChanged)
    stepper3.setOnCurrentChangeHandler(StepperCurrentChanged)
    stepper3.setOnInputChangeHandler(StepperInputChanged)
    stepper3.setOnPositionChangeHandler(StepperPositionChanged)
    stepper3.setOnVelocityChangeHandler(StepperVelocityChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    stepper.openPhidget(92734) ###
    stepper2.openPhidget(267116)
    stepper3.openPhidget(270358)
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    stepper.waitForAttach(10000)
    stepper2.waitForAttach(10000)
    stepper3.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        stepper.closePhidget()
        stepper2.closePhidget()
        stepper2.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    print("Set the current position as start position...")
    stepper.setCurrentPosition(0, 0)
    stepper2.setCurrentPosition(0, 0)
    stepper2.setCurrentPosition(0, 0)
    #stepper.setCurrentPosition(0, interfaceKit.getSensorValue(0))
    #stepper2.setCurrentPosition(0, interfaceKit.getSensorValue(1))
    #stepper2.setCurrentPosition(0, interfaceKit.getSensorValue(2))
    sleep(1)
    
    print("Set the motor as engaged...")
    stepper.setEngaged(0, True)
    stepper2.setEngaged(0, True)
    stepper3.setEngaged(0, True)
    sleep(1)
    
    print("The motor will run until it reaches the set goal position...")
    
    stepper.setAcceleration(0, 4000)
    stepper.setVelocityLimit(0, 500)
    stepper.setCurrentLimit(0, 1.50)
    stepper2.setAcceleration(0, 4000)
    stepper2.setVelocityLimit(0, 500)
    stepper2.setCurrentLimit(0, 1.50)
    stepper3.setAcceleration(0, 4000)
    stepper3.setVelocityLimit(0, 500)
    stepper3.setCurrentLimit(0, 1.50)
    sleep(2)
    

###code for IFkit + LCD joystick


    """
    print("Will now move to position 5000...")
    stepper.setTargetPosition(0, 5000)
    stepper2.setTargetPosition(0, 5000)
    stepper3.setTargetPosition(0, 5000)
    while stepper.getCurrentPosition(0) != 5000:
        pass
    while stepper2.getCurrentPosition(0) != 5000:
        pass
    while stepper3.getCurrentPosition(0) != 5000:
        pass
    
    sleep(2)
    
    print("Will now move back to positon 0...")
    stepper.setTargetPosition(0, 0)
    stepper2.setTargetPosition(0, 0)
    stepper3.setTargetPosition(0, 0)
    while stepper.getCurrentPosition(0) != 0:
        pass
    while stepper2.getCurrentPosition(0) != 0:
        pass
    while stepper3.getCurrentPosition(0) != 0:
        pass
    
    """
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

textLCD.setBacklight(1)

for i in range (99999999):
    
	slider1=str(interfaceKit.getSensorValue(0))
	joystick_x=str(interfaceKit.getSensorValue(1))
	joystick_y=str(interfaceKit.getSensorValue(2))
	speed=str(interfaceKit.getSensorValue(3))
	
	print("Joystick X: %s Joystick Y: %s Slider Z: %s Speed: %s" % (joystick_x, joystick_y, slider1, speed))
	
	stepper.setVelocityLimit(0, (interfaceKit.getSensorValue(3) * 8 ))
	stepper2.setVelocityLimit(0, (interfaceKit.getSensorValue(3) * 8 ))
	stepper2.setVelocityLimit(0, (interfaceKit.getSensorValue(3) * 8 ))
	
	stepper.setTargetPosition(0, (interfaceKit.getSensorValue(0) * 8 ))
	stepper2.setTargetPosition(0, (interfaceKit.getSensorValue(1) * 4 ))
	stepper3.setTargetPosition(0, (interfaceKit.getSensorValue(2) * 4 ))

	line1="Motor Velocity: "+speed
	textLCD.setDisplayString(0, line1)
	line2="x: "+joystick_x+" "+"y: "+joystick_y+" z: "+slider1
	textLCD.setDisplayString(1,line2 )
	sleep(0.1)

# slider 0 - 500 -1000
# x 42 - 479 - 971
# y 1 -455	- 980
	
	
	#textLCD.setDisplayString(0, "%s%s") % (joystick_x, joystick_y)  
	

### end new code code


print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKit.closePhidget()
    stepper.setEngaged(0, False)
    stepper2.setEngaged(0, False)
    stepper2.setEngaged(0, False)
    sleep(1)
    stepper.closePhidget()
    stepper2.closePhidget()
    stepper2.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)