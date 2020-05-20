import tools
import datetime as dt
import pandas as pd
import state as st
import message as ms
import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO)
class Event:
    def __init__(self, info, dir):
        self.time = info[0]
        self.target = info[1]
        self.action = info[2]
        self.content = info[3]
        self.dir = dir

    def __str__(self):
        return str((self.time, self.target, self.action, self.content))

    def isMsg(self):
        if self.action == 'msg':
            return True
        else:
            return False

    def process(self):
        if self.isMsg():
            opener = ms.Action(self.dir, 'delivery')
            openMsg = opener.open()
            self.content = openMsg + "\n" + self.content + "\n"
        # elif: self.isBotMsg():
        #     self.content = self.content # probably do not need this elif at
        #     # all then

class EventDataFrame:
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
            columns = ['time', 'user', 'action', 'content']
            return pd.DataFrame(columns = columns)

    def sortSave(self):
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

    def _parseEventsFile(self):
        """Parse events file, erase events, and return event list objects"""
        file = tools.ofile(self.eventsLoc)
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
        tools.wfile(self.eventsLoc, newFile) # delete events from file, they are loaded
        return events

    def loadBotEvents(self):
        """Load bot events and add them to the dataframe"""
        events = self._parseEventsFile()
        for event in events:
            time = dt.datetime(int(event[2]), int(event[0]), int(event[1]), int(event[3]), int(event[4]))
            # YEAR, MONTH, DAY, HOUR, MINUTE
            contentLoc = self.botEventsDir + event[7]
            content = tools.ofile(contentLoc)
            self.addEvent((time, int(event[5]), event[6], content))

class EventHandler(EventDataFrame):
    """Handle events"""
    def __init__(self, bot, dir, initDir):
        """bot: bot object
        dir: directory containing storage for messages and dataframe
        initDir: Initial message folder"""
        self.bot = bot
        self.dir = dir
        self.initDir = initDir
        super().__init__(dir + "events.pkl", dir + "~events") # load data

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
        if ((event['action'] == 'msg') or (event['action'] == 'botmsg')):
            self.bot.sendMessage(event['user'], event['content'])
            logging.info('Running event: ' + event)

    def makeRow(self, eventInfo):
        """Make row from event object.
        eventContent: tuple(time, target, action, content)
        """
        event = Event(eventInfo, self.initDir)
        event.process()
        logging.debug(event)
        return {'time':event.time, 'user':event.target, 'action':event.action, 'content':event.content}

    def getEvent(self):
        # check if it is time to send any events
        if self.data.empty: # no reason to check, no event
            return None
        else:
            currTime = dt.datetime.now()
            nextEvent = self.data.iloc[0]
            if currTime > nextEvent['time']: # activate event
                self.removeEvent(0) # deling may not allow to be ran?
                return (nextEvent(1), nextEvent(2), nextEvent(3)) # (user, action, content)
            else:
                return None
