#! /usr/env/python

import datetime
import time

from open_power_source import PowerSource

def log_status(filename):
	_input = PowerSource(0)
	output = PowerSource(1)
	battery = PowerSource(2)
	
	current_datetime = time.strftime("%Y%m%d_%Hh%Mm%Ss")
	
	battery_update_message = "Battery Voltage at " + str(current_datetime) + " is: " + str(battery.getVolts()) + "\n"
	log_file = open(filename, "a+")
	log_file.write(battery_update_message)
	battery.closeDevice()
	
	output_update_message = "Output Voltage at " + str(current_datetime) + " is: " + str(output.getVolts()) + "\n"
	log_file.write(output_update_message)
	output.closeDevice()
	
	_input_update_message = "Input Voltage at " + str(current_datetime) + " is: " + str(_input.getVolts()) + "\n\n"
	log_file.write(_input_update_message)
	_input.closeDevice()
	
	
	log_file.close()
	
	return
