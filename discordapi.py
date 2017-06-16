import threading
import json
import time
import requests
from globvar import *
from channelapi import *
from guildapi import *
from userapi import *
import emojitable


class Heartbeat(threading.Thread):
    """
    Run this class as a thread to send heartbeat to the websocket
    Make sure to update last_seq every time a new sequence number comes along
    """
    def __init__(self, ws, interval):
        super(Heartbeat, self).__init__()
        self.interval = interval
        self.last_seq = 3
        self.ws = ws
        self.payload = {"op" : 1, "d" : self.last_seq}
    def run(self):
        while True:
            self.payload["d"] = self.last_seq
            self.ws.send(json.dumps(self.payload))
            print("Sending Heartbeat...")
            print(json.dumps(self.payload))
            time.sleep(self.interval)


class Timer(threading.Thread):
    def __init__(self, duration, length, channelID):
        super(Timer, self).__init__()
        self.duration = duration
        self.channelID = channelID
        self.length = length 
        
    def run(self):
        if self.duration < 1:
            return
        counter = 1
        message = "```diff\n-  0 |" + " "*self.length + "| " + str(self.duration) + "\n```"
        # Send message
        messageID = json.loads(sendMessage(message, self.channelID))["id"]
        while counter <= self.duration:
            time.sleep(1)
            # Coloring
            if counter <= float(self.duration)/3:
                message = "```diff\n-"
            elif counter <= float(self.duration)*2/3:
                message = "```fix\n "
            else: 
                message = "```diff\n+"
            # Countup counter
            message += "  " + str(counter) + " |"
            # Progress bar calculation
            progress = int(round(((float(counter)/self.duration*self.length))))
            message += "-"*progress + " "*(self.length-progress) + "| " + str(self.duration) + "\n```"
            response = json.loads(editMessage(message, self.channelID, messageID))
            if "code" in response and response["code"] == 10008:
                return
            counter += 1
        addReaction(u"\U000023F0", self.channelID, messageID)
        #for char in "done!":
            #addReaction(charToEmoji(char), self.channelID, messageID)
            #time.sleep(0.5)


def charToEmoji(char, spaceCounter=0):
    """ 
    If you insert a space, make sure you have your own
    space counter and increment it. Space counter goes from 0 to 3.
    """
    if char in emojitable.table:
        print(char)
        if char == ' ':
            emoji = emojitable.table[char][spaceCounter]
        else:
            emoji = emojitable.table[char]
    return emoji


def parseMessageJson(messageList, username=None):
    """
    messageList: list - Should be a bunch of dictionaries within a list.
    username: string - optional - Used to find message only from that user. Username is case sensitive.
        If username is not given, everyone's message will be used

    Returns a big string that contains all of the user's message.
    """
    retString = ""
    for d in messageList:
        if username != "All":
            if username != d['author']['username']:  # If the message doesn't belong to the specified user.
                continue
        retString += " [BEGIN] " + d["content"] + " [END]"

    return retString


if __name__ == "__main__":
    from pprint import pprint
    r = requests.patch(apiBase + "/users/@me", headers={"Authorization" : token}, data={"username":"lol"})
    print(r.text)
