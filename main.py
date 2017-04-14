#!usr/bin/env python

import requests
import json
import websocket
from discordapi import *
from channelapi import *
from userapi import *
from guildapi import *
import random
import karmabot
import emojitable
import time
from globvar import *

""" Before you begin, create a file named 'token.cfg' and put your bot token in it. Just the bot token."""


def on_open(ws):
    pass


def on_message(ws, recv_raw):
    global userID
    # Start receiving messages from gateway
    receive = json.loads(recv_raw)
    print(json.dumps(receive, indent=2))
    if receive["op"] == 10:
        ws.heartbeatThread = Heartbeat(ws, receive['d']['heartbeat_interval']/1000)
        ws.heartbeatThread.start()

        handshakePayload = json.dumps({
            'op': 2,
            'd': {
            'token': token,
            'properties': {
            },
            'compress': False,
            'large_threshold': 250,
            }
        })

        ws.send(handshakePayload)
        
    if receive["op"] == 0:
        ws.heartbeatThread.last_seq = receive['s']  # Update hearbeat sequence number

        if receive['t'] == 'READY':
            userID = receive['d']['user']['id']
        

        if receive['t'] == 'MESSAGE_CREATE':
            content = receive['d']['content']
            channelID = receive['d']['channel_id']
            guildID = getGuildID(channelID)
            # Also contains userID. It's a global variable.

            messageID = receive['d']['id']
            contentSplit = content.split(" ")

           # Jonisgay 
            if contentSplit[0] == "!jonisgay":  
                print(sendMessage("Jon is g\u00C6y af!", channelID, embed={"title" : "test", "type" : "rich", "description" : "test"}))


            if contentSplit[0] == "!test":
                print(getNick(guildID, userID))


            # Vote
            if contentSplit[0] == "!vote":
                pass

            # Timer
            if contentSplit[0] in ["!time", "!timer"]:
                if len(contentSplit) == 2:
                    Timer(int(contentSplit[1]), 100, channelID).start()
                if len(contentSplit) == 3:
                    Timer(int(contentSplit[1]), int(contentSplit[2]), channelID).start()


            # Trollping
            if contentSplit[0] in ["!trollping", "!tp", "!troll"]:
                changeUser(avatar=avatarBase64)
                originalNick = getNick(guildID, userID)
                alias = "kek"
                if len(contentSplit) > 2:
                    alias = " ".join(contentSplit[2:])
                changeNick(alias, guildID)
                userToPingID = contentSplit[1]
                sentMessage = json.loads(sendMessage("<@!{}>".format(userToPingID), channelID))
                deleteMessage(channelID, messageID)
                deleteMessage(channelID, sentMessage['id'])
                time.sleep(1)
                print(changeNick(originalNick, guildID))
            
            # Amirite
            elif contentSplit[-1] == "amirite?" and len(contentSplit) > 1:
                if contentSplit[-2][-1] == ',':
                    contentSplit[-2] = contentSplit[-2][:-1]  # Strip the comma.
                print(sendMessage("Yeah, {}!".format(" ".join(contentSplit[:-1])), channelID))

            # Karmabot. Activates if first word contains ++ or --
            elif contentSplit[0][-2:] == "++":
                karma.increment(contentSplit[0][:-2])
                karma.dump()
            elif contentSplit[0][-2:] == "--":
                karma.decrement(contentSplit[0][:-2])
                karma.dump()
            elif contentSplit[0] == "!karma"  and len(contentSplit) == 2:
                sendMessage("{}: {}".format(contentSplit[1], karma.read(contentSplit[1])), channelID)

            # Word reactions.
            elif contentSplit[0] == "!react" and len(contentSplit) > 1:
                
                reactMessage = contentSplit[1]
                for i in range(2, len(contentSplit)):
                    reactMessage += " " + contentSplit[i]
                prevMessageJson = json.loads(getPreviousMessage(channelID, messageID))[0]
                prevMessageID = prevMessageJson['id']

                deleteMessage(channelID, messageID)

                spaceCounter = 0
                for char in reactMessage:
                    print(addReaction(charToEmoji(char), channelID, prevMessageID))
                    time.sleep(0.3)


if __name__ == "__main__":
    
    websocket.enableTrace(True)
    # Handshake
    gateWay = "wss://gateway.discord.gg/?encoding=json&v=6"
    ws = websocket.WebSocketApp(gateWay,
                                on_message=on_message,
                                on_open=on_open
                                )
    ws.run_forever()
