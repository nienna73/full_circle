#! /usr/env/python

from open_power_source import PowerSource
import time

def check_volts():		

	_input = PowerSource(0)
	output = PowerSource(1)
	battery = PowerSource(2)
    
	time.sleep(5)
	
	stati = []

	if _input.getVolts() != None and _input.getVolts() < 12.0:
		stati.append(["input", str(_input.getVolts())])
	
	if output.getVolts() != None and output.getVolts() < 12.0:
		stati.append(["output", str(output.getVolts())])
	
	if battery.getVolts() != None and batter.getVolts() < 12.0:
		stati.append(["battery", str(battery.getVolts())])
	
	_input.closeDevice()
	output.closeDevice()
	battery.closeDevice()
	
	return stati
    
def report_volts():
	_input = PowerSource(0)
	output = PowerSource(1)
	battery = PowerSource(2)
    
	time.sleep(5)
	
	stati = []

	stati.append(["input", _input.getVolts()])
	stati.append(["output", output.getVolts()])
	stati.append(["battery", battery.getVolts()])
	
	_input.closeDevice()
	output.closeDevice()
	battery.closeDevice()
	
	return stati
    
