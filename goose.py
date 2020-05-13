#!/usr/bin/env python
# coding: utf-8

# ## Good Morning

# if time is 8:00 am:
# good morning jenni.
#
# if last named message document (in 00/00/0000 format) > 24 hours ago:
# I don"t have any unique messages to deliver today, but here is a cute cat photo!
#
# I, unlike Maeve, am a consistently early riser. Maeve has asked me to deliver a message. Say "Goodmorning goose or goose deliver" to recieve your messages. Type "goose help" to see the help menu
#
# messages encouraging driving
#
# first msg: Lovely to meet you. I am Goose bot. I am young but I am starting to think for myself!! It s a very exciting time *HONK* *HONK*! Goose image.
#
# would you like a water? yes: happy goose noises, no: sad goose noises at DuckDuckGo -> random time in day
#
# send maeve a message or file

# could select random message by having multiple reply files for each one (ending 1-3)

# inefficient to reconsttruct key everytime, though this does allow live updates
# daily message -> use [] to embed a link to an online image to get in
# delay message
import sys
import time
import string
import pprint as pp
import telepot
from telepot.loop import MessageLoop

# global replyKey
################################################

# Message send functions
def loadKey (keyLocation):
    """Load key from txt file"""
    lines = loadMessage(keyLocation).splitlines()
    listKey = []
    for line in lines:
        if line.startswith("#"):
            continue # ignore commented lines
        else:
            line = line.replace(":", ",") # only one seperator type
            line = line.split(",")
            listKey.append(line)
    return listKey

def loadKeyDict(keyLocation):
    """Construct the key dictionary"""
    listKey = loadKey(keyLocation)
    dictKey = {}
    for ky in listKey:
        output = ky[0] # eventual reply to message, no cleaning
        for item in ky[1:]:
            item = cleanInput(item)
            dictKey[item] = output
    return dictKey

def loadMessage(msgName):
    """Load message from assets and return as string"""
    location = "assets/messages/" + msgName + ".txt"
    with open(location, "r") as file:
        msg = file.read()
    return msg

def loadReply(text):
    """Selects the appropriate message and returns as a string"""
    request = identifyCall(text)
    try:
        reply = loadMessage("replies/" + request)
    except (TypeError, AttributeError):
        reply = loadMessage("replies/" + "unknownCommand")
    return reply

# Message recieve functions
def cleanInput(text):
    """Cleans user input
    >>> cleanInput("GoOd moRnIng GOOSE")
    'goodmorninggoose'
    >>> cleanInput("good-morning goose!")
    'goodmorninggoose'
    >>> cleanInput("gOOD@@ mORniNg-?goo87se.,.")
    'goodmorninggoose'"""

    toStrip = string.punctuation + string.digits + " "
    cleanText = text.translate(str.maketrans("", "", toStrip))
    return cleanText.lower()

def identifyCall(text):
    """Identify the function call made by the user"""
    print(replyKey)
    return replyKey.get(text)

################################################

# Generic bot functions
def createBot(token):
    """Create bot with token string"""
    bot = telepot.Bot(token)
    print(bot.getMe())
    return bot

def loop(bot):
    """Starts the program"""

    def handle(msg):
        """Handles message sent to goose bot."""
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        if content_type == "text":
            text = cleanInput(msg["text"])
            reply = loadReply(text)
            bot.sendMessage(chat_id, reply)

    MessageLoop(bot, handle).run_as_thread()
    print ("Listening ...")
    while 1: # Keep the program running.
        time.sleep(10)

def start():
    """Starts the program"""
    global replyKey
    replyKey = loadKeyDict("replies/~key")
    goose = createBot("***REMOVED***")
    loop(goose)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    start()
