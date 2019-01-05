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
            if ".jpg" in file or ".arw" in file:
                iso = subprocess.check_output(["exiftool", "-iso", file]).decode('utf-8').split(':')[1].strip()
                shutter_speed = subprocess.check_output(["exiftool", "-shutterspeed", file]).decode('utf-8').split(':')[1].strip()
    return {'iso':iso, 'shutter':shutter_speed}
