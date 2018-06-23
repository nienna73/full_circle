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
from datetime import datetime
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Devices.GPS import GPS

#Create an interfacekit object
try:
    interfaceKit = InterfaceKit()
    gps = GPS()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

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
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

def GPSAttached(e):
    attached = e.device
    print("GPS %i Attached!" % (attached.getSerialNum()))

def GPSDetached(e):
    detached = e.device
    print("GPS %i Detached!" % (detached.getSerialNum()))

def GPSError(e):
    try:
        source = e.device
        print("GPS %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def GPSPositionChanged(e):
    source = e.device
    # print("GPS %i: Latitude: %F, Longitude: %F, Altitude: %F" % (source.getSerialNum(), e.latitude, e.longitude, e.altitude))

def GPSPositionFixStatusChanged(e):
    source = e.device
    if e.positionFixStatus:
        status = "FIXED"
    else:
        status = "NOT FIXED"
    print("GPS %i: Position Fix Status: %s" % (source.getSerialNum(), status))


#Main Program Code
try:
    interfaceKit.setOnAttachHandler(inferfaceKitAttached)
    interfaceKit.setOnDetachHandler(interfaceKitDetached)
    interfaceKit.setOnErrorhandler(interfaceKitError)
    interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
    interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
    interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
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


try:
    gps.setOnAttachHandler(GPSAttached)
    gps.setOnDetachHandler(GPSDetached)
    gps.setOnErrorhandler(GPSError)
    gps.setOnPositionChangeHandler(GPSPositionChanged)
    gps.setOnPositionFixStatusChangeHandler(GPSPositionFixStatusChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    gps.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        gps.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Press Enter to quit....")

try:
    print("GPS Current Time: %s" %(gps.getTime().toString()))
    print("GPS Current Date: %s" %(gps.getDate().toString()))
    print("GPS Current Latitude: %F" %(gps.getLatitude()))
    print("GPS Current Longitude: %F" %(gps.getLongitude()))
    print("GPS Current Altitude: %F" %(gps.getAltitude()))
    print("GPS Current Heading: %F" %(gps.getHeading()))
    print("GPS Current Velocity: %F" % (gps.getVelocity()))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))


print("Press Enter to quit....")


# DO SOMETHING HERE #

# Set digital output port 0 to be on
#interfaceKit.setOutputState(0, 1)
#import time
#time.sleep(3)

#print sensor value of sensor 3  
#print(interfaceKit.getSensorValue(3))

#if sensor 3 is less than 500 then set digital output 0 to false else true

for i in range (3000):
	
		temperature = ((interfaceKit.getSensorValue(0) * 0.22222) - 61.11)
		relative_humidity = ((interfaceKit.getSensorValue(1) * 0.1906) - 40.2)
		#the_date=gps.getDate().toString()
		#the_date2=the_date.replace("/","-")
		#the_time=gps.getTime().toString()
		#the_time2=the_time.replace(":","-")
		the_lat=gps.getLatitude()
		the_long=gps.getLongitude()
		the_date3=datetime.strptime(gps.getDate().toString(), "%d/%m/%Y").strftime("%Y-%m-%d")
		the_time3=datetime.strptime(gps.getTime().toString().partition('.')[0], "%H:%M:%S").strftime("%H-%M-%S")
		file_name="%s_%s_%s_%s.jpg" % (the_date3, the_time3, the_lat, the_long)
		kml_file="map.kml"
		
        

		
		#the_time3=datetime.strptime(gps.getTime().toString(), "%H:%M:%S").strftime("%H-%M-%OS")
		
		#theis works but leaves the decimal of seconds. eg. 10.99218 sec. Need to round it.
		#round(the_time3, 0)
		
		
		print (temperature)
		print (relative_humidity)
		#from time import time
		#print(time())
		#the_time = (time())
		#the_time=(the_time)
		#print(the_time)
		
	#	from datetime import datetime
		the_time=str(datetime.now())
		
		from subprocess import call
		
		
		#call(["twidge", "update", "Temperature: %s Relative Humidity: %s Time: %s" % (temperature, relative_humidity, the_time)])
		#call(["mpg123", "/root/woo.mp3"])
		print(["gphoto2", "--capture-image-and-download", "--filename", "%s" % (file_name)])
		call(["gphoto2", "--capture-image-and-download", "--filename", "%s" % (file_name)])
		
		import os
		
		
		os.system("sed -i 'N;$!P;$!D;$d' %s" % (kml_file))
		os.system("sed -i 'N;$!P;$!D;$d' %s" % (kml_file))
		os.system("echo '<Placemark>' >> %s" % (kml_file))
		os.system("echo '<name>%s_%s</name>' >> %s" % (the_date3, the_time3))
		os.system("echo '<description>' >> %s" % (kml_file))
		os.system("echo '<![CDATA[' >> %s" % (kml_file))
		os.system("echo '%s,%s,%s%s%s />' >> %s" % (the_lat, the_long,'<img width="450" height="300" border="2" src="http://punkoryan.com/phidgetSBC2/',file_name,'"',kml_file))
		os.system("echo ']]>' >> %s" % (kml_file)) 
		os.system("echo '</description>' >> %s" % (kml_file)) 
		os.system("echo '<Point>' >> %s" % (kml_file))
		os.system("echo '<coordinates>%s,%s</coordinates>' >> %s" % (the_long,the_lat,kml_file)) 
		os.system("echo '</Point>' >> %s" % (kml_file))
		os.system("echo '</Placemark>' >> %s" % (kml_file))
		os.system("echo '</Document>' >> %s" % (kml_file))
		os.system("echo '</kml>' >> %s" % (kml_file))
      

		
		
		#print("echo '%s,%s,%s%s%s />,' >> gps-track.csv" % (the_lat, the_long,'<img src="http://punkoryan.com/phidgetSBC2/',file_name,'"'))
		#os.system("echo '%s,%s,%s%s%s />,' >> gps-track.csv" % (the_lat, the_long,'<img src="http://punkoryan.com/phidgetSBC2/',file_name,'"'))
		#import time
		#time.sleep(1)
		
		print("exiftool -overwrite_original -GPSLatitude=%s -GPSLongitude=%s %s" % (the_lat, the_long, file_name))
		os.system("exiftool -overwrite_original -GPSLatitude=%s -GPSLongitude=%s %s" % (the_lat, the_long, file_name))
		
		
		
		#os.system("convert %s -resize 600x400 %s" % (file_name, file_name))
		#import time
		#time.sleep(10)
		
		print("curl -T map.kml -u phidgetSBC2@punkoryan.com:phidget2theLeft ftp://ftp.punkoryan.com")
		os.system("curl -T map.kml -u phidgetSBC2@punkoryan.com:phidget2theLeft ftp://ftp.punkoryan.com")
		
		print("curl -T %s -u phidgetSBC2@punkoryan.com:phidget2theLeft ftp://ftp.punkoryan.com" % (file_name))
		os.system("curl -T %s -u phidgetSBC2@punkoryan.com:phidget2theLeft ftp://ftp.punkoryan.com" % (file_name))
		
		
		
		print(["twidge", "update", "http://punkoryan.com/phidgetSBC2/%s Time: %s Temp: %s" % (file_name, the_time, temperature)])
		call(["twidge", "update", "http://punkoryan.com/phidgetSBC2/%s Time: %s Temp: %s" % (file_name, the_time, temperature)])
		
		import time
		boom=10
		while boom >0:
    			time.sleep(1)
			#print(boom)
			print("%s seconds until take new picture" % (boom))
			boom -=1
	


                

		
		
	#	import time
	#	time.sleep(60)
		
		    
	



# loop until key pressed
	
# chr = sys.stdin.read(1)


print("Closing...")





try:
    interfaceKit.closePhidget()
    gps.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)




