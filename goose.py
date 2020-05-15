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

# way to get name and use that in addition to ID, that way for sending messages you can see names
# could also just have property for user on who to send messages to


# Reminders:
# Dictionary with keys being reminder time and values being message to send
# Have another dictionary with keys being date and values being dictionary with times for that days
# Store in user/#/reminders, have a file caled time?

# similar type but with messages

# cute aggression generation, random times for honks

# when asking for positivity, give photo or message. Less command like
# if you cannot directly request

# add message contains capabilities, instead of just is

# how are you doing?
# I can't offer too much. But have a nuzzle and a cat photo
# that is great! what is making it so good!

# daily mail can just be one big file

# should add instructions on how to change things
# or could make everything in one central document

# get rid of txt?

import random
import sys
import time
import pprint as pp
import telepot
from telepot.loop import MessageLoop
import string
import os

# date = (0, 0, 0)
# time = (0, 0)

def updateTime():
    utc = time.localtime()
    global t
    global date
    date = (utc.tm_mon, utc.tm_mday, utc.tm_year) # (##/##/####)
    t = (utc.tm_hour, utc.tm_min) # (##,##) in 24 hour time

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

def cleanInput(text, toStrip = string.punctuation + string.digits + " "):
    """Cleans user input
    toStrip = characters to remove"""
    cleanText = text.translate(str.maketrans("", "", toStrip))
    return cleanText.lower()

def loadKey (loc):
    """Load key from txt file"""
    lines = ofile(loc).splitlines()
    listKey = []
    for line in lines:
        if line.startswith("#"):
            continue # ignore commented lines
        else:
            line = line.replace(":", ",") # only one seperator type
            line = line.split(",")
            listKey.append(line)
    return listKey

def loadKeyDict(loc):
    """Construct the key dictionary"""
    listKey = loadKey(loc)
    dictKey = {}
    for ky in listKey:
        output = ky[0] # eventual reply to message, no cleaning
        for item in ky[1:]:
            item = cleanInput(item)
            dictKey[item] = output
    key = dictKey
    return key

class User:
    def __init__(self, id):
        self.id = str(id)
        self.loc = "users/"
        self.load()

    def __str__(self):
        # return user id, number of messages, stored messages ,etc
        return str((self.id, self.msgCount))

    def load(self):
        # toLoad = ["msgCount", ...]
        # for...
        if not os.path.exists(self.loc + self.id):
            os.makedirs(self.loc + self.id)
        try:
            self.msgCount = ofile(self.loc + self.id + "/msgCount")
        except FileNotFoundError:
            self.msgCount = 1
            self.write()

    def uChatCount(self):
        self.msgCount = int(self.msgCount) + 1
        self.write() # should not do this all the time eventually?

    def write(self):
        location = str(self.loc) + str(self.id) + "/msgCount"
        wfile(location, self.msgCount)

class Event:
    # each user should have its own event object
    # certain signal for delete after sent
    # maybe just each is mark sent active after sent, and then create a new object
    # for repeating
    # should I be sending messages from this class?
    # way to check if the event has already been activated. Like some sort of check
    # on the file name??? Or write to file? Daily actions
    def __init__(self):
        # load events from file
        # should probably inherit from messages
        pass

    def checkTime(self):
        # check time events
        pass

    def checkMess(self):
        # check message count eventsprint(cleanInput(str(date), "(), "))
        pass

    def checkEvents(self):
        # run the checks
        pass

class Message:
    def __init__(self, bot, key, msgDir, userID):
        """key: dict of the key """
        self.key = key #self.loadKeyDict(keyLocation)
        self.bot = bot
        self.userID = userID
        self.msgDir = msgDir # default msgDir

    def open(self, msgName):
        """Load message from assets and return as string"""
        location = "assets/messages/" + msgName
        with open(location, "r") as file:
            msg = file.read()
        return msg

    def action(self, request):
        """Check if request is action"""
        if (("&" in request) or ("()" in request)):
            return True
        else:
            return False

    def loadMsg(self, text):
        """Selects the appropriate message and returns as a string"""
        request = self.key.get(text)
        if request is None:
            return self.open("replies/unknownCommand")
        elif self.action(request): #
            action = Action(request, self.userID)
            return action.process()
        else:
            return self.open(self.msgDir + request)

    def send(self, text):
        """Sends message"""
        msg = self.loadMsg(text)
        self.bot.sendMessage(self.userID, msg)

class Action(Message):
    """Parse action messages"""
    def __init__(self, request, userID):
        """request: requset starting
        userID: id of messege originator"""
        self.request = request
        self.userID = userID

    def randSel(self):
        """Select random message in request category"""
        clean = self.request[:-1] # remove rand indicator
        dir = 'assets/messages/replies/'+clean
        messages = os.listdir(dir)
        sel = random.randrange(len(messages))
        selDir = dir + '/' + str(sel)
        return ofile(selDir)

    def deliverDaily(self):
        """Open daily messages - mailbox"""
        global date
        uDir = 'users/' + str(self.userID) + '/mailbox/'
        date = cleanInput(str(date), "(), ")
        dir = uDir + date
        if os.path.exists(dir):
            msg = ofile(uDir + date)
            return '*HONK* Here are your messages:' + msg
        else:
            return "No new mail today"

    def process(self):
        """Determine action type and run appropriate function"""
        if "&" in self.request:
            self.msg = self.randSel()
        elif self.request == "deliverMessage()":
            self.msg = self.deliverDaily()
        else:
            self.msg = "ERROR"
        return self.msg

class Bot:
    def __init__(self, token, replyLoc, initLoc):
        """Initialize and create bot.
        token: token value for controlling bot
        replyLoc: string location of input reply parings
        initLoc: string location of bot initial messages based on input
        """
        self.bot = telepot.Bot(token)
        self.replyKey = loadKeyDict(replyLoc)
        self.replyDir = 'replies/'
        self.initDir = 'init/'
        # self.reply = Message(self.bot, replyLoc, 'replies/')
        # self.initial = Message(self.bot, initLoc, 'init/')
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
            print(self.users[chat_id])
        else: # add the user and create user object
            user = User(chat_id)
            self.users[chat_id] = user
        if content_type == "text":
            text = cleanInput(msg["text"])
            reply = Message(self.bot, self.replyKey, self.replyDir, chat_id)
            reply.send(text)

    def listen(self):
        """Starts the program to listen"""
        MessageLoop(self.bot, self.handle).run_as_thread()
        print ("Listening ...")
        while 1: # Keep the program running.
            updateTime()
            time.sleep(10)
if __name__ == "__main__":
    updateTime() # initialize time
    token = "***REMOVED***"
    goose = Bot(token, "assets/messages/replies/~key", "assets/messages/init/~key")
    goose.listen()
