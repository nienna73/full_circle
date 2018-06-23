# full_circle
Project files for Full Circle Visuals

Lessons learned:
1) The cameras will activate in the reverse order they are connected. If you want to trigger cameras 00-05 in that order, connect camera 05 first, followed by 04, then 03, etc. If you connect them in a haphazard way, they will trigger in a haphazard way.
2) If you interrupt 'capture.py' using Ctrl-C, it does not end the processes on the cameras that have not yet taken photos. So, if cameras 00-02 have captured an image as a result of the script and cameras 03-05 have not and you end the process, you will not be able to access/capture from cameras 03-05 until they are turned off and back on.
3) To run the capture program for capturing stills in tethered mode, use: for((i=0;i<[number of cameras you're using];i++)); do python capture.py ${i} & done
For example, if you have 6 cameras connected, you would run: for((i=0;i<6;i++)); do python capture.py ${i} & done
This will enable all 6 cameras in tethered mode. You will have to manually take the photos, but they will be automatically downloaded to the machine.
IMPORTANT: after running the command, the shell will output some numbers and appear to have stopped running. Wait a few seconds and the script will start running, this is just normal bash output.
