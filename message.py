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
            action = Action(request, self.msgDir)
            return action.process()
        else:
            return self.open(self.msgDir + request), st.default

class Action(Message):
    """Parse action messages"""
    def __init__(self, request, msgDir):
        """request: requset starting
        userID: id of messege originator"""
        self.request = request
        self.msgDir = 'assets/messages/' + msgDir

    def randSel(self):
        """Select random message in request category"""
        dir = self.msgDir+self.request
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
