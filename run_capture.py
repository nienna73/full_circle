import sys
import subprocess
import datetime
import os
import math
import time
import signal
from Phidget22.Devices.DigitalOutput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *

def main():
    # Relay Phidget setup
    try:
        relay = DigitalOutput()
    except RuntimeError as e:
        print("Runtime Exception: %s" % e.details)
        print("Exiting....")
        exit(1)

    def relayAttachHandler(e):

        ph = relay
        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            DisplayError(e)
            traceback.print_exc()
            return

    def relayDetachHandler(e):

        ph = relay

        try:
            #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            #www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            DisplayError(e)
            traceback.print_exc()
            return

    def relayErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    try:
        relay.setOnAttachHandler(relayAttachHandler)
        relay.setOnDetachHandler(relayDetachHandler)
        relay.setOnErrorHandler(relayErrorHandler)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        relay.setDeviceSerialNumber(120683)
        relay.setChannel(0)
        relay.open()
        relay.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Digital Input Open Failed")

    total_time = sys.argv[1]
    interval = sys.argv[2]

    camera_ports = []

    ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
    ports_strings_split = ports_strings.split()


    for item in ports_strings_split:
        item = item.decode('utf-8')
        if item[0] == 'u':
            camera_ports.append(item)

    number_of_cameras = len(camera_ports)

    number_of_photos = str(math.ceil(int(total_time)/int(interval)))

    processes = []
    i = 0
    x = 0
    while x < int(number_of_photos):
        i = 0
        time.sleep(int(interval))
        while i < number_of_cameras:
            print(i)
            process = subprocess.Popen(["python3", "capture.py", str(i), number_of_photos, interval, str(x)])
            processes.append(process)
            i = i + 1
        x = x + 1
        relay.setDutyCycle(1.0)
        time.sleep(3)
        relay.setDutyCycle(0.0)
        for proc in processes:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    try:
        relay.close()
        exit(0)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)


main()
# for process in processes:
#         process.wait()
# subprocess.call(["for(int i=0;i<" + str(number_of_cameras) + ";i++));", "do", "python3", "capture.py", "${i}", "done"], shell=True)
# os.system("(for (int i=0;i<" + str(number_of_cameras) + ";i++)); do python3 capture.py ${i} 2 3 done")
