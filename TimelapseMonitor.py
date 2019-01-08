# This program is designed to monitor the TimelapseMagic file
# It runs on system startup and checks for the TimelapseMagic file
# every 10 seconds. If the program is running, it waits 10 seconds
# and checks again. If the program is not running, it starts it
# and prints a message to the terminal indicating this action

# This program has a desktop shortcut, TimelapseMonitor.desktop, that's
# what gets opened/called on system startup

__author__ = 'Jolene Poulin'
__version__ = '0.3.2'
__date__ = 'August 31st, 2018'

import sys
import time
import subprocess
import os

# Having functions is best practice :)
def main():
# Always run, never stop
    while True:

        # Get a list of all processes that are currently running
        # and decode them so they can be easily processed
        processes = subprocess.check_output(["ps", "-ef"])
        processes_list = processes.split()
        for i in range(0, len(processes_list)):
            processes_list[i] = processes_list[i].decode('utf-8')

        # Print each process so we have some indication it's working
        for process in processes_list:
            print(process)

        # If TimelapseMagic isn't running, start it up
        if not '/home/ryan/Documents/full_circle/TimelapseMagic.py' in processes_list:
            os.system('gnome-terminal -x python3 /home/ryan/Documents/full_circle/TimelapseMagic.py')
            print('Relaunching Program')

        # Wait 10 seconds before checking again
        time.sleep(10)

main()
