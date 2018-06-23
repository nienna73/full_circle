#!/usr/bin/env python

import sys, string
import os
import subprocess


#### make tmp links to pictures and rename sequence "x=1; for i in /home/pi/imgseq/*jpg; do counter=$(printf %03d $x); ln "$i" /tmp/img"$counter".jpg; x=$(($x+1)); done" 
#print("Creating symlinks and renaming image sequence")
#os.system("x=1; for i in /home/pi/imgseq/*jpg; do counter=$(printf %s%s $x); ln %s$i%s /tmp/img%s$counter%s.jpg; x=$(($x+1)); done" % ('%0','3d','"','"','"','"'))

#ffmpeg create h264 video from image sequence
#print("Creating H264 video with FFmpeg")
#os.system("nice -n 19 ffmpeg -y -i /tmp/img%s%s.jpg -vcodec libx264 -vprofile high -preset slow -b:v 500k -maxrate 500k -bufsize 1000k -vf scale=-1:450  /home/pi/timelapse.mp4" % ('%0','3d'))

#ffmpeg create webm video from image sequence
#print("Creating WebM video with FFmpeg")
#os.system("nice -n 19 ffmpeg -y -i /tmp/img%s%s.jpg -vcodec libvpx  -cpu-used 0 -b:v 500k -qmin 10 -qmax 42 -maxrate 500k -bufsize 1000k -vf scale=-1:450 /home/pi/timelapse.webm" % ('%0','3d'))

#FTP upload H264 video
#print("FTP upload timelapse.mp4")
#os.system("curl --progress-bar --upload-file /home/pi/timelapse.mp4 -u goosebot@punkoryan.com:Pi2theRight ftp://ftp.punkoryan.com")

#FTP upload webm video
#print("FTP upload timelapse.webm")
#os.system("curl --progress-bar --upload-file /home/pi/timelapse.webm -u goosebot@punkoryan.com:Pi2theRight ftp://ftp.punkoryan.com")

#print("Delete /tmp/*.jpg files")
#os.system("sudo rm -rf /tmp/*.jpg")

print("Copy timelapse.mp4 to timelapse_upload.mp4")
os.system("cp timelapse.mp4 timelapse_upload.mp4")

print("Copy timelapse.webm to timelapse_upload.webm")
os.system("cp timelapse.webm timelapse_upload.webm")

print("Upload timelapse_upload.mp4 and rename on server")
os.system("curl --progress-bar --upload-file /home/pi/timelapse_upload.mp4 -u goosebot@punkoryan.com:Pi2theRight ftp://ftp.punkoryan.com -Q %s-RNFR timelapse_upload.mp4%s -Q %s-RNTO timelapse.mp4%s" % ('"','"','"','"',))

print("Upload timelapse_upload.webm and rename on server")
os.system("curl --progress-bar --upload-file /home/pi/timelapse_upload.webm -u goosebot@punkoryan.com:Pi2theRight ftp://ftp.punkoryan.com -Q %s-RNFR timelapse_upload.webm%s -Q %s-RNTO timelapse.webm%s" % ('"','"','"','"',))

print("Delete timelapse_upload.mp4")
os.system("rm timelapse_upload.mp4")

print("Delete timelapse_upload.webm")
os.system("rm timelapse_upload.webm")

print("Done.")
exit(0)



#### check if process is running.... if yes, then wait a few seconds.... ?

#this just needs to take timelapse_working and copy it to timelapse.mp4  that way it is never uploading a working file. 

#  rename file after upload
#curl -T infile ftp://upload.com/dir/ -Q "-RNFR infile" -Q "-RNTO newname" 