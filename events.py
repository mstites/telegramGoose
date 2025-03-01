import tools
import datetime as dt
import pandas as pd
import state as st
import message as ms
import random
import os
import logging
import numpy as np

def seriesToEvent(series, dir):
    """Convert a series to an event"""
    info = (series['time'], series['user'],
    series['action'], series['content'], series['recurring'])
    return Event(info, dir)

class Event:
    def __init__(self, info, dir):
        self.time = info[0]
        self.target = info[1]
        self.action = info[2]
        self.content = info[3]
        self.recurring = info[4]
        self.dir = dir

    def __str__(self):
        return str((self.time, self.target, self.action, self.content, self.recurring))

    def prepareSend(self):
        """Preparing for sending by loading the specific information"""
        if self.action == "userMsg": # add prefix
            opener = ms.Action(self.dir, 'delivery')
            self.content = opener.open() + "\n" + self.content + "\n"
        elif os.path.isdir(self.content): # load random file in dir
            sel = random.choice(os.listdir(self.content))
            self.content = self.content + sel
        if self.action == "msg" and os.path.isfile(self.content): # open content
            self.content = tools.ofile(self.content)

class EventDF:
    def __init__(self, loc, eventsLoc):
        """Location of file"""
        self.loc = loc
        self.eventsLoc = eventsLoc
        self.data = self.readData()
        self.loadBotEvents()

    def readData(self):
        """Read dataframe from disk, or create it if it does not exist"""
        if os.path.exists(self.loc):
            return pd.read_pickle(self.loc)
        else: # initialize
            columns = ['time', 'user', 'action', 'content', 'recurring']
            return pd.DataFrame(columns = columns)

    def sortSave(self):
        """Sort and save dataframe"""
        self.data = self.data.sort_values(by='time')
        self.data = self.data.reset_index(drop = True)
        self.data.to_pickle(self.loc, protocol=4) # save

    def removeEvent(self, eventLoc):
        """Remove event from dataframe"""
        self.data = self.data.drop(eventLoc)
        self.sortSave()

    def addEvent(self, eventInfo):
        """Add event to event dataframe
        eventInfo: tuple(time, target, action, content)"""
        row = self.makeRow(eventInfo)
        self.data = self.data.append(row, ignore_index=True)
        self.sortSave()

    def loadBotEvents(self):
        """Load bot events and add them to the dataframe"""
        header = pd.read_csv(self.eventsLoc, nrows=4, sep=";")
        df = pd.read_csv(self.eventsLoc, skiprows=4, sep=";")
        for index, row in df.iterrows():
            # load time
            date = list(map(int, row['Date'].split("-")))
            time = list(map(int, row['Time'].split("-")))
            eTime = dt.datetime(date[2], date[0], date[1], time[0], time[1])
            # load recurring
            recurring = tuple()
            recurring = tuple(map(int, row['Recurring'].split("-")))
            # add event
            self.addEvent((eTime, int(row['UserID']), row['Type'], row['Content'], recurring))
        header.to_csv(self.eventsLoc, index=False, sep=";") # overwrite


class EventHandler(EventDF):
    """Handle events"""
    def __init__(self, bot, dir, initDir):
        """bot: bot object
        dir: directory containing storage for messages and dataframe
        initDir: Initial message folder"""
        self.bot = bot
        self.dir = dir
        self.initDir = initDir
        super().__init__(dir + "events.pkl", dir + "newEvents.csv") # load data

    def cancelEvent(self, user, action):
        """Cancel a previously requested event"""
        filtered = self.data[(self.data.user == user) & (self.data.action == action)]
        filtered = filtered.reset_index()
        if filtered.empty:
            return False
        else:
            last = filtered.iloc[0]['index']
            self.removeEvent(last)
            return True

    def runEvent(self, event):
        """Run an event"""
        # schedule next event if recurring
        if event.recurring != (0,0): # recurring
            next = random.randint(event.recurring[0], event.recurring[1])
            time = event.time + dt.timedelta(days=next)
            self.addEvent((time, event.target, event.action,
            event.content, event.recurring)) # same event, new time
        # run event
        event.prepareSend()
        if event.action == "msg" or event.action == "userMsg":
            self.bot.sendMessage(event.target, event.content)
        elif event.action == "img":
            self.bot.sendImage(event.target, event.content)

        # delete event
        self.removeEvent(0)
        logging.info('Running event: ' + str(event))


    def makeRow(self, eventInfo):
        """Make row from event object.
        eventContent: tuple(time, target, action, content, recurring)"""
        event = Event(eventInfo, self.initDir)
        logging.debug(event)
        return {'time':event.time, 'user':event.target, 'action':event.action, 'content':event.content, 'recurring':event.recurring}


    def getEvent(self):
        """Check if it is time to send any events."""
        if not self.data.empty: # data exists
            currTime = dt.datetime.now()
            next = self.data.iloc[0]
            if currTime > next['time']: # activate event
                return seriesToEvent(next, self.initDir)
            else:
                return None
        return None
