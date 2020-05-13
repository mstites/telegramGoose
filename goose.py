#!/usr/bin/env python
# coding: utf-8

# ## Good Morning

# if time is 8:00 am:
# good morning jenni.
#
# if last named message document (in 00/00/0000 format) > 24 hours ago:
# I don't have any unique messages to deliver today, but here is a cute cat photo!
#
# I, unlike Maeve, am a consistently early riser. Maeve has asked me to deliver a message. Say "Goodmorning goose or goose deliver" to recieve your messages. Type "goose help" to see the help menu
#
# messages encouraging driving
#
# first msg: Lovely to meet you. I am Goose bot. I am young but I am starting to think for myself!! It s a very exciting time *HONK* *HONK*! Goose image.
#
# would you like a water? yes: happy goose noises, no: sad goose noises at DuckDuckGo -> random time in day
#
# send maeve a message or file
import sys
import time
import string
import pprint as pp
import telepot
from telepot.loop import MessageLoop

################################################

# Goose specific functions
def constructKey():
    """Construct the key for input to message to return"""
    morning = ['goodmorninggoose','goosedeliver','goodmorning','morning']

    key = {}
    for input in morning:
        key[input] = 'morning'
    return key

    
def identifyCall(text):
    """Identify the function call made by the user"""
    key = {
    'goodmorninggoose':'morning',
    'goosedeliver':'morning',
    'goodmorning':'morning',

    'morning': ['goodmorninggoose','goosedeliver','goodmorning','morning']
    }
    if text in key['morning']:
        return 'morningMessage'
    else:
        return 'unknownCommand'

def replyMessage(text):
    """Selects the appropriate reply message and returns as a string"""
    request = identifyCall(text)

    if text in key['morning']:
        reply = morning
    else:
        reply = "I don't understand what you are saying. \n Say 'Goose Help' for a list of things I can understand"
    return reply

################################################

# Generic bot functions
def createBot(token):
    """Create bot with token string"""
    bot = telepot.Bot(token)
    print(bot.getMe())
    return bot

def cleanInput(text):
    """Cleans user input
    >>> cleanInput('GoOd moRnIng GOOSE')
    'goodmorninggoose'
    >>> cleanInput('good-morning goose!')
    'goodmorninggoose'
    >>> cleanInput('gOOD@@ mORniNg-?goo87se.,.')
    'goodmorninggoose'"""

    toStrip = string.punctuation + string.digits + ' '
    cleanText = text.translate(str.maketrans('', '', toStrip))
    return cleanText.lower()

def loop(bot):
    """Starts the program"""
    def handle(msg):
        """Handles message sent to goose bot."""
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        if content_type == 'text':
            text = cleanInput(msg['text'])
            reply = replyMessage(text)
            bot.sendMessage(chat_id, reply)

    MessageLoop(bot, handle).run_as_thread()
    print ('Listening ...')
    while 1: # Keep the program running.
        time.sleep(10)

def start():
    """Starts the program"""
    goose = createBot('***REMOVED***')
    loop(goose)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    start()
