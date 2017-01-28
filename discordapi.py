import threading
import json
import time
import requests
from globvar import *


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

        
def sendMessage(content, channelID):
    """
    Sends a message to the specified channel

    uses globvar: apiBase, token
    content: string
    token: string
    channelID: string
    """
    
    url = apiBase + "/channels/" + channelID + "/messages"
    header = {"Authorization" : token}
    data = {"content" : content}
    r = requests.post(url, headers=header, data=data)
    return r.text

def getPreviousMessage(channelID, messageID):
    """
    Get the most recent message sent in a channel.

    uses globvar: apiBase, token
    content: string
    token: string
    channelID: string
    messageID: string
    """
    
    url = apiBase + "/channels/" + channelID + "/messages"
    header = {"Authorization" : token}
    param = {"before" : messageID, "limit" : 1}
    r = requests.get(url, headers=header, params=param)
    return r.text

def addReaction(reaction, channelID, messageID):
    """
    PUT/channels/{channel.id}/messages/{message.id}/reactions/{emoji}/@me

    Add one reaction to a message.
    reaction: emoji string.
    """
    url = apiBase + "/channels/" + channelID + "/messages/" + messageID + "/reactions/" + reaction + "/@me" # %F0%9F%91%8C%F0%9F%8F%BD
    header = {"Authorization" : token}
    r = requests.put(url, headers=header)
    return r.text
    

def changeUsername(content, channelID):
    """
    Sends a message to the specified channel

    uses globvar: apiBase, token
    content: string
    token: string
    channelID: string
    """
    
    url = apiBase + "/channels/" + channelID + "/messages"
    header = {"Authorization" : token}
    data = {"content" : content}
    r = requests.post(url, headers=header, data=data)
    return r.text

def deleteMessage(channelID, messageID):
    """
    Sends a message to the specified channel

    uses globvar: apiBase, token
    content: string
    token: string
    channelID: string
    """
    
    url = apiBase + "/channels/" + channelID + "/messages/" + messageID
    header = {"Authorization" : token}
    r = requests.delete(url, headers=header)
    return r.text

def getMemberList(guildID):
    """
    Get the list of guild members
    
    uses globvar: apiBase, token
    guildID: string
    """
    url = apiBase + "/guilds/" + guildID + "/members"
    headers = {"Authorization" : token}
    r = requests.get(url, headers=headers, params={"limit" : 50})
    return r.text
    

def getMessageJson(channelID):
    """
    Get all the messages from the specified channelID in a json

    uses globvar: apiBase, token
    channelID: string
    username: string - optional - Used to find message only from that user. Username is case sensitive.

    Returns a list of message informations
    """
    url = apiBase + "/channels/" + channelID + "/messages"
    header = {"Authorization" : token}
    
    messageList = []
    before = None  # Parameter used to get messages beyond the limit.
    counter = 0
    while True:
        counter += 1
        params = {"limit" : 100, "before" : before}
        r = requests.get(url, headers=header, params=params)
        if r.status_code == 429:
            print(r.text)
            print("ERROR ERROR ERROR ERROR ERROR ERROR")
            return "ERROR"
        receiveList = json.loads(r.text)
        if len(receiveList) == 0 or counter == 10:  # If we ran out of messages.
            return messageList
        messageList += receiveList
        before = receiveList[len(receiveList)-1]['id']

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
