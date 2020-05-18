import time
import telegram
import telegram.ext
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
            self.mailTarget = ***REMOVED***
            tools.wfile(mailTargetLoc, self.mailTarget)

    def uChatCount(self):
        self.msgCount = int(self.msgCount) + 1
        self.write() # should not do this all the time eventually?

    def write(self):
        location = str(self.loc) + str(self.id) + "/msgCount"
        tools.wfile(location, self.msgCount)

class Bot:
    def __init__(self, token, rFuncKey, rTransKey):
        """Initialize and create bot.
        token: token value for controlling bot
        rFuncKey: key for function runnig from message
        rTransKey: key for translating text to response
        """
        self.updater = telegram.ext.Updater(token, use_context=True)
        self.replyKeys = (tools.loadKeyDict(rFuncKey), tools.loadKeyDict(rTransKey, list = True))
        self.replyDir = "assets/messages/replies/"
        self.initDir = "assets/messages/init/"
        self.loadUsers()
        self.handler = events.EventHandler(self.updater, "assets/", self.initDir)

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
            reply = ms.Reply(self.replyDir, self.replyKeys, text)
            msg, state = reply.loadMsg() # how will we make sure it is
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
        elif state is st.checkIn:
            "I am hearing how you are doing, though am not able to process it quite yet."
            # analyze how are you question
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

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
        # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0
        # telegram.Message.date? Or should I keep universal as to potentially support other platforms?

    def handler(self):
        """Starts the program to listen"""
        dispatcher = self.updater.dispatcher
        textHandler = telegram.ext.MessageHandler(telegram.ext.filters.text, self.start)
        # start_handler = telegram.ext.CommandHandler('start', self.start)
        dispatcher.add_handler(textHandler)
        # need catch all
        self.updater.start_polling()
        # do you want me to send this image?
        # MessageLoop(self.bot, self.handle).run_as_thread()
        # print ("Listening ...")
        # while 1: # Keep the program running.
        #     self.handler.checkTimeEvents()
        #     time.sleep(10)

def run():
    # way to handle when telegram cuts it off for a bit
    token = "***REMOVED***"
    goose = Bot(token, "assets/messages/replies/~funcKey", "assets/messages/replies/~translationKey")
    print(goose.handler.df)
    goose.handler()

if __name__ == "__main__":
    run()

    # restart on error
