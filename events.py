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
            return False

    def process(self):
        if self.isMsg():
            opener = ms.Action('delivery&', self.dir)
            openMsg = opener.randSel()
            self.content = openMsg + "\n" + self.content + "\n"
        # elif: self.isBotMsg():
        #     self.content = self.content # probably do not need this elif at
        #     # all then

class EventHandler:
    """Handle events"""
    def __init__(self, bot, dir, initDir):
        """bot: bot object
        dir: directory containing storage for messages and dataframe
        initDir: Initial message folder"""
        self.dir = dir
        self.initDir = initDir
        self.df = self.readData("events.pkl")
        self.loadBotEvents("~events")
        self.bot = bot

    def readData(self, fileName):
        """Read dataframe from disk, or create it if it does not exist"""
        self.loc = self.dir + fileName
        if os.path.exists(self.loc):
            return pd.read_pickle(self.loc)
        else: # initialize
            columns = ['time', 'user', 'action', 'content']
            return pd.DataFrame(columns = columns)

    def parseEventsFile(self, loc):
        """Parse events file, erase events, and return event list objects"""
        file = tools.ofile(loc)
        lines = file.splitlines()
        newFile= []
        events = []
        for line in lines:
            if line.startswith("#"):
                newFile.append(line)
            elif line.startswith("dir:"):
                newFile.append(line)
                line = line.strip("dir: ")
                self.botEventsDir = line
            else:
                line = line.replace("-", ",") # only one seperator
                line = line.replace(":", ",") # only one seperator
                line = line.replace(" ", "") # strip whitespace
                line = line.split(",")
                events.append(line)

        newFile = ('\n'.join(map(str, newFile)))
        tools.wfile(loc, newFile) # delete events from file, they are loaded
        return events


    def loadBotEvents(self, fileName):
        """Load bot events and add them to the dataframe"""
        loc = self.dir + fileName
        events = self.parseEventsFile(loc)
        for event in events:
            time = dt.datetime(int(event[2]), int(event[0]), int(event[1]), int(event[3]), int(event[4]))
            # YEAR, MONTH, DAY, HOUR, MINUTE
            contentLoc = self.botEventsDir + event[7]
            content = tools.ofile(contentLoc)
            self.addEvent((time, int(event[5]), event[6], content))

    def sortSave(self):
        self.df = self.df.sort_values(by='time')
        self.df = self.df.reset_index(drop = True)
        self.df.to_pickle(self.loc) # save

    def removeEvent(self, loc):
        """Remove event from dataframe"""
        self.df = self.df.drop(loc)
        self.sortSave()

    def addEvent(self, eventInfo):
        """Add event to event dataframe
        eventInfo: tuple(time, target, action, content)"""
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
        if ((event['action'] == 'msg') or (event['action'] == 'botmsg')):
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
