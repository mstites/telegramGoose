import tools
import os
import datetime as dt
import pandas as pd
import state as st
import message as ms

class Event:
    def __init__(self, time, target, action, content):
        self.time = time
        self.target = target
        self.action = action
        self.content = content

    def isMsg(self):
        if self.action == 'msg':
            return True
        else:
            return True

    def process(self):
        if self.isMsg():
            opener = ms.Action('delivery&', 'init/')
            openMsg = opener.randSel()
            self.content = openMsg + "\n\n\n" + self.content + "\n\n"

class EventHandler:
    """Handle events"""
    def __init__(self, bot):
        self.df = pd.read_pickle('assets/events.pkl')
        self.bot = bot

    def remove(self, loc):
        """Remove event from dataframe"""
        self.df = self.df.drop(loc)
        self.df = self.df.reset_index(drop = True)
        self.df.to_pickle('assets/events.pkl')

    def cancel(self, user, action):
        """Cancel a previously requested event"""
        # find last event by user and action
        # delete event
        pass

    def runEvent(self, event):
        """Run an event"""
        if event['action'] == 'msg':
            self.bot.sendMessage(event['user'], event['content'])
            print('Running event: ', event)

    def saveToDisk(self):
        self.df.to_pickle('assets/events.pkl')

    def addTimeEvent(self, time, target, action, content):
        """Add event to event dataframe"""
        event = Event(time, target, action, content)
        event.process()
        row = {'time':event.time, 'user':event.target, 'action':event.action, 'content':event.content}
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
                self.remove(0)
