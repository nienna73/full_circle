#! /usr/env/python
import subprocess
import time
import os

subprocess.call(["python", "/home/pi/Documents/full_circle/pi/close_current.py"])
time.sleep(15)

print("Calling slack monitor...")
os.chdir("/home/pi/Documents/full_circle/pi/")
subprocess.call(["python", "slack_monitor.py"])
