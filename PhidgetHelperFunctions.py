import sys
from Phidget22.PhidgetException import *
from Phidget22.ErrorCode import *
from Phidget22.Phidget import *
from Phidget22.Net import *

class NetInfo():
    def __init__(self):
        self.isRemote = None
        self.serverDiscovery = None
        self.hostname = None
        self.port = None
        self.password = None

class ChannelInfo():
    def __init__(self):
        self.serialNumber = -1
        self.hubPort = -1
        self.isHubPortDevice = 0
        self.channel = -1
        self.isVINT = None
        self.netInfo = NetInfo()

class EndProgramSignal(Exception):
    def __init__(self, value):
        self.value = str(value )

class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg

# Returns None if an error occurred, True for 'Y' and False for 'N'
def ProcessYesNo_Input(default):

    strvar = sys.stdin.readline(100)
    if not strvar:
        raise InputError("Empty Input String")

    strvar = strvar.replace('\r\n', '\n') #sanitize newlines for Python 3.2 and older
    if (strvar[0] == '\n'):
        if (default == -1):
            raise InputError("Empty Input String")
        return default

    if (strvar[0] == 'N' or strvar[0] == 'n'):
        return False

    if (strvar[0] == 'Y' or strvar[0] == 'y'):
        return True

    raise InputError("Invalid Input")

def DisplayError(e):
    sys.stderr.write("Desc: " + e.details + "\n")

    if (e.code == ErrorCode.EPHIDGET_WRONGDEVICE):
        sys.stderr.write("\tThis error commonly occurs when the Phidget function you are calling does not match the class of the channel that called it.\n"
                        "\tFor example, you would get this error if you called a PhidgetVoltageInput_* function with a PhidgetDigitalOutput channel.")
    elif (e.code == ErrorCode.EPHIDGET_NOTATTACHED):
        sys.stderr.write("\tThis error occurs when you call Phidget functions before a Phidget channel has been opened and attached.\n"
                        "\tTo prevent this error, ensure you are calling the function after the Phidget has been opened and the program has verified it is attached.")
    elif (e.code == ErrorCode.EPHIDGET_NOTCONFIGURED):
        sys.stderr.write("\tThis error code commonly occurs when you call an Enable-type function before all Must-Set Parameters have been set for the channel.\n"
                        "\tCheck the API page for your device to see which parameters are labled \"Must be Set\" on the right-hand side of the list.")


def InputSerialNumber(channelInfo):

    deviceSerialNumber = -1
    channelInfo.deviceSerialNumber = deviceSerialNumber
    return


def InputIsHubPortDevice(channelInfo):
    isHubPortDevice = -1

    channelInfo.isHubPortDevice = isHubPortDevice

    return

def InputVINTProperties(channelInfo, ph):
    canBeHubPortDevice = 0
    pcc = -1
    hubPort = -1
    isVINT = 0

    channelInfo.isVINT = isVINT

    channelInfo.hubPort = hubPort

    try:
        pcc = ph.getChannelClass()
    except PhidgetException as e:
        sys.stderr.write("Runtime Error -> Getting ChannelClass: \n\t")
        DisplayError(e)
        raise

    if (pcc == ChannelClass.PHIDCHCLASS_VOLTAGEINPUT):
        canBeHubPortDevice = 1
    elif (pcc == ChannelClass.PHIDCHCLASS_VOLTAGERATIOINPUT):
        canBeHubPortDevice = 1
    elif (pcc == ChannelClass.PHIDCHCLASS_DIGITALINPUT):
        canBeHubPortDevice = 1
    elif (pcc == ChannelClass.PHIDCHCLASS_DIGITALOUTPUT):
        canBeHubPortDevice = 1

    if (canBeHubPortDevice):
        InputIsHubPortDevice(channelInfo)

    return

def InputChannel(channelInfo):
    isHubPortDevice = 0
    channel = 0

    # Hub port devices only have a single channel, so don't ask for the channel
    if (channelInfo.isHubPortDevice):
        return

    channelInfo.channel = channel

    return

def SetupNetwork(channelInfo):
    hostname = ""
    password = ""
    discovery = 0
    isRemote = 0
    port = 0

    channelInfo.netInfo.isRemote = isRemote

    channelInfo.netInfo.serverDiscovery = discovery

    channelInfo.netInfo.hostname = hostname
    channelInfo.netInfo.port = port
    channelInfo.netInfo.password = password

    return

def PrintOpenErrorMessage(e, ph):
    sys.stderr.write("Runtime Error -> Opening Phidget Channel: \n\t")
    DisplayError(e)
    if(e.code == ErrorCode.EPHIDGET_TIMEOUT):
        sys.stderr.write("\nThis error commonly occurs if your device is not connected as specified, "
                         "or if another program is using the device, such as the Phidget Control Panel.\n")
        sys.stderr.write("\nIf your Phidget has a plug or terminal block for external power, ensure it is plugged in and powered.\n")
        if(     ph.getChannelClass() != ChannelClass.PHIDCHCLASS_VOLTAGEINPUT
            and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_VOLTAGERATIOINPUT
            and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_DIGITALINPUT
            and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_DIGITALOUTPUT
        ):
            sys.stderr.write("\nIf you are trying to connect to an analog sensor, you will need to use the "
                              "corresponding VoltageInput or VoltageRatioInput API with the appropriate SensorType.\n")

        if(ph.getIsRemote()):
            sys.stderr.write("\nEnsure the Phidget Network Server is enabled on the machine the Phidget is plugged into.")

def PrintEnableServerDiscoveryErrorMessage(e):
    sys.stderr.write("Runtime Error -> Enable Server Discovery: \n\t")
    DisplayError(e)
    if(e.code == ErrorCode.EPHIDGET_UNSUPPORTED):
        sys.stderr.write("\nThis error commonly occurs if your computer does not have the required mDNS support. "
                         "We recommend using Bonjour Print Services on Windows and Mac, or Avahi on Linux.\n")


def AskForDeviceParameters(ph):
    channelInfo = ChannelInfo()
    InputSerialNumber(channelInfo)
    InputVINTProperties(channelInfo, ph)
    InputChannel(channelInfo)
    SetupNetwork(channelInfo)
    return channelInfo
