import sys
import time
import subprocess
import os

def check_shutter_and_iso(old_files, path):
    shutter_speed = 0
    iso = 0
    new_files = os.listdir(path)
    for file in new_files:
        if file not in old_files:
            print(file)
            if ".jpg" in file.lower() or ".arw" in file.lower():
                iso = subprocess.check_output(["exiftool", "-iso", path+'/'+file])
                iso = iso.decode('utf-8')
                iso = iso.split(':')
                iso = iso[1].strip()
                shutter_speed = subprocess.check_output(["exiftool", "-shutterspeed", path+'/'+file]).decode('utf-8').split(':')[1].strip()
    return {'iso':iso, 'shutter':shutter_speed}
