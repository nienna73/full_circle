#! /usr/env/python

import sys
import time
import traceback
import subprocess
import os
import datetime
import time

from Phidget22.Devices.VoltageInput import *


class PowerSource():
	def __init__(self, channel):
		self.volts = None
		self.device = VoltageInput()
		self.channel = channel
		
		"""
		* Add event handlers before calling open so that no events are missed.
		"""
		self.device.setOnAttachHandler(onAttachHandlerInput)
		self.device.setOnDetachHandler(onDetachHandlerInput)
		self.device.setOnErrorHandler(onErrorHandlerInput)
		self.device.setOnVoltageChangeHandler(onVoltageChangeHandlerInput)
		self.device.setOnSensorChangeHandler(onSensorChangeHandlerInput)

		
		try:
			self.device.setDeviceSerialNumber(271638)
			self.device.setChannel(self.channel)
			self.device.openWaitForAttachment(5000)
		except PhidgetException as e:
			print("Program Terminated: Open PowerSource Failed")
			print(e)

   	def onAttachHandler(self):

        	ph = self.device
        	try:
            		#If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            		#www.phidgets.com/docs/Using_Multiple_Phidgets for information

            		print("\nAttach Event:")

            		"""
            		* Get device information and display it.
            		"""
            		channelClassName = ph.getChannelClassName()
            		serialNumber = ph.getDeviceSerialNumber()
            		channel = ph.getChannel()
            
            		if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
                		hubPort = ph.getHubPort()
                		print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                			"\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
            		else:
                		print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                			"\n\t-> Channel:  " + str(channel) + "\n")

                	"""
                	* Set the DataInterval inside of the attach handler to initialize the device with this value.
                	* DataInterval defines the minimum time between VoltageChange events.
                	* DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
                	"""
                	print("\n\tSetting DataInterval to 1000ms")
                	ph.setDataInterval(1000)

                	"""
                	* Set the VoltageChangeTrigger inside of the attach handler to initialize the device with this value.
                	* VoltageChangeTrigger will affect the frequency of VoltageChange events, by limiting them to only occur when
                	* the voltage changes by at least the value set.
                	"""
                	print("\tSetting Voltage ChangeTrigger to 0.0")
                	ph.setVoltageChangeTrigger(0.0)

                	"""
                	* Set the SensorType inside of the attach handler to initialize the device with this value.
                	* You can find the appropriate SensorType for your sensor in its User Guide and the VoltageInput API
                	* SensorType will apply the appropriate calculations to the voltage reported by the device
                	* to convert it to the sensor's units.
                	* SensorType can only be set for Sensor Port voltage inputs (VINT Ports and Analog Input Ports)
                	"""
                	if(ph.getChannelSubclass() == ChannelSubclass.PHIDCHSUBCLASS_VOLTAGEINPUT_SENSOR_PORT):
                    		print("\tSetting Voltage SensorType")
                    		ph.setSensorType(VoltageSensorType.SENSOR_TYPE_VOLTAGE)

        	except PhidgetException as e:
            		print("\nError in Attach Event:")
    	    		traceback.print_exc()
	    	return

 
	def onDetachHandler(self):
		ph = self.device

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
                "\n\t-> Channel:  " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")

        except PhidgetException as e:
	    print("\nError in Detach Event:")
	    traceback.print_exc()
	    return

 
    def onErrorHandler(self, errorCode, errorString):
        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")


    def onSensorChangeHandler(self, sensorValue, sensorUnit):
        print("[Sensor Event] -> Sensor Value: " + str(sensorValue) + sensorUnit.symbol)


    def onVoltageChangeHandler(self, voltage):
        self.volts = (voltage - 2.5) / 0.0681
        


