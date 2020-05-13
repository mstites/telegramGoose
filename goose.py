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
import telepot
from telepot.loop import MessageLoop
import pprint as pp

# create bot
goose = telepot.Bot('1165408473:AAFbR7nslY9WPWAx5H3AcOk5Klrf3-9Lp5E')
goose.getMe()


def handle(msg):
    """Handles message sent to goose bot and replies."""
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        if
        goose.sendMessage(chat_id, msg['text'])

MessageLoop(goose, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
