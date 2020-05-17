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
    def __init__(self, msgDir, request):
        self.msgDir = msgDir
        self.request = request

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

class Reply(Action):
    """Precess user input and reply appropriately"""
    def __init__(self, msgDir, keys, input):
        self.funcKey = keys[0]
        self.transKey = keys[1]
        request = self.analyzeMessage(input)
        super().__init__(msgDir, request)

    def checkTranslations(self, text):
        """Check for any preformed messages in translation key"""
        print('checking translations')
        words = text.splitlines()
        weights = {}
        for word in words:
            if word in self.transKey:
                print('word: ', word)
                if word in weights:
                    weights[word] += 1
                else:
                    weights[word] = 1
        print('weights: ', weights)
        if weights:
            translation = max(weights, key=weights.get)
            print('translation: ', translation)
            return translation
        else: # no message
            return None

    def analyzeMessage(self, input):
        """Analyze user message and return most likely request"""
        clean = tools.cleanInput(input)
        if clean in self.funcKey:
            return self.funcKey.get(clean)
        else:
            translation = self.checkTranslations(clean)
            if translation is True:
                return translation
            else:
                # check chatterbox
                print("chatterbox")
                return None

    def loadMsg(self):
        """Selects the appropriate message and returns as a string"""
        if self.request is None:
            return self.open("unknownCommand"), st.default
        elif self.isAction(self.request): #
            action = Action(self.msgDir, self.request)
            return action.process()
        else:
            return self.open(self.request), st.default
