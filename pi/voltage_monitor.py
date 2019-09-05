#! /usr/env/python

from open_power_source import PowerSource
import time

def check_volts():		

	_input = PowerSource(0)
	output = PowerSource(1)
	battery = PowerSource(2)
    
	time.sleep(5)
	
	stati = []

	input_volts = ((_input.getVolts() if _input.getVolts() else 0) - 2.5) / 0.0681
	if _input.getVolts() != None and input_volts < 12.0:
		stati.append(["input", str(input_volts)])
		
	_input.closeDevice()
	
	output_volts = ((output.getVolts() if output.getVolts() else 0) - 2.5) / 0.0681
	if output.getVolts() != None and output_volts < 12.0:
		stati.append(["output", str(output_volts)])
		
	output.closeDevice()
	
	battery_volts = ((battery.getVolts() if battery.getVolts() else 0) - 2.5) / 0.0681
	if battery.getVolts() != None and battery_volts < 12.0:
		stati.append(["battery", str(battery_volts)])
	
	battery.closeDevice()
	
	return stati
    
def report_volts():
	_input = PowerSource(0)
	output = PowerSource(1)
	battery = PowerSource(2)
	
	_input.start()
	output.start()
	battery.start()
    
	time.sleep(5)
	
	stati = []
	
	input_volts = (_input.getVolts() - 2.5) / 0.0681
	_input.closeDevice()
	
	output_volts = (output.getVolts() - 2.5) / 0.0681
	output.closeDevice()
	
	battery_volts = (battery.getVolts() - 2.5) / 0.0681
	battery.closeDevice()

	stati.append(["input", str(input_volts)])
	stati.append(["output", str(output_volts)])
	stati.append(["battery", str(battery_volts)])

	
	return stati
