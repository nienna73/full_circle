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
def video_stitch(x, path, log_file):
    try:
        image_number = "%06d" % (x)

        # take the next stitched image and make it into the newest-video-frame
        subprocess.call(["ffmpeg", "-y", "-framerate", "24", "-i", path + "/" + image_number + "-A.jpg", "-s", "2048x1024", "-vcodec", "libx264", "-cmp", "22", path + "/" + "newest-video-frame.mp4"])
        # take the current full-stitched-video and add the newest-video-frame to the end of it.
        # subprocess.call(["ffmpeg", "-y", "-i", "concat:" + path + "full-stitched-video.mp4|" + path + "newest-video-frame.mp4", "-c", "copy", path + "new-full-stitched-video.mp4"])

        # subprocess.call(["ffmpeg", "-y", "-f", "concat", "-i", path + "full-stitched-video.mp4", "-i", path + "newest-video-frame.mp4", "-c", "copy", path + "new-full-stitched-video.mp4"])
        subprocess.call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "input_files.txt", "-c", "copy", path + "/" + "new-full-stitched-video.mp4"])
        # over wright the full-stitched-video with the new-full-stitched-video
        subprocess.call(["mv", "-f", path + "/" + "new-full-stitched-video.mp4", path + "/" + "full-stitched-video.mp4"])
        # repeat as new stitched images come in
    except(e):
        print("\n\nError in attaching new frame to video:")
        print(e)
        log_file = open(filename, "a+")
        log_file.write(str(e) + '\n\n')
        log_file.close()

# This function is for stitching the first video
def first_stitch(path, log_file):
    try:
        # take first stitched  image and call it full-stitched-video
        subprocess.call(["ffmpeg", "-y", "-framerate", "24", "-i", path + "/000001-A.jpg", "-s", "2048x1024", "-vcodec", "libx264", "-cmp", "22", path + "/" +"full-stitched-video.mp4"])
    except(e):
        print("\n\nError in attaching new frame to video:")
        print(e)
        log_file = open(filename, "a+")
        log_file.write(str(e) + '\n\n')
        log_file.close()
