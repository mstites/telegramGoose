import tools
import os
import random
import state as st

class Message:
    def __init__(self, bot, key, msgDir, userID):
        """key: dict of the key """
        self.key = key #self.loadKeyDict(keyLocation)
        self.userID = userID
        self.msgDir = msgDir # default msgDir

    def open(self, msgName):
        """Load message from assets and return as string"""
        location = self.msgDir + msgName
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
            return self.open("unknownCommand"), st.default
        elif self.action(request): #
            action = Action(request, self.msgDir)
            return action.process()
        else:
            return self.open(request), st.default

class Action(Message):
    """Parse action messages"""
    def __init__(self, request, msgDir):
        """request: requset starting
        userID: id of messege originator"""
        self.request = request
        self.msgDir = msgDir

    def randSel(self):
        """Select random message in request category"""
        messages = os.listdir(self.msgDir + self.request)
        sel = random.randrange(len(messages))
        file = self.request + '/' + str(sel)
        return self.open(file)

    def funcSelector(self):
        """Select function by changing state"""

        if self.request == "sendMessage()":
            state = st.sendMessage
        elif self.request == "cancelMessage()":
            state = st.cancelMessage
        else:
            state = st.default
        return state

    def process(self):
        """Determine action type and run appropriate function"""
        if "&" in self.request:
            self.msg = self.randSel()
            self.state = st.default
        elif "()" in self.request:
            self.msg = self.open(self.request)
            self.state = self.funcSelector()
        else:
            self.msg = "ERROR"
            self.state = st.default
        return self.msg, self.state
