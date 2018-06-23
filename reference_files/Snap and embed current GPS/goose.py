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
import sys, string
import os, random
import subprocess
from time import gmtime, strftime
from datetime import datetime
import time
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, TemperatureChangeEventArgs
from Phidgets.Devices.TemperatureSensor import TemperatureSensor, ThermocoupleType
#import methods for sleeping thread
from time import sleep

#Create an temperaturesensor object
try:
    temperatureSensor = TemperatureSensor()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    inputCount = temperatureSensor.getTemperatureInputCount()
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (temperatureSensor.isAttached(), temperatureSensor.getDeviceName(), temperatureSensor.getSerialNum(), temperatureSensor.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Temperature Inputs: %i" % (inputCount))
    for i in range(inputCount):
        print("Input %i Sensitivity: %f" % (i, temperatureSensor.getTemperatureChangeTrigger(i)))

#Event Handler Callback Functions
def TemperatureSensorAttached(e):
    attached = e.device
    print("TemperatureSensor %i Attached!" % (attached.getSerialNum()))

def TemperatureSensorDetached(e):
    detached = e.device
    print("TemperatureSensor %i Detached!" % (detached.getSerialNum()))

def TemperatureSensorError(e):
    try:
        source = e.device
        if source.isAttached():
            print("TemperatureSensor %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def TemperatureSensorTemperatureChanged(e):
    try:
        ambient = temperatureSensor.getAmbientTemperature()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        ambient = 0.00
    
    source = e.device
    print("TemperatureSensor %i: Ambient Temp: %f -- Thermocouple %i temperature: %f -- Potential: %f" % (source.getSerialNum(), ambient, e.index, e.temperature, e.potential))

#Main Program Code
try:
    temperatureSensor.setOnAttachHandler(TemperatureSensorAttached)
    temperatureSensor.setOnDetachHandler(TemperatureSensorDetached)
    temperatureSensor.setOnErrorhandler(TemperatureSensorError)
    #temperatureSensor.setOnTemperatureChangeHandler(TemperatureSensorTemperatureChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    temperatureSensor.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    temperatureSensor.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        temperatureSensor.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

#print("Setting Thermocouple type...")
#temperatureSensor.setThermocoupleType(0, ThermocoupleType.PHIDGET_TEMPERATURE_SENSOR_K_TYPE)

print("Setting sensitivity of the thermocouple....")
temperatureSensor.setTemperatureChangeTrigger(0, 5.00)  #set the amount of degrees to trigger an update.
sleep(1) #sleep for 5 seconds
print("Sensitivity of thermocouple index 0 is now %f" % (temperatureSensor.getTemperatureChangeTrigger(0)))

print("Press Enter to quit....")

### put the new code here 

csv_file="goose.csv"
in_img="return-pic.jpg"
out_img="left-pic.jpg"
fmt = '%Y-%m-%d %H:%M:%S'

#f = open (csv_file)
#lineList = f.readlines()
#f.close()
#parts=(lineList[-1]).split(',')
#word1=str(parts[4])


temp1=temperatureSensor.getAmbientTemperature()
temp2=temperatureSensor.getTemperature(0)
temp_diff=abs(temp2-temp1)

#define in_nest
in_nest = False


if temp_diff > 3:
	in_nest is True
	print("Setting in_nest to True")
else:
	in_nest is False
	print("Setting in_nest to False")

start_time_in_nest=strftime(fmt, gmtime())

#Set this as First Run as it hasn't entered loop yet so it must be a first run
first_run = True
	
for i in range (99999):
	
		
	#temp1=temperatureSensor.getAmbientTemperature()
	temp1=23
	print("Temp 1")
	print(temp1)
	sleep(1)
	temp2=temperatureSensor.getTemperature(0)
	print("Temp 2")
	print(temp2)
	sleep(1)
	temp_diff=abs(temp2-temp1)
	print("Temp Difference")
	print(temp_diff)
	sleep(1)
			
	
	if temp_diff > 2 and in_nest is False:
		print("She's coming into Nest!")
		sleep(1)
		
		in_nest = True
		
		start_time_in_nest=strftime(fmt, gmtime())
		
		#take_picture  
		print("Take Picture of Empty Nest")
		in_nest_time=strftime('%Y-%m-%d-%H-%M-%S', gmtime())
		in_nest_file_name="%s.jpg" % (in_nest_time)
		print(["gphoto2", "--capture-image-and-download", "--filename", "%s" % (in_nest_file_name)])
		#call(["gphoto2", "--capture-image-and-download", "--filename", "%s" % (in_nest_file_name)])
		os.system("gphoto2 --capture-image-and-download --filename %s" % (in_nest_file_name))
		
		#Turn JPG into ASCII for Terminal Preview
		os.system("jp2a %s" % (in_nest_file_name))
		sleep(1)
		
		#FTP photo
		print("FTP Upload Empty Nest Photo")
		print("curl -T %s -u phidgetSBC2@punkoryan.com:phidget2theLeft ftp://ftp.punkoryan.com" % (in_nest_file_name))
		os.system("curl -T %s -u phidgetSBC2@punkoryan.com:phidget2theLeft ftp://ftp.punkoryan.com" % (in_nest_file_name))
		sleep(1)
		#tweet picture
		print("Tweet Photo of Empty Nest")
		print(["twidge", "update", "Goose came back at %s http://punkoryan.com/phidgetSBC2/%s" % (start_time_in_nest,in_nest_file_name)])
		#call(["twidge", "update", "Goose came back at %s http://punkoryan.com/phidgetSBC2/%s" % (start_time_in_nest,in_nest_file_name)])
		os.system("twidge update %sGoose came back at %s Ambient Temp: %s Goose Temp: %s http://punkoryan.com/phidgetSBC2/%s %s" % ('"',start_time_in_nest,temp1,temp2,in_nest_file_name,'"'))
		sleep(1)
		
		in_img=("http://punkoryan.com/phidgetSBC2/%s" % (in_nest_file_name))
						
		if first_run is True:
			print("She's in the nest. first_run is True so I'll add a new line to the CSV")
			os.system("echo 'In Nest,%s' >> %s" % (start_time_in_nest,csv_file))
		else:
			end_time_out_nest=strftime(fmt, gmtime())
			print("She's in the nest. first_run is FALSE so I'll add a new line to the CSV")
			#calculate how long out of nest
			d1 = datetime.strptime(start_time_out_nest, fmt)
			d2 = datetime.strptime(end_time_out_nest, fmt)
			# convert to unix timestamp
			d1_ts = time.mktime(d1.timetuple())
			d2_ts = time.mktime(d2.timetuple())
			time_out_of_nest_in_seconds=int(d2_ts-d1_ts) 
			time_out_of_nest_in_minutes=(int(d2_ts-d1_ts) / 60)
			time_out_of_nest_in_hours=(int(d2_ts-d1_ts) / 60 /60)
			print ("Out of nest for %i hours, %i minutes and %i seconds" % (time_out_of_nest_in_hours,time_out_of_nest_in_minutes, time_out_of_nest_in_seconds)) #seconds
			duration_time_out_nest=("%i:%i:%i" % (time_out_of_nest_in_hours,time_out_of_nest_in_minutes, time_out_of_nest_in_seconds))
			
			
			with open (csv_file, 'a') as f: f.write ((',%s,%s,%s,') % (end_time_out_nest,duration_time_out_nest,out_img))
			
			with open ('goose.csv', 'a') as f: f.write (('%sIn Nest,%s') % ("\n",start_time_in_nest))
		
			sleep(3)
	
	elif temp_diff > 2 and in_nest is True:
		print("She's staying in nest. Waiting....")
		first_run = False
		#end_time_in_nest=strftime(fmt, gmtime())
		
		sleep(3)		
		
	elif temp_diff < 2 and in_nest is True:	
		
		print("She's Left the Nest!....")
		
		in_nest = False
		start_time_out_nest=strftime(fmt, gmtime())
		
		#take_picture  
		print("Take Picture of Empty Nest")
		out_nest_time=strftime('%Y-%m-%d-%H-%M-%S', gmtime())
		out_nest_file_name="%s.jpg" % (out_nest_time)
		print(["gphoto2", "--capture-image-and-download", "--filename", "%s" % (out_nest_file_name)])
		#call(["gphoto2", "--capture-image-and-download", "--filename", "%s" % (out_nest_file_name)])
		os.system("gphoto2 --capture-image-and-download --filename %s" % (out_nest_file_name))
		
		#Turn JPG into ASCII for Terminal Preview
		os.system("jp2a %s" % (in_nest_file_name))
		
		#FTP photo
		print("FTP Upload Empty Nest Photo")
		print("curl -T %s -u phidgetSBC2@punkoryan.com:phidget2theLeft ftp://ftp.punkoryan.com" % (out_nest_file_name))
		os.system("curl -T %s -u phidgetSBC2@punkoryan.com:phidget2theLeft ftp://ftp.punkoryan.com" % (out_nest_file_name))
		
		#tweet picture
		print("Tweet Photo of Empty Nest")
		print(["twidge", "update", "Goose left the nest at %s http://punkoryan.com/phidgetSBC2/%s" % (start_time_out_nest,out_nest_file_name)])
		#call(["twidge", "update", "Goose left the nest at %s http://punkoryan.com/phidgetSBC2/%s" % (start_time_out_nest,out_nest_file_name)])
		
		out_img=("http://punkoryan.com/phidgetSBC2/%s" % (out_nest_file_name))
		
		if first_run is True:
			print("She's left the nest. first_run is True so I'll add a new line to the CSV")
			os.system("echo 'Out Nest,%s' >> %s" % (start_time_out_nest,csv_file))
		else:
			print("She's left the nest. first_run is FALSE so I'll append to the last line in the CSV")
			end_time_in_nest=strftime(fmt, gmtime())
			#calculate how long in nest
			d1 = datetime.strptime(start_time_in_nest, fmt)
			d2 = datetime.strptime(end_time_in_nest, fmt)
			# convert to unix timestamp
			d1_ts = time.mktime(d1.timetuple())
			d2_ts = time.mktime(d2.timetuple())
			time_in_nest_in_seconds=int(d2_ts-d1_ts) 
			time_in_nest_in_minutes=(int(d2_ts-d1_ts) / 60)
			time_in_nest_in_hours=(int(d2_ts-d1_ts) / 60 /60)
			print ("In nest for %i hours, %i minutes and %i seconds" % (time_in_nest_in_hours,time_in_nest_in_minutes, time_in_nest_in_seconds)) #seconds
			duration_time_in_nest=("%i:%i:%i" % (time_in_nest_in_hours,time_in_nest_in_minutes, time_in_nest_in_seconds))
			
			
			with open ('goose.csv', 'a') as f: f.write ((',%s,%s,%s,') % (end_time_in_nest,duration_time_in_nest,in_img))

			with open ('goose.csv', 'a') as f: f.write (('%sOut Nest,%s') % ("\n",start_time_out_nest))
		
			sleep(3)
		
	elif temp_diff < 2 and in_nest is False:	
		print("She's out of nest. Waiting....")
		first_run = False
		#end_time_out_nest=strftime(fmt, gmtime())
		sleep(3)
	else:
		print("Hmmm....Error...Who'd da thunk it???")
	
			
#chr = sys.stdin.read(1)
### end the new code here

print("Closing...")

try:
    temperatureSensor.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)