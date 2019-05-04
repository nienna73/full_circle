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

# Global variables, because everything breaks when they aren't global :/
output_has_notified_slack = False
input_has_notified_slack = False
battery_has_notified_slack = False
pi_has_under_90 = False
pi_has_under_50 = False
pi_has_under_10 = False
ticks = 0
log_file_name = str(time.strftime("%Y%m%d_%Hh%Mm%Ss")) + "_log.txt"


relay_left = DigitalOutput()
relay_right = DigitalOutput()

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
	
#####################################################################################################################################

### Start relay_left functions

    # Standard phidget attach handler for the relay
    def relayLeftAttachHandler(self):
        
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
	    #DisplayError(e)
	    traceback.print_exc()
	    return

    # Standard phidget detach handler for the relay
    def relayLeftDetachHandler(self):
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
	    #DisplayError(e)
	    traceback.print_exc()
	    return

    # Standard error handler for the relay
    def relayLeftErrorHandler(button, errorCode, errorString):
        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")
    
    # Change handler for the relay
    def relayLeftStateChangeHandler(self, state):
        # Output the state in two locations to indicate that things are working
        if(state == 1):
            print('relay left')


### End relay_left functions

#####################################################################################################################################

### Start relay_right functions

    # Standard phidget attach handler for the relay
    def relayRightAttachHandler(self):
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
	    #DisplayError(e)
	    traceback.print_exc()
	    return

    # Standard phidget detach handler for the relay
    def relayRightDetachHandler(self):
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
	    #DisplayError(e)
	    traceback.print_exc()
	    return

    # Standard error handler for the relay
    def relayRightErrorHandler(button, errorCode, errorString):
        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    # Change handler for the relay
    def relayRightStateChangeHandler(self, state):
        # Output the state in two locations to indicate that things are working
        if(state == 1):
            print('relay right')


### End relay_right functions

#####################################################################################################################################


    def onAttachHandlerInput(self):

        ph = self
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
            #DisplayError(e)
    	    traceback.print_exc()
	    return

    def onAttachHandlerOutput(self):

        ph = self
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
	    #DisplayError(e)
	    traceback.print_exc()
	    return

    def onAttachHandlerBattery(self):
        ph = self
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
	    #DisplayError(e)
	    traceback.print_exc()
	    return

    """
    * Displays info about the detached Phidget channel.
    * Fired when a Phidget channel with onDetachHandler registered detaches
    *
    * @param self The Phidget channel that fired the attach event
    """
    def onDetachHandlerInput(self):
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
                "\n\t-> Channel:  " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")

        except PhidgetException as e:
	    print("\nError in Detach Event:")
	    traceback.print_exc()
	    return

    def onDetachHandlerOutput(self):
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
                "\n\t-> Channel:  " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")

        except PhidgetException as e:
	    print("\nError in Detach Event:")
	    #DisplayError(e)
	    traceback.print_exc()
	    return

    def onDetachHandlerBattery(self):
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
                "\n\t-> Channel:  " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")

        except PhidgetException as e:
	    print("\nError in Detach Event:")
	    #DisplayError(e)
	    traceback.print_exc()
	    return


    """
    * Writes Phidget error info to stderr.
    * Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
    *
    * @param self The Phidget channel that fired the attach event
    * @param errorCode the code associated with the error of enum type ph.ErrorEventCode
    * @param errorString string containing the description of the error fired
    """
    def onErrorHandlerInput(self, errorCode, errorString):
        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def onErrorHandlerOutput(self, errorCode, errorString):
        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def onErrorHandlerBattery(self, errorCode, errorString):
        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    """
    * Outputs the VoltageInput's most recently reported sensor value.
    * Fired when a VoltageInput channel with onSensorChangeHandler registered meets DataInterval and ChangeTrigger criteria
    *
    * @param self The VoltageInput channel that fired the SensorChange event
    * @param sensorValue The reported sensor value from the VoltageInput channel
    """
    def onSensorChangeHandlerInput(self, sensorValue, sensorUnit):
        print("[Sensor Event] -> Sensor Value: " + str(sensorValue) + sensorUnit.symbol)

    def onSensorChangeHandlerOutput(self, sensorValue, sensorUnit):
        print("[Sensor Event] -> Sensor Value: " + str(sensorValue) + sensorUnit.symbol)

    def onSensorChangeHandlerBattery(self, sensorValue, sensorUnit):
        print("[Sensor Event] -> Sensor Value: " + str(sensorValue) + sensorUnit.symbol)


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
		
	relay_right.setOnAttachHandler(relayRightAttachHandler)
        relay_right.setOnDetachHandler(relayRightDetachHandler)
        relay_right.setOnErrorHandler(relayRightErrorHandler)
    
        try:
            relay_right.setDeviceSerialNumber(271638)
            relay_right.setChannel(1)
            print('Wait for relay right to attach...')
            relay_right.openWaitForAttachment(5000)
        except PhidgetException as e:
            print("Program Terminated: Relay Right Open Failed")
            return

        relay_left.setOnAttachHandler(relayLeftAttachHandler)
        relay_left.setOnDetachHandler(relayLeftDetachHandler)
        relay_left.setOnErrorHandler(relayLeftErrorHandler)

        try:
            relay_left.setDeviceSerialNumber(271638)
            relay_left.setChannel(0)
            print('Wait for relay left to attach...')
            relay_left.openWaitForAttachment(5000)
        except PhidgetException as e:
            print("Program Terminated: Relay Left Open Failed")
            return

        """
        * Allocate a new Phidget Channel object
        """
        _input = VoltageInput()

        """
        * Add event handlers before calling open so that no events are missed.
        """
        _input.setOnAttachHandler(onAttachHandlerInput)
        _input.setOnDetachHandler(onDetachHandlerInput)
        _input.setOnErrorHandler(onErrorHandlerInput)
        _input.setOnVoltageChangeHandler(onVoltageChangeHandlerInput)
        _input.setOnSensorChangeHandler(onSensorChangeHandlerInput)

        """
        * Open the channel with a timeout
        """

        print("\nOpening and Waiting for _input Attachment...")

        try:
            _input.setDeviceSerialNumber(271638)
            _input.setChannel(0)
            _input.openWaitForAttachment(5000)
        except PhidgetException as e:
            print("Program Terminated: Open Input Failed")
            print(e)
            return 2

        output = VoltageInput()
        
        """
	* Add event handlers before calling open so that no events are missed.
	"""
        output.setOnAttachHandler(onAttachHandlerOutput)
        output.setOnDetachHandler(onDetachHandlerOutput)
        output.setOnErrorHandler(onErrorHandlerOutput)
        output.setOnVoltageChangeHandler(onVoltageChangeHandlerOutput)
        output.setOnSensorChangeHandler(onSensorChangeHandlerOutput)

        """
    	* Open the channel with a timeout
    	"""
		
        print("\nOpening and Waiting for output Attachment...")

        try:
            output.setDeviceSerialNumber(271638)
    	    output.setChannel(1)
            output.openWaitForAttachment(5000)
        except PhidgetException as e:
	    print("Program Terminated: Open Output Failed")
	    print(e)
    	    return 2
			
        battery = VoltageInput()
        
        """
	* Add event handlers before calling open so that no events are missed.
	"""
        battery.setOnAttachHandler(onAttachHandlerBattery)
        battery.setOnDetachHandler(onDetachHandlerBattery)
        battery.setOnErrorHandler(onErrorHandlerBattery)
        battery.setOnVoltageChangeHandler(onVoltageChangeHandlerBattery)
        battery.setOnSensorChangeHandler(onSensorChangeHandlerBattery)
        
        """
    	* Open the channel with a timeout
        """

        print("\nOpening and Waiting for battery Attachment...")
        
        try:
	    battery.setDeviceSerialNumber(271638)
	    battery.setChannel(2)
	    battery.openWaitForAttachment(5000)
        except PhidgetException as e:
	    print("Program Terminated: Open Battery Failed")
	    print(e)
	    return 2

        print("Sampling data for 60 seconds...")
        
        print("You can do stuff with your Phidgets here and/or in the event handlers.")
        
        time.sleep(60)

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
