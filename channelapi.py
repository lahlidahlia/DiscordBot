from globvar import *
from discordapi import *


def sendMessage(content, channelID, embed=None):
    """
    Sends a message to the specified channel

    uses globvar: apiBase, token
    content: string
    token: string
    channelID: string
    Possible embed categories: title, description, url, timestamp, color, footer,
                           image, thumbnail, video, provider, fields.
    """
    
    url = apiBase + "/channels/" + channelID + "/messages"
    header = {"Content-Type": "application/json", "Authorization" : token}
    data = {"content" : content, "embed" : embed}
    r = requests.post(url, headers=header, data=json.dumps(data))
    return r.text


def editMessage(content, channelID, messageID):
    url = apiBase + "/channels/" + channelID + "/messages/" + messageID
    header = {"Content-Type": "application/json", "Authorization" : token}
    data = {"content" : content}
    r = requests.patch(url, headers=header, data=json.dumps(data))
    return r.text


def getGuildID(channelID):
    url = apiBase + "/channels/" + channelID
    header = {"Content-Type": "application/json", "Authorization" : token}
    r = requests.get(url, headers=header)
    return json.loads(r.text)['guild_id']


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
