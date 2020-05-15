# Telegram Goose
A bot to keep me busy during quarantine and give my girlfriend and I some laughs.

## Requirements:
* telegram-send
* group called "jenni.conf", create with the bash command "telegram-send --config jenni-.conf --configure"

## Ideas
* Could make more generic, have a translation table from command to thing to load in a text file or a spreadsheet

Make requirements.txt

Way to check if selected message contains () - a function


Trans support bot:
"Misgendered by professors"
* Do you need help writing a letter to a professor


user folder structure:
ID/
mailbox: any items for mail, targetted by date
mailTaget: id to send mail to
msgCount: number of messages

assets folder structur:
messages: message txt files
* init: initial messages (~key is the item that contains aliases)
* replies: replying messages (~key contains aliases)
Sort through:
#!/usr/bin/env python
# coding: utf-8

# ## Good Morning

# if time is 8:00 am:
# good morning jenni.
#
# if last named message document (in 00/00/0000 format) > 24 hours ago:
# I don"t have any unique messages to deliver today, but here is a cute cat photo!
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

# could select random message by having multiple reply files for each one (ending 1-3)

# inefficient to reconsttruct key everytime, though this does allow live updates
# daily message -> use [] to embed a link to an online image to get in
# delay message
# goodbye

# way to get name and use that in addition to ID, that way for sending messages you can see names
# could also just have property for user on who to send messages to


# Reminders:
# Dictionary with keys being reminder time and values being message to send
# Have another dictionary with keys being date and values being dictionary with times for that days
# Store in user/#/reminders, have a file caled time?

# similar type but with messages

# cute aggression generation, random times for honks

# when asking for positivity, give photo or message. Less command like
# if you cannot directly request

# add message contains capabilities, instead of just is

# how are you doing?
# I can't offer too much. But have a nuzzle and a cat photo
# that is great! what is making it so good!

# daily mail can just be one big file

# should add instructions on how to change things
# or could make everything in one central document

# get rid of txt?
