#! /usr/env/python
import subprocess
import time


subprocess.call(["python", "/home/pi/Documents/full_circle/pi/close_current.py"])
time.sleep(5)

subprocess.Popen(["python", "/home/pi/Documents/full_circle/pi/voltage_monitor.py"])
subprocess.Popen(["python", "/home/pi/Documents/full_circle/pi/slack_monitor.py"])
