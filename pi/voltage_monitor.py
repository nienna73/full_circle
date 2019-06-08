#! /usr/env/python

import sys
import time
import traceback
import requests 	# For Slack integration
import subprocess
import os
import datetime
import time

from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

from get_battery_status import get_status
from open_relay import open_relay
from open_power_source import PowerSource

# Global variables, because everything breaks when they aren't global :/
output_has_notified_slack = False
input_has_notified_slack = False
battery_has_notified_slack = False
pi_has_under_90 = False
pi_has_under_50 = False
pi_has_under_10 = False
ticks = 0
log_file_name = str(time.strftime("%Y%m%d_%Hh%Mm%Ss")) + "_log.txt"


relay_left = open_relay(1)
relay_right = open_relay(0)

def kill_process():
    global relay_left, relay_right
    try:
	relay_left.setDutyCycle(1.0)
	print("relay on")
	sleep(10)
	relay_left.setDutyCycle(0.0)
	print("relay off")

	relay_right.setDutyCycle(1.0)
	print("relay on")
	sleep(10)
	relay_right.setDutyCycle(0.0)
	print("relay off")
    except PhidgetException as e:
	print("Phidget Exception %i: %s" % (e.code, e.details))
	print("Exiting....")
	print(e)
	exit(1)


def main():
    global relay_left, relay_right, log_file_name
    
    log_file = open(log_file_name, "a+")
    log_file.write("\nStart of session\n")
    log_file.close()
	
    # Check if it's a new day
    # Make a new logfile if it is
    def checkFileName(filename):
	global log_file_name
	name = filename[:8]
	new_date = str(time.strftime("%Y%m%d"))
	if new_date != name:
            print("Creating a new log file")
            log_file_name = str(time.strftime("%Y%m%d_%Hh%Mm%Ss")) + "_log.txt"
	    log_file = open(log_file_name, "a+")
	    log_file.write("\nStart of session\n")
	    log_file.close()
	
 
    """
    * Outputs the DigitalInput's most recently reported state.
    * Fired when a DigitalInput channel with onStateChangeHandler registered detects a state change
    *
    * @param self The DigitalInput channel that fired the StateChange event
    * @param state The reported state from the DigitalInput channel
    """
    def onVoltageChangeHandlerInput(self, voltage):
        #input
        global input_has_notified_slack
        global ticks
        global log_file_name
        volts = (voltage - 2.5) / 0.0681
        webhook = os.environ.get('VOLTAGE_MONITOR_WEBHOOK')
        string_volts = "%.2f" % volts

        if ticks % 60 == 0:
            current_datetime = time.strftime("%Y%m%d_%Hh%Mm%Ss")
            input_update_message = "Input Voltage at " + str(current_datetime) + " is: " + string_volts + "\n"
            log_file = open(log_file_name, "a+")
            log_file.write(input_update_message)
            log_file.close()

        if volts < 11.5 and (not input_has_notified_slack):
	    print("[Voltage Event] -> Input Voltage: " + string_volts)
	    input_has_notified_slack = True
	    print("posting to slack")
	    command = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"Help! The input voltage (input 0) has dropped to " + string_volts + "\"}' " + webhook
	    os.system(command)
	    current_datetime = time.strftime("%Y%m%d_%Hh%Mm%Ss")
	    input_log_message = "At " + str(current_datetime) + " the input voltage dropped to : " + string_volts + "\n"
	    log_file = open(log_file_name, "a+")
	    log_file.write(input_log_message)
	    log_file.close()
        elif volts > 11.5:
	    input_has_notified_slack = False

    def onVoltageChangeHandlerOutput(self, voltage):
        #output
        global output_has_notified_slack
        global ticks
        global log_file_name
        volts = (voltage - 2.5) / 0.0681
        webhook = os.environ.get('VOLTAGE_MONITOR_WEBHOOK')
        string_volts = "%.2f" % volts

        if ticks % 60 == 0:
            current_datetime = time.strftime("%Y%m%d_%Hh%Mm%Ss")
            output_update_message = "Output Voltage at " + str(current_datetime) + " is: " + string_volts + "\n"
            log_file = open(log_file_name, "a+")
            log_file.write(output_update_message)
            log_file.close()

        if volts < 11.5 and not output_has_notified_slack:
	    print("[Voltage Event] -> Output Voltage: " + string_volts)
	    output_has_notified_slack = True
	    print("posting to slack")
	    command = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"Help! The output voltage (input 2) has dropped to " + string_volts + "\"}' " + webhook
	    os.system(command)
	    current_datetime = time.strftime("%Y%m%d_%Hh%Mm%Ss")
	    output_log_message = "At " + str(current_datetime) + " the output voltage dropped to : " + string_volts + "\n"
	    log_file = open(log_file_name, "a+")
	    log_file.write(output_log_message)
	    log_file.close()
        elif volts > 11.5:
	    output_has_notified_slack = False

    def onVoltageChangeHandlerBattery(self, voltage):
        #battery
        global battery_has_notified_slack
        global ticks
        global log_file_name
        global pi_has_under_90, pi_has_under_50, pi_has_under_10
        volts = (voltage - 2.5) / 0.0681
        webhook = os.environ.get('VOLTAGE_MONITOR_WEBHOOK')
        string_volts = "%.2f" % volts

        if ticks % 60 == 0:
            current_datetime = time.strftime("%Y%m%d_%Hh%Mm%Ss")
            battery_update_message = "Battery Voltage at " + str(current_datetime) + " is: " + string_volts + "\n\n"
            log_file = open(log_file_name, "a+")
            log_file.write(battery_update_message)
            log_file.close()

        if volts < 11.5 and not battery_has_notified_slack:
            print("[Voltage Event] -> Battery Voltage: " + string_volts)
            battery_has_notified_slack = True
            print("posting to slack")
            command = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"Help! The battery voltage (input 1) has dropped to " + string_volts + "\"}' " + webhook
            os.system(command)
            current_datetime = time.strftime("%Y%m%d_%Hh%Mm%Ss")
            battery_log_message = "At " + str(current_datetime) + " the battery voltage dropped to : " + string_volts + "\n"
            log_file = open(log_file_name, "a+")
            log_file.write(battery_log_message)
            log_file.close()
        elif volts > 11.5:
            battery_has_notified_slack = False

        # Check the filename once every hour
        if ticks % 3600 == 0:
            checkFileName(log_file_name)

        # Check the Pi battery once every 5 minutes
        if ticks % 300 == 0:
            per = get_status()
            if per < 100 and per > 50 and not pi_has_under_90:
                pi_has_under_90 = True
                command = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"The Raspberry Pi has " + str(per) + "% battery remaining. \"}' " + webhook
                os.system(command)
            elif per < 50 and per > 10 and not pi_has_under_50:
                pi_has_under_50 = True
                command = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"The Raspberry Pi has " + str(per) + "% battery remaining. \"}' " + webhook
                os.system(command)
            elif per < 10 and not pi_has_under_10:
                pi_has_under_10 = True
                command = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"The Raspberry Pi has " + str(per) + "% battery remaining. It will die soon. \"}' " + webhook
                os.system(command)
            else:
                pi_has_under_10 = False
                pi_has_under_50 = False
                pi_has_under_90 = False

        ticks += 1

    try:
		
        """
        * Allocate a new Phidget Channel object
        """
        _input = PowerSource(0)

        output = PowerSource(1)
        
        battery = PowerSource(2)
        
    except PhidgetException as e:
	sys.stderr.write("\nExiting with error(s)...")
	print(e)
	traceback.print_exc()
	print("Cleaning up...")
	_input.close()
	output.close()
	battery.close()
	relay_right.close()
	relay_left.close()
	return 1
    except RuntimeError as e:
	sys.stderr.write("Runtime Error: \n\t" + e)
	traceback.print_exc()
	return 1
    finally:
        print("Press ENTER to end program.")
        readin = sys.stdin.readline()
		

if __name__ == "__main__":
    main()
    
    
else:
    pass
