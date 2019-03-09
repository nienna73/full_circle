import subprocess
import os
import sys
import time
from video_stitch import video_stitch, first_stitch

x = int(sys.argv[1])        # number of the photo one before the one we just took
dir_name = sys.argv[2]      # location where all .arw files are stored

filename = sys.argv[3]


full_dir_name = "/home/ryan/Documents/full_circle/" + dir_name + "/"

# Try editing and renaming the .pts file
try:
    if x > 0:

        # Look for the new stitched image before creating the video
        txt_file_check = subprocess.check_output(["ls", full_dir_name])
        txt_file_check = txt_file_check.decode('utf-8')
        txt_file_check = txt_file_check.splitlines()

        old_number = "%06d" % (x)
        new_number = "%06d" % (x+1)
        old_path = full_dir_name + old_number + "-A.pts"
        new_path = full_dir_name + new_number + "-A.pts"
        command = "sed 's/%s/%s/g' %s > %s" % (old_number, new_number, old_path, new_path)
        process = subprocess.call([command], shell=True)
    else:
        new_location = full_dir_name + "000001-A.pts"
        subprocess.call(["cp", "-f", "/home/ryan/Documents/full_circle/template.pts", new_location])
except NameError as e:
    # Print error to the screen and to the log file
    print("Error in renaming .pts file")
    print(e)
    log_file = open(filename, "a+")
    log_file.write("Error in renaming .pts file")
    log_file.close()
except AttributeError as e:
    print(e)

subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/wine_ptgui.py", str(x), str(dir_name), str(filename)])
