import tools
import os
import random
import state as st

class Message:
    def __init__(self, msgDir, request):
        self.msgDir = msgDir # default msgDir
        self.request = request

    def open(self, msgName):
        """Load message from assets and return as string"""
        location = self.msgDir + msgName
        with open(location, "r") as file:
            msg = file.read()
        return msg

    def isAction(self, request):
        """Check if request is action"""
        if (("&" in request) or ("()" in request)):
            return True
        else:
            return False

class Action(Message):
    """Parse action messages"""
    def __init__(self, request, msgDir):
        self.request = request
        self.msgDir = msgDir

    def randSel(self):
        """Select random message according to request"""
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

    def processAction(self):
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

class Reply(Action):
    """Precess user input and reply appropriately"""
    def __init__(self, msgDir, key, input):
        self.key = key
        request = self.analyzeMessage(input)
        super().__init__(userID, msgDir, request)

    def analyzeMessage(self, input):
        """Analyze user message and return most likely request"""
        clean = tools.cleanInput(input)
        words = clean.splitlines()
        weight = {}
        for word in words:
            if word in self.key:
                request = self.key.get(text)
        #  for loop, go through each word in input
        # see if that word matches any in text
        # see which one shows up the most
        # create a new dictionaries  with the totals
        # if dictionary empty
        self.request = None

    def loadMsg(self):
        """Selects the appropriate message and returns as a string"""
        if self.request is None:
            return self.open("unknownCommand"), st.default
        elif self.action(self.request): #
            action = Action(request, self.msgDir)
            return action.process()
        else:
            return self.open(self.request), st.default
