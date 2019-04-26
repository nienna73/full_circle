#! /usr/env/python
import sys
import subprocess
import os

def get_status():
	raw_hex = subprocess.check_output(["sudo", "i2cget", "-f", "-y", "1", "0x36", "4", "w"])
	last_two = raw_hex[4:6]
	first_two = raw_hex[2:4]
	
	new_hex = "0x" + str(last_two) + str(first_two)
	
	i = int(new_hex, 16)
	
	percentage = i / 256
	
	print "The battery has " + str(percentage) + "% charge"
	
	return percentage
	
get_status()
