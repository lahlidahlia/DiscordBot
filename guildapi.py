from globvar import *
from discordapi import *
from channelapi import *


def changeNick(nickname, guildID):
    url = apiBase + "/guilds/" + str(guildID) + "/members/@me/nick"
    header = {"Content-Type": "application/json", "Authorization" : token}
    data = {"nick": nickname}
    r = requests.patch(url, headers=header, data=json.dumps(data))
    return r.text


def getNick(guildID, userID):
    url = apiBase + "/guilds/" + str(guildID) + "/members/"  + str(userID)
    header = {"Content-Type": "application/json", "Authorization" : token}
    r = requests.get(url, headers=header)
    if "nick" in json.loads(r.text):
        ret = json.loads(r.text)['nick']
    else:
        ret = json.loads(r.text)['user']['username']

    return ret


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
