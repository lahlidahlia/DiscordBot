from globvar import *
from discordapi import *


def changeUser(username=None, avatar=None):
    """

    """
    url = apiBase + "/users/@me"
    header = {"Content-Type": "application/json", "Authorization" : token}
    data = {"username": username, "avatar": avatar }
    r = requests.patch(url, headers=header, data=json.dumps(data))
    return r.text
