#! /usr/env/python

import sys
import time
import traceback
import subprocess
import os
import datetime
import time

from Phidget22.Devices.VoltageInput import *
from power_source_funcs import onAttachHandler, onDetachHandler, onSensorChangeHandler, onErrorHandler


class PowerSource():
	def __init__(self, channel):
		self.volts = None
		self.device = VoltageInput()
		self.channel = channel
		this = self
		
	def onVoltageChangeHandler(self, voltage):
		this.volts = (voltage - 2.5) / 0.0681

		"""
		* Add event handlers before calling open so that no events are missed.
		"""
		self.device.setOnAttachHandler(onAttachHandler)
		self.device.setOnDetachHandler(onDetachHandler)
		self.device.setOnErrorHandler(onErrorHandler)
		self.device.setOnVoltageChangeHandler(onVoltageChangeHandler)
		self.device.setOnSensorChangeHandler(onSensorChangeHandler)


		try:
			self.device.setDeviceSerialNumber(271638)
			self.device.setChannel(self.channel)
			self.device.openWaitForAttachment(5000)
		except PhidgetException as e:
			print("Program Terminated: Open PowerSource Failed")
			print(e)
			
	def getVolts(self):
		return self.volts
		
	def closeDevice(self):
		self.device.close()
