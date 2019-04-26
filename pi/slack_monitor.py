#! /usr/env/python
import re
import time
import json
from slackclient import SlackClient
import subprocess
import os

time.sleep(10)
slack_token = os.environ.get('KILLBOT_5000_TOKEN')
slack_client = SlackClient(slack_token)


# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
if user_list['ok']:
    for user in user_list.get('members'):
        if user.get('name') == "killbot5000":
            slack_user_id = user.get('id')
            break


# Start connection
if slack_client.rtm_connect():
    print ("Connected!")

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id):
                
                # print "Message received: %s" % json.dumps(message, indent=2)

                message_text = message['text'].\
                    split("<@%s>" % slack_user_id)[1].\
                    strip()

                if re.match(r'.*(engage).*', message_text, re.IGNORECASE):
                    print("engage")
                    process = subprocess.Popen(["python", "/home/pi/Documents/full_circle/pi/killswitch_engage.py"])
                    process.wait()

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="The killswitch was engaged",
                        as_user=True)
                        
                if re.match(r'.*(you there).*', message_text, re.IGNORECASE):
                    print("you there?")

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Hello!",
                        as_user=True)


        time.sleep(1)
        
else:
    print("HELP")
