import requests
import json
from websocket import create_connection
from globvar import *
from discordapi import *
import random
import karmabot
import emojitable
import time

""" Before you begin, create a file named 'token.cfg' and put your bot token in it. Just the bot token."""

if __name__ == "__main__":
    karma = karmabot.Karma("karma.json")
    
    # Handshake
    gateWay = "wss://gateway.discord.gg/"
    handshakePayload = json.dumps({
        'op': 2,
        'd': {
        'token': token,
        'properties': {},
        'compress': False,
        'large_threshold': 250
        }
    })
    ws = create_connection(gateWay)
    ws.send(handshakePayload)
    readyPayload = json.loads(ws.recv())

    # Start heartbeat
    heartbeatThread = Heartbeat(ws, readyPayload['d']['heartbeat_interval']/1000)
    heartbeatThread.start()

    # trollPingThread = TrollPing()
    # trollPingThread.start()

    # Start receiving messages from gateway
    while True:
        recv_raw = ws.recv()
        if recv_raw != '':
##            print(recv_raw.encode("utf-8"))
##            print("--------------------------------------------------------------------------------------------------------------------------------------------")
            receive = json.loads(recv_raw)
            heartbeatThread.last_seq = receive['s']  # Update hearbeat sequence number
            
            print(json.dumps(receive, indent=2))

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
##                    if receive['d']['author']['id'] == "137685926078840832" and ("Fuck" in contentSplit or "fuck" in contentSplit):
##                        print(sendMessage("Yeah, muck fike!", channelID))
##                    else:
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
                            time.sleep(0.07)
                        
                    
                    
                    





                # Wrong!bot
##                elif receive['d']['author']['id'] != "174655468273270786":  # The bot's ID.
##                    if random.random() < 0.1:
##                        print(sendMessage("WRONG!", channelID))
                        
                
               # # # Shit x says 
               # # if len(contentSplit) > 2 and contentSplit[0].lower() == "shit" and contentSplit[2].lower() == "says":
               # #     username = contentSplit[1]
               # #     messageList = getMessageJson(channelID)
               # #     if messageList == "ERROR":
               # #         sendMessage("PLEASE STOP SENDING SHIT YOU'RE GOING TO MAKE ME LOSE MY DEVKEY", channelID)
               # #     messageString = parseMessageJson(messageList, username)
               # #     if not messageString:
               # #         sendMessage(username + " has never said anything ever!", channelID)
               # #         continue
               # #     s = markov.split_string(messageString)
               # #     m = markov.markov_chain(s)
               # #     mg = markov.markov_generate(m)
               # #     sendMessage(username + ": " + mg, channelID)

