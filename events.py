import tools
import random
import os
import datetime as dt
import pandas as pd
import state as st

class EventHandler:
    """Handle events"""
    def __init__(self, bot):
        self.df = pd.read_pickle('assets/events.pkl')
        self.bot = bot

    def remove(self, event):
        """Remove event from dataframe"""
        self.df = self.df.drop(0)
        self.df = self.df.reset_index(drop = True)
        self.df.to_pickle('assets/events.pkl')

    def runEvent(self, event):
        """Run an event"""
        if event['action'] == 'msg':
            self.bot.sendMessage(event['user'], event['content'])
            print('Running event: ', event)

    def saveToDisk(self):
        self.df.to_pickle('assets/events.pkl')

    def addTimeEvent(self, time, target, action, content):
        """Add event to event dataframe"""
        row = {'time':time, 'user':target, 'action':action, 'content':content}
        self.df = self.df.append(row, ignore_index=True)
        self.df = self.df.sort_values(by='time')
        self.df = self.df.reset_index(drop = True)
        self.saveToDisk()

    def checkTimeEvents(self):
        # check if it is time to send any events
        if self.df.empty: # no reason to checks
            return
        else:
            currTime = dt.datetime.now()
            nextEvent = self.df.iloc[0]
            if currTime > nextEvent['time']: # activate event
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
        return tools.ofile(selDir)

    def sendMessage(self):
        msg = tools.ofile(self.msgDir + self.request)
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
