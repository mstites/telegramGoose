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
            self.msgCount = tools.ofile(msgCountLoc)
        else:
            self.msgCount = 1
            self.write()

        mailTargetLoc = userLoc + '/mailTarget'
        if os.path.exists(mailTargetLoc):
            self.mailTarget = tools.cleanInput(tools.ofile(mailTargetLoc), "\n")
        else:
            self.mailTarget = ***REMOVED***
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
        self.replyDir = 'replies/'
        self.initDir = 'init/'
        self.loadUsers()
        self.handler = events.EventHandler(self.bot)

    def __str__(self):
        return self.bot.getMe()

    def loadUsers(self):
        """Load all known users"""
        self.users = {} # id key, user val
        self.states = {} # state of each users session
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
                text = tools.cleanInput(text)
                reply = events.Message(self.bot, self.replyKey, self.replyDir, chat_id)
                msg, state = reply.loadMsg(text) # how will we make sure it is

            elif state is st.sendMessage:
                user = self.users[chat_id]
                delivery = dt.datetime.now() + dt.timedelta(hours=4)
                store = "I have a message for you!! *uses beak to place in hand*: \n\n\n" + text + "\n\n"
                self.handler.addTimeEvent(delivery, user.mailTarget, 'msg', store)
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
            self.handler.checkTimeEvents()
            time.sleep(10)

if __name__ == "__main__":
    token = "***REMOVED***"
    goose = Bot(token, "assets/messages/replies/~key", "assets/messages/init/~key")
    goose.listen()
