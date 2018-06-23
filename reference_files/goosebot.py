#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack and Ryan Jackson'
__version__ = '2.1.8'
__date__ = 'May 17 2010 and April 2013'

#Basic imports
from ctypes import *
import sys, string
import os, random
import subprocess
from time import gmtime, strftime, sleep
from datetime import datetime
import time

#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

#Create an interfacekit object
try:
    interfaceKit = InterfaceKit()
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

#Main Program Code
try:
    interfaceKit.setOnAttachHandler(inferfaceKitAttached)
    interfaceKit.setOnDetachHandler(interfaceKitDetached)
    interfaceKit.setOnErrorhandler(interfaceKitError)
   # interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
   # interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
   # interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
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

print("Setting the data rate for each sensor index to 64ms....")
for i in range(interfaceKit.getSensorCount()):
    try:
        
        interfaceKit.setDataRate(i, 64)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

print("Press Enter to quit....")

#### new code


	
	#turn camera on
interfaceKit.setOutputState(0,1)
sleep(5)

temp=str(round((((interfaceKit.getSensorValue(0)) * 0.22222) - 61.11),1))
RH=str(round((((interfaceKit.getSensorValue(1)) * 0.1906 ) - 40.2 ),1))

print(temp)
print(RH)

#take a photo
time_for_filename=strftime('%Y-%m-%d-%H-%M-%S', gmtime())
photo_file_name="%s.jpg" % (time_for_filename)
photo_file_name_960="%s_960.jpg" % (time_for_filename)
photo_file_name_600="%s_600.jpg" % (time_for_filename)

print("gphoto2 --capture-image-and-download --filename %s" % (photo_file_name))
os.system("gphoto2 --capture-image-and-download --filename %s" % (photo_file_name))


#resize the image   #600x450  #960x720
#convert 2013-04-04-20-09-26.jpg -size 960x720 -contrast -modulate 100,150,100 -auto-gamma 2013-04-04-20-09-26_960.jpg 
#convert 2013-04-04-20-31-31.jpg -size 600x450 2013-04-04-20-31-31_600.jpg
#convert 2013-04-04-20-10-30.jpg -modulate 120,10,100 -fill '#222b6d' -colorize 20 -gamma 0.5 -contrast -contrast 2013-04-04-20-10-30_960.jpg

#resize images
print("resize image to 960px")
os.system("convert %s -resize 960x720 %s" % (photo_file_name,photo_file_name_960))
print("resize image to 600px")
os.system("convert %s -resize 600x450 %s" % (photo_file_name,photo_file_name_600))
#

#create 1 frame of H264 video from the picture
print("Creating 1 frame of H264 video with FFmpeg")
os.system("nice -n 19 ffmpeg -y -i %s -vcodec libx264 -vprofile high -preset slow -b:v 500k -maxrate 500k -bufsize 1000k -vf scale=-1:450  /home/pi/%s.mp4" % (photo_file_name,photo_file_name))

#make a copy of timelapse.mp4
print("Make a copy of timelapse.mp4")
os.system("cp timelapse.mp4 timelapse_copy.mp4")

#concat the 1 frame of video to the larger timelapse.mp4
print("Concat the 1 frame of H264 video to the larger timelapse video using MP4box")
os.system("MP4Box -cat timelapse_copy.mp4 -cat %s.mp4 timelapse.mp4" % (photo_file_name))

#delete 1 frame of H264 video and timelapse_copy.mp4
print("delete 1 frame of H264 video and timelapse_copy.mp4")
os.system("rm %s.mp4" % (photo_file_name))
os.system("rm timelapse_copy.mp4")

#create 1 frame of WebM video from the picture
print("Creating 1 frame of WebM video with FFmpeg")
os.system("nice -n 19 ffmpeg -y -i %s -vcodec libvpx  -cpu-used 0 -b:v 500k -qmin 10 -qmax 42 -maxrate 500k -bufsize 1000k -vf scale=-1:450 /home/pi/%s.webm" % (photo_file_name,photo_file_name))

#make a copy of timelapse.webm
print("Make a copy of timelapse.webm")
os.system("cp timelapse.webm timelapse_copy.webm")

#concat 1 frame of WebM video to timelapse_copy.webm
print("concat 1 frame of WebM video to timelapse_copy.webm")
os.system("mkvmerge -o timelapse.webm -w timelapse_copy.webm + %s.webm" % (photo_file_name))

#delete 1 frame of WebM video and timelapse_copy.webm
print("delete 1 frame of WebM video and timelapse_copy.webm")
os.system("rm %s.webm" % (photo_file_name))
os.system("rm timelapse_copy.webm")


#FTP photo
print("FTP Upload Empty Nest Photo")
print("curl -T %s -u goosebot@punkoryan.com:Pi2theRight ftp://ftp.punkoryan.com" % (photo_file_name))
#os.system("curl -T %s -u goosebot@punkoryan.com:Pi2theRight ftp://ftp.punkoryan.com" % (photo_file_name))
os.system("curl -T %s -u goosebot@punkoryan.com:Pi2theRight ftp://ftp.punkoryan.com" % (photo_file_name_960))
os.system("curl -T %s -u goosebot@punkoryan.com:Pi2theRight ftp://ftp.punkoryan.com" % (photo_file_name_600))

#delete _960 and _600 photos and move high res image
os.system("rm %s" % (photo_file_name_960))
os.system("mv %s /home/pi/imgseq" % (photo_file_name_600))
os.system("mv %s /home/pi/highres" % (photo_file_name))


print("Tweet Temp and RH")
print("twidge update %sTemperature: %s Relative Humidity: %s Photo: http://punkoryan.com/goosebot/%s %s" % ('"',temp,RH,photo_file_name_600,'"'))
#os.system("twidge update %sTemperature: %s Relative Humidity: %s Photo: http://punkoryan.com/goosebot/%s %s" % ('"',temp,RH,photo_file_name_600,'"'))
os.system("twidge update %sKickin' it in the nest. Photo: http://www.journalexpress.com/goosecam/?image=%s&temp=%s&humidity=%s Temperature: %s Relative Humidity: %s  %s" % ('"',photo_file_name_600,temp,RH,temp,RH,'"'))


#turn camera off
interfaceKit.setOutputState(0,0)
	

print("Done.")
exit(0)

#### end new code
chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKit.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
