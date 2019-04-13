import sys
import subprocess
import os
import time

def change_priority():
    time.sleep(3)

    ps = subprocess.Popen(['ps', 'ax'], stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', 'gphoto'), stdin=ps.stdout)
    ps.wait()

    output = output.decode('utf-8')
    output = output.split('\n')

    pid_list = []
    for item in output:
        item = item.split()
        print(item)
        if len(item) > 1:
            pid_list.append(item[0])

    for pid in pid_list:
        subprocess.call(["renice", "0", pid])
