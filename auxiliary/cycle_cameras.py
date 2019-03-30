import time
import os
import subprocess

os.chdir("/home/ryan/uhubctl")

for i in range(4):
    subprocess.call(["./uhubctl", "-a", "0", "-p", str(i+1), "-l", "2-3.2"])
    subprocess.call(["./uhubctl", "-a", "0", "-p", str(i+1), "-l", "2-3"])

time.sleep(10)

for j in range(4):
    subprocess.call(["./uhubctl", "-a", "1", "-p", str(j+1), "-l", "2-3.2"])
    subprocess.call(["./uhubctl", "-a", "1", "-p", str(j+1), "-l", "2-3"])
