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
# goodbye

import sys
import time
import pprint as pp
import telepot
from telepot.loop import MessageLoop
import string
import os

def ofile(location):
    with open(location, "r") as file:
        return file.read()

def wfile(location, data):
    """Write file"""
    # with open(location, "w") as file:
    #     file.write(data)
    #     file.flush()
    file = open(location, "w")
    file.write(str(data))
    file.flush()
    file.close()

def ufile(location, new):
    """Update file, add a new line"""
    pass

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

class User:
    def __init__(self, id):
        self.id = str(id)
        self.loc = "users/"
        self.load()
    def __str__(self):
        # return user id, number of messages, stored messages ,etc
        pass
    def load(self):
        # toLoad = ["msgCount", ...]
        # for...
        if not os.path.exists(self.loc + self.id):
            os.makedirs(self.loc + self.id)
        try:
            self.msgCount = ofile(self.loc + self.id + "/msgCount")
        except FileNotFoundError:
            self.msgCount = 0
            self.write()

    def uChatCount(self):
        self.msgCount = int(self.msgCount) + 1
        self.write() # should not do this all the time eventually?

    def write(self):
        location = str(self.loc) + str(self.id) + "/msgCount"
        wfile(location, self.msgCount)

class Message:
    def __init__(self, bot, keyLocation, msgDir):
        """keyLocation: string of the key location"""
        self.key = self.loadKeyDict(keyLocation)
        self.bot = bot
        self.msgDir = msgDir # default msgDir

    def loadKey (self, keyLocation):
        """Load key from txt file"""
        lines = self.open(keyLocation).splitlines()
        listKey = []
        for line in lines:
            if line.startswith("#"):
                continue # ignore commented lines
            else:
                line = line.replace(":", ",") # only one seperator type
                line = line.split(",")
                listKey.append(line)
        return listKey

    def loadKeyDict(self, keyLocation):
        """Construct the key dictionary"""
        listKey = self.loadKey(keyLocation)
        dictKey = {}
        for ky in listKey:
            output = ky[0] # eventual reply to message, no cleaning
            for item in ky[1:]:
                item = cleanInput(item)
                dictKey[item] = output
        return dictKey

    def open(self, msgName):
        """Load message from assets and return as string"""
        location = "assets/messages/" + msgName + ".txt"
        with open(location, "r") as file:
            msg = file.read()
        return msg

    def loadMsg(self, text):
        """Selects the appropriate message and returns as a string"""
        request = self.key.get(text)
        try:
            loc = ""
            msg = self.open(self.msgDir + request)
        except (TypeError, AttributeError):
            msg = self.open("replies/unknownCommand")
        return msg

    def send(self, chat_id, text):
        """Sends message"""
        msg = self.loadMsg(text)
        self.bot.sendMessage(chat_id, msg)

class Bot:
    def __init__(self, token, replyLoc, initLoc):
        """Initialize and create bot.
        token: token value for controlling bot
        replyLoc: string location of input reply parings
        initLoc: string location of bot initial messages based on input
        """
        self.bot = telepot.Bot(token)
        self.reply = Message(self.bot, replyLoc, 'replies/')
        self.initial = Message(self.bot, initLoc, 'init/')
        self.users = {} # id key, user val
        self.loadUsers()
        # self.users = []

    def __str__(self):
        return self.bot.getMe()

    def loadUsers(self):
        """Load all known users"""
        userIds = os.listdir('users')
        for id in userIds:
            user = User(id)
            self.users[int(id)] = user

    def handle(self, msg):
        """Handles message sent to goose bot."""
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        
        if chat_id in self.users:
            self.users[chat_id].uChatCount()
        else: # add the user and create user object
            user = User(chat_id)
            self.users[chat_id] = user

        if content_type == "text":
            text = cleanInput(msg["text"])
            self.reply.send(chat_id, text)

    def listen(self):
        """Starts the program to listen"""
        MessageLoop(self.bot, self.handle).run_as_thread()
        print ("Listening ...")
        while 1: # Keep the program running.
            time.sleep(10)

if __name__ == "__main__":
    token = "***REMOVED***"
    goose = Bot(token, "replies/~key", "init/~key")
    goose.listen()
