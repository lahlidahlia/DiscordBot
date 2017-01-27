# Globvars
f = open("token.cfg", "r")
tokenString = f.read()
f.close()
apiBase = "https://discordapp.com/api"
token = "Bot " + tokenString[:-1]
once = True

