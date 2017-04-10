# Globvars
f = open("token.cfg", "r")
tokenString = f.read()
f.close()
apiBase = "https://discordapp.com/api"
token = "Bot " + tokenString[:-1]
once = True

f = open("blankImage64.txt", "r")
avatarBase64 = f.read()

global userID
userID = None  # Will be set in the READY payload.
