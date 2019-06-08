#! /usr/env/python
import re
import time
import json
from slackclient import SlackClient
import subprocess
import os

#from voltage_monitor import kill_process
from killswitch_engage import engage
from log_status import log_status
from check_filename import check_filename
from voltage_monitor import check_volts, report_volts

def main():
    time.sleep(10)
    
    log_file_name = str(time.strftime("%Y%m%d_%Hh%Mm%Ss")) + "_log.txt"
    log_file = open(log_file_name, "a+")
    log_file.write("\nStart of session\n")
    log_file.close()
    
    slack_token = os.environ.get('KILLBOT_5000_TOKEN')
    slack_client = SlackClient(slack_token)


    # Fetch your Bot's User ID
    user_list = slack_client.api_call("users.list")
    if user_list['ok']:
        for user in user_list.get('members'):
            if user.get('name') == "killbot5000":
                slack_user_id = user.get('id')
                print("Found bot user name")
                break


    # Start connection
    if slack_client.rtm_connect():
        print ("Connected!")
        ticks = 0

        while True:
            for message in slack_client.rtm_read():
                if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id):
                    
                    message_text = message['text'].\
                        split("<@%s>" % slack_user_id)[1].\
                        strip()

                    if re.match(r'.*(engage).*', message_text, re.IGNORECASE):
                        # Engage the relay
                        print("engage")
                        engage()

                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="The killswitch was engaged",
                            as_user=True)
                            
                    if re.match(r'.*(there).*', message_text, re.IGNORECASE):
                        # To check it killbot5000 is online
                        print("you there?")

                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Hello!",
                            as_user=True)
                            
                    if re.match(r'.*(status).*', message_text, re.IGNORECASE):
                        # Report on the input, battery, and output 
                        # voltage status
                        print("status")
                        
                        stati = report_volts()
                        info = ""
                        for key in stati:
                            info += "The " + key[0] + " has " + str(key[1]) + " volts remaining \n"
                        print(info)
                            
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text=info,
                            as_user=True)
                            
                            
                    if re.match(r'.*(help).*', message_text, re.IGNORECASE):
                        # Prouce a usage guide
                        print("help")
                        
                        info = ("Hello! I'm the Killbot5000. I monitor the cameras and "
                               "their power sources. You can use these keywords to communicate " 
                               "with me: \n" 
                               "- 'there' makes sure I'm online \n" 
                               "- 'engage' tells me to toggle the relays \n" 
                               "- 'status' produces a status report of all the power sources \n"
                               "- 'help' brings up this dialogue \n\n"
                               "Happy Killbot-ing!")
                               
                            
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text=info,
                            as_user=True)

            
            if ticks % 60 == 0:
                # Write status to log file every minute
                log_status(log_file_name)
                
            if ticks % 300 == 0:
                # Check volt statuses/stati every 5 minutes
                stati = check_volts()
                if stati != []:
                    for key in stati:
                        info = "The " + key[0] + " has " + str(key[1]) + " volts remaining"
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text=info,
                            as_user=True)
                
            if ticks % 3600 == 0:
                # check for new filename every hour
                new_name = check_filename(log_file_name)
                if new_name != None:
                    log_file_name = new_name


            time.sleep(1)
            ticks += 1
            
    else:
        print("HELP")
        
if __name__ == "__main__":
    main()
