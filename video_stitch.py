import subprocess

def video_stitch(x):
    try:
        #take first stitched  image and call it full-stitched-video
        subprocess.call(["ffmpeg", "-y", "-framerate", "24", "-i", "00000" + str(x) + "-A.jpg", "-s", "2048x1024", "-vcodec", "libx264", "-cmp", "22", "full-stitched-video.mp4"])
        #take the next stitched image and make it into the newest-video-frame
        subprocess.call(["ffmpeg", "-y", "-framerate", "24", "-i", "00000" + str(x+1) + "-A.jpg", "-s", "2048x1024", "-vcodec", "libx264", "-cmp", "22", "newest-video-frame.mp4"])
        #take the current full-stitched-video and add the newest-video-frame to the end of it.
        subprocess.call(["ffmpeg", "-y", "-i", "\"concat:full-stitched-video.mp4|newest-video-frame.mp4\"", "-c", "copy", "new-full-stitched-video.mp4"])
        #over wright the full-stitched-video with the new-full-stitched-video
        subprocess.call(["mv", "-f", "new-full-stitched-video.mp4", "full-stitched-video.mp4"])
        #repeat as new stitched images come in
    except:
        print("Error in attaching new frame to video")
