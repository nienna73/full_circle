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

frame_name = sys.argv[1]
subprocess.Popen(["ffplay", frame_name, "-vf", "split=2[a][b],[b]waveform=g=green:s=ire:fl=15:i=.1:f=chroma:bgopacity=.5,format=yuva444p[bb],[a][bb]overlay", "-x", "1000", "-y", "500"])
time.sleep(30)
close_current_frame()
