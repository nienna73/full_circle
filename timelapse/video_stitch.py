# These two functions are used to stitch images as they're taken
# input_files.txt is a text file that stores the names of the
# videos to be concatenated.

### Questions: where does the stitched video get stored?
### I imagine I should make a folder with the same name
### as the directory where the images are stored, and add
### a _preview to the end of it and that's where all the
### stitched .jpgs and the .mp4 should be...

import subprocess
import os

# This function is for stitching all videos beyond the first one
def video_stitch(x, path_to_jpg, path_to_mp4, log_file):
    try:
        image_number = "%06d" % (x+1)

        photo_name = "%06d" % (int(x+1)) + "-A.arw"
        shutterspeed = subprocess.check_output(["exiftool", "-shutterspeed", photo_name]).decode('utf-8').split(':')[1].strip()
        iso = subprocess.check_output(["exiftool", "-iso", photo_name]).decode('utf-8').split(':')[1].strip()
        frame_date = subprocess.check_output(["exiftool", "-modifydate", photo_name]).decode('utf-8')
        frame_date = frame_date.replace(":", "$", 1)
        frame_date = frame_date.split("$")[1].strip()
        frame_date = frame_date.replace(":", ".")

        display_info = ""
        display_info = f"{display_info} drawtext='text='Frame number = {str(x+1)}"
        display_info = f"{display_info}    Shutterspeed = {str(shutterspeed)}"
        display_info = f"{display_info}    ISO = {str(iso)}"
        display_info = f"{display_info}    Date = {str(frame_date)}':"
        display_info = f"{display_info} fontcolor=white: fontsize=36: box=1: boxcolor=black@0.5:"
        display_info = f"{display_info} boxborderw=5: x=(w-text_w): y=(h-text_h)'"

        # take the next stitched image and make it into the newest-video-frame
        subprocess.call(["ffmpeg", "-y", "-framerate", "24", "-i", path_to_jpg + image_number + "-A.jpg", "-s", "2048x1024", "-vcodec", "libx264", "-cmp", "22", path_to_mp4 + "temp-frame.mp4"])

        # add information overlay
        # first one adds the logo,
        # second one adds all other information
        subprocess.call(["ffmpeg", "-y", "-i", path_to_mp4 + "temp-frame.mp4", "-vf", "movie=../FCV_Logo_White_160x80.png [watermark]; [in][watermark] overlay=10:main_h-overlay_h-10 [out]", path_to_mp4 + "temp-frame-logo.mp4"])
        subprocess.call(["ffmpeg", "-y", "-i", path_to_mp4 + "temp-frame-logo.mp4", "-vf", display_info, path_to_mp4 + "newest-video-frame.mp4"])

        # take the current full-stitched-video and add the newest-video-frame to the end of it.
        subprocess.call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "/home/ryan/watchfile/input_files.txt", "-c", "copy", path_to_mp4 + "new-full-stitched-video.mp4"])

        # over write the full-stitched-video with the new-full-stitched-video
        subprocess.call(["mv", "-f", path_to_mp4 + "new-full-stitched-video.mp4", path_to_mp4 + "full-stitched-video.mp4"])
        # repeat as new stitched images come in

        filepath = path_to_jpg + log_file
        log_file = open(filepath, "a+")
        message = "Attached new frame to video: " + image_number + "\n"
        log_file.write(message)
        log_file.close()
        show_frame(path_to_mp4 + "newest-video-frame.mp4", x+1)
        return 0
    except:
        # Print the error to the terminal and to the log file
        print("\n\nError in attaching new frame to video:")
        print(e)
        filepath = path_to_jpg + log_file
        log_file = open(filepath, "a+")
        log_file.write("Error in attaching new frame to video \n")
        # log_file.write(str(e) + '\n\n')
        log_file.close()
        show_frame(path_to_mp4 + "new-full-stitched-video.mp4", x+1)
        return -1

# This function is for stitching the first video
def first_stitch(path_to_jpg, path_to_mp4, log_file):
    try:

        photo_name = "%06d" % 1 + "-A.arw"
        shutterspeed = subprocess.check_output(["exiftool", "-shutterspeed", photo_name]).decode('utf-8').split(':')[1].strip()
        iso = subprocess.check_output(["exiftool", "-iso", photo_name]).decode('utf-8').split(':')[1].strip()
        frame_date = subprocess.check_output(["exiftool", "-modifydate", photo_name]).decode('utf-8')
        frame_date = frame_date.replace(":", "$", 1)
        frame_date = frame_date.split("$")[1].strip()
        frame_date = frame_date.replace(":", ".")

        display_info = ""
        display_info = f"{display_info} drawtext='text='Frame number = 1"
        display_info = f"{display_info}    Shutterspeed = {str(shutterspeed)}"
        display_info = f"{display_info}    ISO = {str(iso)}"
        display_info = f"{display_info}    Date = {str(frame_date)}':"
        display_info = f"{display_info} fontcolor=white: fontsize=36: box=1: boxcolor=black@0.5:"
        display_info = f"{display_info} boxborderw=5: x=(w-text_w): y=(h-text_h)'"


        # take first stitched  image and call it full-stitched-video
        subprocess.call(["ffmpeg", "-y", "-framerate", "24", "-i", path_to_jpg + "000001-A.jpg", "-s", "2048x1024", "-vcodec", "libx264", "-cmp", "22", path_to_mp4 + "temp-frame.mp4"])

        # add information overlay
        # first one adds the logo,
        # second one adds all other information
        subprocess.call(["ffmpeg", "-y", "-i", path_to_mp4 + "temp-frame.mp4", "-vf", "movie=../FCV_Logo_White_160x80.png [watermark]; [in][watermark] overlay=10:main_h-overlay_h-10 [out]", path_to_mp4 + "temp-frame-logo.mp4"])
        subprocess.call(["ffmpeg", "-y", "-i", path_to_mp4 + "temp-frame-logo.mp4", "-vf", display_info, path_to_mp4 + "full-stitched-video.mp4"])

        show_frame(path_to_mp4 + "full-stitched-video.mp4", 1)
        return 0
    except AttributeError as e:
        # Print the error to the terminal and to the log file
        print("\n\nError in attaching new frame to video:")
        print(e)
        log_file = open(filename, "a+")
        log_file.write("Error in creating first stitched image: \n")
        log_file.write(str(e) + '\n\n')
        log_file.close()
        return -1

def show_frame(frame_name, x):
    subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/timelapse/display_frame.py", frame_name, str(x)])
    return
