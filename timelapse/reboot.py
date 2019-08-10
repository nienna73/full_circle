#! /usr/env/python

import sys
import time
import traceback
import subprocess
import os
import datetime
import time

from Phidget22.Devices.DigitalOutput import *
from Phidget22.Phidget import *


def open_relay(channel):
	relay = DigitalOutput()
	relay.setOnAttachHandler(relayAttachHandler)
	relay.setOnDetachHandler(relayDetachHandler)
	relay.setOnErrorHandler(relayErrorHandler)

	try:
		relay.setDeviceSerialNumber(352936)
		relay.setChannel(channel)
		print('Wait for relay to attach...')
		relay.openWaitForAttachment(5000)
	except PhidgetException as e:
		print("Program Terminated: Relay Open Failed")
		return

	return relay


def relayAttachHandler(self):
	ph = self

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
	    traceback.print_exc()
	return

    # Standard phidget detach handler for the relay
def relayDetachHandler(self):
	ph = self

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



def main():
    # create relays 0-5 using the open relay function above
    # set each of them to 'off'
    # wait 10 seconds
    # set each of them to 'on'

    relay_0 = open_relay(0)
    relay_0.setDutyCycle(1.0)

    relay_1 = open_relay(1)
    relay_1.setDutyCycle(1.0)

    relay_2 = open_relay(2)
    relay_2.setDutyCycle(1.0)

    relay_3 = open_relay(3)
    relay_3.setDutyCycle(1.0)

    relay_4 = open_relay(4)
    relay_4.setDutyCycle(1.0)

    relay_5 = open_relay(5)
    relay_5.setDutyCycle(1.0)

    time.sleep(10)

    relay_5.setDutyCycle(0.0)
    time.sleep(1)
    relay_4.setDutyCycle(0.0)
    time.sleep(1)
    relay_3.setDutyCycle(0.0)
    time.sleep(1)
    relay_2.setDutyCycle(0.0)
    time.sleep(1)
    relay_1.setDutyCycle(0.0)
    time.sleep(1)
    relay_0.setDutyCycle(0.0)



main()
