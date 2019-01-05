#standard imports
import sys
import time
import subprocess
import os
import datetime

#phidget imports
from Phidget22.Devices.DigitalOutput import *

#custom imports
from file_monitor import check_shutter_and_iso

def main():


    #Setup the relay
    try:
        relay = DigitalOutput()
    except RuntimeError as e:
        print("Runtime Exception: %s" % e.details)
        print("Exiting....")
        exit(1)

    #Relay functions
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
            #DisplayError(e)
            traceback.print_exc()
            return

    def relayErrorHandler(button, errorCode, errorString):

        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def relayStateChangeHandler(self, state):
        if(state == 1):
            print('relay')

        text = str(state)
        textLCD.writeText(LCDFont.FONT_5x8, 13, 1, text)
        textLCD.flush()


    #Setup for digital input
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
        print('Wait for relay attach...')
        relay.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Digital Input Open Failed")


### End relay functions

    # Define variables for use in the loop
    now = datetime.datetime.now()
    dir_name = now.strftime("%Y%m%d_%Hh%Mm%Ss")
    # path = "/home/ryan/" + str(dir_name)
    path = "/home/ryan/watchfile"

    files = []
    x = 0
    while True:
        results = check_shutter_and_iso(files, path)

        iso = results['iso']
        shutter = results['shutter']

        if iso != 0 and shutter != 0:
            print(iso)
            print(shutter)

            try:
                os.chdir(str(dir_name))
            except:
                make_dir = subprocess.Popen(["mkdir", str(dir_name)])
                make_dir.wait()
                os.chdir(str(dir_name))

            camera_ports = []

            ports_strings = subprocess.check_output(["gphoto2", "--auto-detect"])
            ports_strings_split = ports_strings.split()


            for item in ports_strings_split:
                item = item.decode('utf-8')
                if item[0] == 'u':
                    camera_ports.append(item)

            number_of_cameras = len(camera_ports)
            for port in camera_ports:
                print(port)
                subprocess.call(["gphoto2", "--port=" + port, "--set-config-value", "shutterspeed=" + str(shutter), "--set-config-value", "iso=" + str(iso)])

            i = 0
            while i < number_of_cameras:
                process = subprocess.Popen(["python3", "/home/ryan/Documents/full_circle/capture.py", str(x), str(i), '1', '1'])
                i = i + 1
            x += 1
            relay.setDutyCycle(1.0)
            time.sleep(1)
            relay.setDutyCycle(0.0)
            files = os.listdir(path)


    #Close the relay
    try:

        relay.close()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)


main()
