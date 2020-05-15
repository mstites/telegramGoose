import random
import sys
import time
import pprint as pp
import telepot
from telepot.loop import MessageLoop
import string
import os
import datetime as dt
import pandas as pd
import state as st

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
        return str((self.id, self.msgCount, self.mailTarget))

    def load(self):
        userLoc = self.loc+self.id
        if not os.path.exists(userLoc):
            os.makedirs(userLoc)

        msgCountLoc = userLoc + '/msgCount'
        if os.path.exists(msgCountLoc):
            self.msgCount = ofile(msgCountLoc)
        else:
            self.msgCount = 1
            self.write()

        mailTargetLoc = userLoc + '/mailTarget'
        if os.path.exists(mailTargetLoc):
            self.mailTarget = cleanInput(ofile(mailTargetLoc), "\n")
        else:
            self.mailTarget = ***REMOVED***
            wfile(mailTargetLoc, self.mailTarget)

    def uChatCount(self):
        self.msgCount = int(self.msgCount) + 1
        self.write() # should not do this all the time eventually?

    def write(self):
        location = str(self.loc) + str(self.id) + "/msgCount"
        wfile(location, self.msgCount)

class EventHandler:
    """Handle events"""
    def __init__(self, bot):
        self.df = pd.read_pickle('assets/events.pkl')
        self.bot = bot

    def remove(self, event):
        """Remove event from dataframe"""
        self.df = self.df.drop(0)
        self.df = self.df.reset_index()
        self.df.to_pickle('assets/events.pkl')

    def runEvent(self, event):
        """Run an event"""
        if event['action'] == 'msg':
            self.bot.sendMessage(event['user'], event['content'])

    def saveToDisk(self):
        self.df.to_pickle('assets/events.pkl')

    def addTimeEvent(self, time, target, action, content):
        """Add event to event dataframe"""
        row = {'time':time, 'user':target, 'action':action, 'content':content}
        self.df = self.df.append(row, ignore_index=True)
        self.df = self.df.sort_values(by='time')
        self.df = self.df.reset_index()
        self.saveToDisk()

    def checkTimeEvents(self):
        # check if it is time to send any events
        if self.df.empty: # no reason to checks
            return
        else:
            currTime = dt.datetime.now()
            print(currTime)
            nextEvent = self.df.iloc[0]
            print(self.df)
            if currTime > nextEvent['time']: # activate event
                print('hi')
                self.runEvent(nextEvent)
                self.remove(nextEvent)

class Message:
    def __init__(self, bot, key, msgDir, userID):
        """key: dict of the key """
        self.key = key #self.loadKeyDict(keyLocation)
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
            return self.open("replies/unknownCommand"), st.default
        elif self.action(request): #
            action = Action(request, self.userID, self.msgDir)
            return action.process()
        else:
            return self.open(self.msgDir + request), st.default

class Action(Message):
    """Parse action messages"""
    def __init__(self, request, userID, msgDir):
        """request: requset starting
        userID: id of messege originator"""
        self.request = request
        self.userID = userID
        self.msgDir = 'assets/messages/' + msgDir

    def randSel(self):
        """Select random message in request category"""
        clean = self.request[:-1] # remove rand indicator
        dir = self.msgDir+clean
        messages = os.listdir(dir)
        sel = random.randrange(len(messages))
        selDir = dir + '/' + str(sel)
        return ofile(selDir)

    def sendMessage(self):
        msg = ofile(self.msgDir + self.request)
        return msg

    def process(self):
        """Determine action type and run appropriate function"""
        if "&" in self.request:
            self.msg = self.randSel()
            self.state = st.default
        elif self.request == "sendMessage()":
            self.msg = self.sendMessage()
            self.state = st.sendMessage
        else:
            self.msg = "ERROR"
            self.state = st.default
        return self.msg, self.state

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
        self.users = {} # id key, user val
        self.states = {} # state of each users session
        self.loadUsers()
        self.events = EventHandler(self.bot)

    def __str__(self):
        return self.bot.getMe()

    def loadUsers(self):
        """Load all known users"""
        userIds = os.listdir('users')
        for id in userIds:
            user = User(id)
            self.users[int(id)] = user
            self.states[int(id)] = st.default

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
            state = self.states[chat_id]
            text = msg["text"]
            if state is st.default:
                text = cleanInput(text)
                reply = Message(self.bot, self.replyKey, self.replyDir, chat_id)
                msg, state = reply.loadMsg(text) # how will we make sure it is

            elif state is st.sendMessage:
                user = self.users[chat_id]
                delivery = dt.datetime.now() + dt.timedelta(hours=8)
                store = "I have a message for you!! *uses beak to place in hand*: \n\n\n" + text + "\n\n"
                self.events.addTimeEvent(delivery, user.mailTarget, 'msg', store)
                msg = "Message ready to send"
                state = st.default

            elif state is reminder:
                # previous message should have said enter message
                state = st.default

            elif state is reminderTime:
                # previous message should have said enter message time
                state = st.default

            elif state is cancel:
                # enter cancel to delete last message or reminder (Last event)
                state = st.default
                # will need ability to have who entered it

            self.bot.sendMessage(chat_id, msg)
            self.states[chat_id] = state


    def listen(self):
        """Starts the program to listen"""
        MessageLoop(self.bot, self.handle).run_as_thread()
        print ("Listening ...")
        while 1: # Keep the program running.
            self.events.checkTimeEvents()
            time.sleep(10)

if __name__ == "__main__":
    token = "***REMOVED***"
    goose = Bot(token, "assets/messages/replies/~key", "assets/messages/init/~key")
    goose.listen()
