import requests
import json
from globvar import *
import websocket
from discordapi import *
import random
import karmabot
import emojitable
import time

""" Before you begin, create a file named 'token.cfg' and put your bot token in it. Just the bot token."""


def on_open(ws):
    pass


def on_message(ws, recv_raw):
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
        

        if receive['t'] == 'MESSAGE_CREATE':
            content = receive['d']['content']
            channelID = receive['d']['channel_id']
            messageID = receive['d']['id']
            contentSplit = content.split(" ")

           # Jonisgay 
            if contentSplit[0] == "!jonisgay":  
                print(sendMessage("Jon is g\u00C6y af!", channelID))
            
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
                    if char in emojitable.table:
                        print(char)
                        if char == ' ':
                            emoji = emojitable.table[char][spaceCounter]
                            spaceCounter += 1 if spaceCounter < 3 else 0
                        else:
                            emoji = emojitable.table[char]
                        print(addReaction(emoji, channelID, prevMessageID))
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
