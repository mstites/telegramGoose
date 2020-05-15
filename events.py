import tools
import datetime as dt
import pandas as pd
import state as st
import message as ms
import os

class Event:
    def __init__(self, info, dir):
        self.time = info[0]
        self.target = info[1]
        self.action = info[2]
        self.content = info[3]
        self.dir = dir

    def isMsg(self):
        if self.action == 'msg':
            return True
        else:
            return True

    def process(self):
        if self.isMsg():
            opener = ms.Action('delivery&', self.dir)
            openMsg = opener.randSel()
            self.content = openMsg + "\n" + self.content + "\n"

class EventHandler:
    """Handle events"""
    def __init__(self, bot, dir, initDir):
        """bot: bot object
        dir: directory containing storage for messages and dataframe
        initDir: Initial message folder"""
        self.dir = dir
        self.initDir = initDir
        self.df = self.readData("events.pkl")
        self.bot = bot

    def readData(self, fileName):
        """Read dataframe from disk, or create it if it does not exist"""
        self.loc = self.dir + fileName
        if os.path.exists(self.loc):
            return pd.read_pickle(self.loc)
        else: # initialize
            columns = ['time', 'user', 'action', 'content']
            return pd.DataFrame(columns = columns)

    def sortSave(self):
        self.df = self.df.reset_index(drop = True)
        self.df = self.df.sort_values(by='time')
        self.df.to_pickle(self.loc) # save

    def removeEvent(self, loc):
        """Remove event from dataframe"""
        self.df = self.df.drop(loc)
        self.sortSave()

    def addEvent(self, eventInfo):
        """Add event to event dataframe"""
        row = self.makeRow(eventInfo)
        self.df = self.df.append(row, ignore_index=True)
        self.sortSave()

    def cancelEvent(self, user, action):
        """Cancel a previously requested event"""
        filtered = self.df[(self.df.user == user) & (self.df.action == action)]
        filtered = filtered.reset_index()
        if filtered.empty:
            return False
        else:
            last = filtered.iloc[0]['index']
            self.removeEvent(last)
            return True

    def runEvent(self, event):
        """Run an event"""
        if event['action'] == 'msg':
            self.bot.sendMessage(event['user'], event['content'])
            print('Running event: ', event)

    def makeRow(self, eventInfo):
        """Make row from event object.
        eventContent: tuple(time, target, action, content)
        """
        event = Event(eventInfo, self.initDir)
        event.process()
        return {'time':event.time, 'user':event.target, 'action':event.action, 'content':event.content}


    def checkTimeEvents(self):
        # check if it is time to send any events
        if self.df.empty: # no reason to checks
            return
        else:
            currTime = dt.datetime.now()
            nextEvent = self.df.iloc[0]
            if currTime > nextEvent['time']: # activate event
                self.runEvent(nextEvent)
                self.removeEvent(0)
