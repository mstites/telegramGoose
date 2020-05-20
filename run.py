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
import threading
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO)

class User:
    def __init__(self, id):
        self.id =  id
        self.loc = "users/"
        self.load()

    def __str__(self):
        # return user id, number of messages, stored messages ,etc
        return str((self.id, self.msgCount, self.mailTarget))

    def load(self):
        userLoc = self.loc + str(self.id)
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
            self.mailTarget = int(tools.cleanInput(tools.ofile(mailTargetLoc), "\n"))
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
    def __init__(self, token):
        """Initialize and create bot.
        token: token value for controlling bot
        """
        self.token = token
        self.loadUsers()
        # self.eventHandler = events.EventHandler(self.updater, "assets/", self.initDir)

    def __str__(self):
        return self.bot.getMe()

    def loadUsers(self):
        """Load all known users"""
        self.users = {} # id key, user val
        self.userStates = {} # state of each users session
        userIds = os.listdir('users')
        for id in userIds:
            id = int(id)
            user = User(id)
            self.users[id] = user
            self.userStates[id] = st.default

    def sendMessage(self, context, user, msg):
        """Send a message from the bot :)"""
        context.bot.send_message(user, msg)
        logging.info(str(user) + ": " + msg)

class botManager:
    """Handles bot updates and actions"""
    def __init__(self, bot, rFuncKey, rTransKey, eventDir):
        self.bot = bot
        # THE ABOVE THREE SHOULD LOAD INTO A MESSAGE OBJECT THAT IS CALLED EVERY TIME A REPLY IS NEEDED
        self.updater = telegram.ext.Updater(self.bot.token, use_context=True)
        self.replyDir = "assets/messages/replies/"
        self.initDir = "assets/messages/init/"
        self.eventHandler = events.EventHandler(self.updater, eventDir, self.initDir)
        self.replyKeys = (tools.loadKeyDict(rFuncKey), tools.loadKeyDict(rTransKey, list = True))
        self.eventDir = eventDir


    def checkEvents(self):
        """Check for events to activate"""
        logging.info("Starting checking events")
        while 1:
            event = self.eventHandler.getEvent()
            logging.debug("Checking event, event = " + event)
            if event == None:
                continue
            else:
                logging.info(self.eventHandler.data)
                user, action, content = event
                if ((action == "msg") or (action == "botmsg")):
                    self.bot.sendMessage(user, content)
                else:
                    self.log.error("")
            time.sleep(10)

    def checkMessages(self, dispatcher):
        logging.info("Starting checking messages")
        self.updater.start_polling()

    def checkCommands(self):
        """Check for terminal input from admin"""
        logging.info("Starting to check for commands")
        cmd = input("")
        if cmd == "quit":
            exit()
        elif cmd == "help":
            print("help: this menu, quit: close program, debug: logging debug mode")
        elif cmd == "debug":
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG)

    def start(self):
        """Starts the program to listen and run events"""
        dispatcher = self.updater.dispatcher
        textHandler = telegram.ext.MessageHandler(telegram.ext.filters.Filters.text, self._textHandler)
        dispatcher.add_handler(textHandler)
        cmdHandler = threading.Thread(target=self.checkCommands)
        eventHandler = threading.Thread(target=self.checkEvents, daemon=True)
        msgHandler = threading.Thread(target=self.checkMessages, args=(dispatcher,), daemon=True)
        cmdHandler.start()
        eventHandler.start()
        msgHandler.start()

    def _textHandler(self, update, context):
        """Handles text message sent to goose bot."""
        msg = update.message.text
        chat_id=update.effective_chat.id
        if chat_id in self.bot.users:
            self.bot.users[chat_id].uChatCount()
            user = self.bot.users[chat_id]
        else: # create user
            user = User(chat_id)
            self.bot.users[chat_id] = user
        def stateHandler(self, user, text):
            state = self.bot.userStates[user.id]
            if state is st.default:
                reply = ms.Reply(self.replyDir, self.replyKeys, text)
                msg, state = reply.loadMsg() # how will we make sure it is
            elif state is st.sendMessage:
                delivery = dt.datetime.now() + dt.timedelta(hours=5)
                self.eventHandler.addEvent((delivery, user.mailTarget, 'msg', text))
                msg = "Message will be sent! *HONK*"
                state = st.default
            if state is st.cancelMessage:
                success = self.eventHandler.cancelEvent(user.mailTarget,  'msg')
                if not success:
                    msg = "No message to delete you silly goose"
                state = st.default
            elif state is st.checkIn:
                "I am hearing how you are doing, though am not able to process it quite yet."
                # analyze how are you question
                state = st.default
            return msg, state
        reply, state = stateHandler(self, user, msg)
        self.bot.userStates[user.id] = state
        self.bot.sendMessage(context, chat_id, reply)

def run():
    # way to handle when telegram cuts it off for a bit
    token = "***REMOVED***"
    goose = Bot(token)
    gooseManager = botManager(goose, "assets/messages/replies/~funcKey", "assets/messages/replies/~translationKey", "assets/")
    gooseManager.start()
    print(gooseManager.eventHandler.data)
    # gooseManager.update()
if __name__ == "__main__":
    run()

    # restart on error
