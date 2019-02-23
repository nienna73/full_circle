# This function is dedicated to recording 1 minute of audio
# every hour so as to provide ambient noise/sounds for 
# extended (24h+) timelapses
# It's called by AutomaticTimelapse and nothing else at the moment

__author__ = 'Jolene Poulin'
__version__ = '0.0.1'
__date__ = 'January 31st, 2019'

# General imports
import subprocess
import time
import sys
import os
import datetime

def main():
    # Gather information from arguments passed to function
    filepath = sys.argv[1]

    has_audio = False                       # a bool to store whether or not
                                            # we can record with the Zoom device

    # Get a string of all connected audio devices,
    # decode the string to remove strange characters,
    # split the string into a list to be treated
    audio_devices = subprocess.check_output(["arecord", "--list-devices"])
    audio_devices = audio_devices.decode('utf-8')
    audio_devices = audio_devices.split()

    # Look for the Zoom H2n device
    for device in audio_devices:
        if device.lower() == "h2n":
            has_audio = True

    # Record audio to the filepath passed in
    if has_audio:
        print("Recording with audio")

        # Try navigating to the directory passed in, 
        # return an error if it can't be found/accessed
        try:
            os.chdir(str(filepath))
        except:
            print("Unable to access filepath")
            return

        subprocess.Popen(["arecord", "-d", "60", "-t", "wav", "--use-strftime", "%Y%m%d_%Hh%Mm%vs.wav", "-c", "4", "-f", "S24_LE", "-r48000"])
        # The preferred format is:
        # arecord -d 10 -t wav --use-strftime %Y%m%d_%Hh%Mm%vs.wav -c 4 -f S24_LE -r48000

        time.sleep(3540)
        return

    return


main()
