#! /usr/env/python
import subprocess
import time

time.sleep(3)

subprocess.Popen(["python", "/home/pi/Documents/full_circle/pi/voltage_monitor.py"])
subprocess.Popen(["python", "/home/pi/Documents/full_circle/pi/slack_monitor.py"])
