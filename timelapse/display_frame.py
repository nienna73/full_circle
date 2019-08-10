import subprocess
import os
import sys
import time

def close_current_frame():
    processes = subprocess.check_output(["ps", "aux"])
    break_char = "\n".encode('ascii')
    processes = processes.split(break_char)
    for process in processes:
        process = process.decode("utf-8")
        if "ffplay" in process.lower():
            split_process = process.split()
            subprocess.call(["kill", split_process[1]])
            print ("Killed process ", split_process[-1])

    return

# Get all necessary information from sys and exiftool
frame_name = sys.argv[1]
frame_number = sys.argv[2]
photo_name = "%06d" % (int(frame_number)) + "-A.arw"
shutterspeed = subprocess.check_output(["exiftool", "-shutterspeed", photo_name]).decode('utf-8').split(':')[1].strip()
iso = subprocess.check_output(["exiftool", "-iso", photo_name]).decode('utf-8').split(':')[1].strip()
frame_date = subprocess.check_output(["exiftool", "-modifydate", photo_name]).decode('utf-8')
frame_date = frame_date.replace(":", "$", 1)
frame_date = frame_date.split("$")[1].strip()
frame_date = frame_date.replace(":", ".")

# Build display information (waveform)
# This is done here to avoid having one giant line of text
# in the call to ffplay
display_info = ""
display_info = f"{display_info} split=2[a][b],[b]waveform=g=green:s=ire:fl=15:i=.1:f=chroma:bgopacity=.5,format=yuva444p[bb],"
display_info = f"{display_info}[a][bb]overlay"



subprocess.Popen(["ffplay", frame_name, "-vf", display_info, "-x", "1000", "-y", "500"])
time.sleep(30)
close_current_frame()
