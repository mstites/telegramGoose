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

        mailTargetLoc = userLoc + '/userLoc'
        if os.path.exists(mailTargetLoc):
            self.mailTarget = ofile(mailTargetLoc)
        else:
            self.mailTarget = 774796474
            wfile(mailTargetLoc, self.mailTarget)

    def uChatCount(self):
        self.msgCount = int(self.msgCount) + 1
        self.write() # should not do this all the time eventually?

    def write(self):
        location = str(self.loc) + str(self.id) + "/msgCount"
        wfile(location, self.msgCount)

class Event:
    def __init__(self, time, userID, action, content):
        """
        time: time to send
        userID: user to send to
        action: type
        content: msg
        """
        self.time = time
        self.user = userID
        self.action = action
        self.content = content

    def __str__(self):
        return str(self.status + '/' + self.time + '/' + self.user + '/' + self.action)

class EventHandler:
    """Handle events"""
    def __init__(self, bot):
        self.df = pd.read_pickle('assets/events.pkl')
        self.bot = bot

    def remove(self, event):
        """Remove event from dataframe"""
        self.df = self.df.drop(0)
        self.df = self.df.reset_index()
        print(self.df)

    def runEvent(self, event):
        """Run an event"""
        if event['action'] == 'msg':
            self.bot.sendMessage(event['user'], event['content'])

    def saveToDisk(self):
        self.df.to_pickle('assets/events.pkl')

    def addEvent(self, event):
        """Add event to event dataframe"""
        row = {'time':event.time, 'user':event.user, 'action':event.action, 'content':event.content}
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
            print('next')
            print(nextEvent)
            if currTime > nextEvent['time']: # activate event
                self.runEvent(nextEvent)
                self.remove(nextEvent)

class Reply:
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

class Action(Reply):
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

    def sendMessage(self):
        """Send message"""
        pass

    # REDO?
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
        self.users = {} # id key, user val
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
            reply = Reply(self.bot, self.replyKey, self.replyDir, chat_id)
            reply.send(text)

    def listen(self):
        """Starts the program to listen"""
        MessageLoop(self.bot, self.handle).run_as_thread()
        print ("Listening ...")
        while 1: # Keep the program running.
            self.events.checkTimeEvents()
            time.sleep(10)

if __name__ == "__main__":
    token = "1165408473:AAFbR7nslY9WPWAx5H3AcOk5Klrf3-9Lp5E"
    goose = Bot(token, "assets/messages/replies/~key", "assets/messages/init/~key")
    goose.listen()
