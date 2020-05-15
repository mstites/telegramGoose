import sys
import time
import telepot
from telepot.loop import MessageLoop
import os
import datetime as dt
import pandas as pd
import state as st
import tools
import events
import message as ms

class User:
    def __init__(self, id):
        self.id =  str(id)
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
            self.msgCount = tools.ofile(msgCountLoc)
        else:
            self.msgCount = 1
            self.write()

        mailTargetLoc = userLoc + '/mailTarget'
        if os.path.exists(mailTargetLoc):
            self.mailTarget = tools.cleanInput(tools.ofile(mailTargetLoc), "\n")
        else:
            self.mailTarget = 774796474
            tools.wfile(mailTargetLoc, self.mailTarget)

    def uChatCount(self):
        self.msgCount = int(self.msgCount) + 1
        self.write() # should not do this all the time eventually?

    def write(self):
        location = str(self.loc) + str(self.id) + "/msgCount"
        tools.wfile(location, self.msgCount)

class Bot:
    def __init__(self, token, replyLoc, initLoc):
        """Initialize and create bot.
        token: token value for controlling bot
        replyLoc: string location of input reply parings
        initLoc: string location of bot initial messages based on input
        """
        self.bot = telepot.Bot(token)
        self.replyKey = tools.loadKeyDict(replyLoc)
        self.replyDir = "assets/messages/replies/"
        self.initDir = "assets/messages/init/"
        self.loadUsers()
        self.handler = events.EventHandler(self.bot, "assets/", self.initDir)

    def __str__(self):
        return self.bot.getMe()

    def loadUsers(self):
        """Load all known users"""
        self.users = {} # id key, user val
        self.states = {} # state of each users session
        userIds = os.listdir('users')
        for id in userIds:
            user = User(id)
            self.users[id] = user
            self.states[id] = st.default

    def reply(self, user, text):
        state = self.states[user.id]
        if state is st.default:
            text = tools.cleanInput(text)
            reply = ms.Message(self.bot, self.replyKey, self.replyDir, user.id)
            msg, state = reply.loadMsg(text) # how will we make sure it is

        elif state is st.sendMessage:
            delivery = dt.datetime.now() + dt.timedelta(hours=5)
            self.handler.addEvent((delivery, user.mailTarget, 'msg', text))
            msg = "Message will be sent! *HONK*"
            state = st.default

        elif state is st.reminder:
            # previous message should have said enter message
            state = st.default

        elif state is st.reminderTime:
            # previous message should have said enter message time
            state = st.default

        if state is st.cancelMessage:
            success = self.handler.cancelEvent(user.mailTarget,  'msg')
            if not success:
                msg = "No message to delete you silly goose"
            state = st.default

        return msg, state

    def handle(self, msg):
        """Handles message sent to goose bot."""
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if chat_id in self.users:
            self.users[chat_id].uChatCount()
            user = self.users[chat_id]
        else: # add the user and create user object
            user = User(chat_id)
            self.users[chat_id] = user
            # add intro message to arrive soon

        if content_type == "text":
            text = msg["text"]
            msg, state = self.reply(user, text)
            self.bot.sendMessage(user.id, msg)
            self.states[user.id] = state

    def listen(self):
        """Starts the program to listen"""
        MessageLoop(self.bot, self.handle).run_as_thread()
        print ("Listening ...")
        while 1: # Keep the program running.
            self.handler.checkTimeEvents()
            time.sleep(10)

def loop():
    while 1:
        token = "1165408473:AAFbR7nslY9WPWAx5H3AcOk5Klrf3-9Lp5E"
        goose = Bot(token, "assets/messages/replies/~key", "assets/messages/init/~key")
        print(goose.handler.df)
        goose.listen()
        time.sleep(10)

if __name__ == "__main__":
    loop()

    # restart on error
