import sys
import time
import subprocess
import os

while True:
    processes = subprocess.check_output(["ps", "-ef"])
    processes_list = processes.split()
    for i in range(0, len(processes_list)):
        processes_list[i] = processes_list[i].decode('utf-8')

    for process in processes_list:
        print(process)

    if not '/home/ryan/Documents/full_circle/TimelapseMagic.py' in processes_list:
        # subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/TimelapseMagic.py"])
        os.system('gnome-terminal -x python3 /home/ryan/Documents/full_circle/TimelapseMagic.py')
        print('Relaunching Program')

    time.sleep(30)
