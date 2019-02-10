import subprocess
import os
import sys
import time

# files = subprocess.check_output((["ls", "/home/ryan/Desktop/20190125_19h15m23s_sourceJPGs"]))
files = subprocess.check_output((["ls", "/home/ryan/Desktop/Stitch_Test_Images"]))
files = files.decode('utf-8')
files = files.splitlines()

x = 0

while x < len(files):
    photo_location = '/home/ryan/Desktop/Stitch_Test_Images/' + files[x]
    subprocess.call(["cp", "-f", photo_location, "/home/ryan/watchfile"])

    time.sleep(60)
    x += 1
