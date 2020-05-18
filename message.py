import tools
import os
import random
import state as st

class Message:
    def __init__(self, msgDir, request):
        self.msgDir = msgDir # default msgDir
        self.request = request

    def open(self):
        """Load message from assets and return as string"""
        location = self.msgDir + self.request
        if os.path.exists(location) is False:
            print('ERROR: Message path does not exist')
            return "I could not find the message :("
        if os.path.isdir(location):
            # get file location
            location = self.randSel()
        with open(location, "r") as file:
            return file.read()

    def randSel(self):
        """Select random message according to message directory"""
        messages = os.listdir(self.msgDir + self.request)
        sel = random.randrange(len(messages))
        fileLoc = self.msgDir + self.request + '/' + str(sel)
        return fileLoc

    def isAction(self):
        """Check if request is action"""
        if (("&" in self.request) or ("()" in self.request)):
            return True
        else:
            return False

class Action(Message):
    """Parse action messages"""
    def __init__(self, msgDir, request):
        self.msgDir = msgDir
        self.request = request

    def funcSelector(self):
        """Select function by changing state"""
        if self.request == "sendMessage()":
            state = st.sendMessage
        elif self.request == "cancelMessage()":
            state = st.cancelMessage
        elif self.request == "checkIn()":
            state = st.checkIn
        else:
            state = st.default
        return state

    def process(self):
        """Determine action type and run appropriate function"""
        if "()" in self.request:
            self.msg = self.open()
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
        words = text.split() # how does this handle /n
        # should have a way to clean that does not clean spaces
        searched = []
        matches = {}
        while words:
            word = words[0]
            if ((word in self.transKey) and (word not in searched)):
                wordOutputs = self.transKey[word]
                for output in wordOutputs:
                    if output in matches:
                        matches[output] += 1
                    else:
                        matches[output] = 1
                searched = word # word has been searched
            else: # next word
                del words[0]
                searched = []
        if matches:
            translation = max(matches, key=matches.get)
            tmatch = matches[translation]
            print('translation: ', translation, tmatch)
            if tmatch > 1:
                return translation
            else: # too low likelines
                return None
        # if translation has low probablity, eg only one or two word match, return None
        else: # no message
            return None

    def analyzeMessage(self, input):
        """Analyze user message and return most likely request"""
        clean = tools.cleanInput(input)
        if clean in self.funcKey:
            return self.funcKey.get(clean)
        else:
            translation = self.checkTranslations(input)
            if translation is not None:
                return translation
            else:
                # check chatterbox
                print("chatterbox")
                return None

    def loadMsg(self):
        """Selects the appropriate message and returns as a string"""
        if self.request is None:
            self.request = "unknownCommand"
            return self.open(), st.default
        elif self.isAction(): #
            action = Action(self.msgDir, self.request)
            return action.process()
        else:
            return self.open(), st.default
