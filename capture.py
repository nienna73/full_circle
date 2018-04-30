import subprocess
import time
import threading

camera_ports = []

ports_string = subprocess.check_output(["gphoto2", "--auto-detect"])
ports_string_split = ports_string.split()

for port in ports_string_split:
    if port[0] == 'u':
        camera_ports.append(port)


for port in camera_ports:
    print("Thread" + str(x) + "started")
    threading.Thread(target=loop1_10(port, x)).start()
    x = x + 1
    print(threading.activeCount())

