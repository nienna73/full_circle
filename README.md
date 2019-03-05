# full_circle
Project files for Full Circle Visuals

Lessons learned:
1) The cameras will activate in the reverse order they are connected. If you want to trigger cameras 00-05 in that order, connect camera 05 first, followed by 04, then 03, etc. If you connect them in a haphazard way, they will trigger in a haphazard way.

2) If you interrupt 'capture.py' using Ctrl-C, it does not end the processes on the cameras that have not yet taken photos. So, if cameras 00-02 have captured an image as a result of the script and cameras 03-05 have not and you end the process, you will not be able to access/capture from cameras 03-05 until they are turned off and back on.

3) To run the capture program for capturing stills in tethered mode, use: 

for((i=0;i<[number of cameras you're using];i++)); do python capture.py ${i} & done

For example, if you have 6 cameras connected, you would run: 

for((i=0;i<6;i++)); do python capture.py ${i} & done

This will enable all 6 cameras in tethered mode. You will have to manually take the photos, but they will be automatically downloaded to the machine.
IMPORTANT: after running the command, the shell will output some numbers and appear to have stopped running. Wait a few seconds and the script will start running, this is just normal bash output.

## AutomaticTimelapse.py

Use python3 AutomaticTimelapse.py to run this program.

It will ask a series of questions that serve as checks/reminders to the user unless they explicitly ask for (y/n). This program monitors another file on the machine. Whenever a new .jpg or .arw file with readable ISO and shutter speed appears in this folder, AutomaticTimelapse is told to trigger all the cameras using the ISO and shutter speed from that image. That image is saved to a folder that was created when the program was started, named using the convention YYYYMMdd_HHhMMmSSs. This set of six images is passed to PTgui for stitching into a single panorama; this functionality is handled by "wine_stitch.py". That panorama is then passed to video_stitch.py to be converted into a single frame of video and added to a video that has the full timelapse as its occurring.


## TimelapseMagic.py

Use python3 TimelapseMagic.py to run this program.

TimelapseMagic uses an assortment of phidgets to control camera settings and the configuration of the current session. The phidgets are used as follows:

- a rotator to control the length of the section
- a toggle to change the units for the length of the session from minutes to hours
- a rotator to control the delay between each capture
- a toggle to change the units of this delays from minutes to seconds
- a rotator for the length of the video to be taken, in minutes
- a rotator to set the time between starting the system and the cameras recording (present values ranging between minutes and seconds)
- a slider to set the shutter speed
- a slider to set the ISO
- a light sensor to monitor daylight, currently unused
- a button to start the system
- a button to end all system processes
- a toggle to decide is the cameras should snap stills or record video
- a toggle to turn the LCD screen on and off
- an LCD display to show all the details of the above phidgets
- a relay for tethered image capture, currently disabled
- a GPS to add location metadata to the images, currently disabled

Use the phidgets and the LCD display to configure your desired session and press the 'run' button to start a session. To close the session, press the 'kill all' button.
Images and videos from this session are stored in a new folder, created when the program is started. This folder follows the YYYYMMdd_HHhMMmSSs convention.

## TimelapseMonitor.py

Use python3 TimelapseMonitor.py to run this program.

This program checks all currently running programs every 10 seconds. If TimelapseMagic isn't running, it restarts the program. This is used so you can kill all processes in the field and not have to connect to the machine to restart the main program.

## MaxBlast.py

Use python3 MaxBlast.py [int] to run this program.

The int passed in through the command line is the amount of time in seconds you want to wait between each image capture. The images are saved to the camera's SD card with this function. The fasts our Sony cameras can shoot is 4 seconds, so any number >=4 can be passed in. This program is used to capture fast-changing activities, such as an eclipse.

## Other files

The other files are helper files for the main programs described above. These files may be documented in the future, but are not pertinent at the moment.
