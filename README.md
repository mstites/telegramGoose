# Telegram Goose
A soft but sometimes bastard energy bot who will never stop loving its users. It is currently capable of delivering messages between users, sending scheduled messages, and interpreting basic commands and greetings.

Currently working on improving its language capabilities. Long term goal is to expand functionality and pre-defined messages and commands to give the bot personality.

## Adding events:
### Background Information
There are three types of events you can easily add in:
1. Functions
2. Replies
3. initEvents

Functions and Replies are things that happen based on user input. In other words, they are activated when the user says something. On the other hand, events are things the bot will initiate. For example, sending the user messages at a certain time.

The key difference between functions and replies is that functions use explicit commands to run, while replies just make a best guess at what the user might want. In many cases, these actually can access the same functions, with functions just being a fool proof, more reliable way to access the functions the user may desire.

### Customizing/adding function/reply events:
Customizing or adding events is a similar process for these two types of events, there are just two major steps:
1. Modify the key file (optional if you just want to customize the sent message)
2. Add the message/messages

#### Modifying the Key File (optional)
By default, the function event key file is located at assets/messages/replies/~funcKey and the reply event key file is located at assets/messages/replies/~translationKey, these values can be changed in the "run" function of run.py.

File notation notes:
* The first value in every line is the file location
* Items on the rest of the line are keywords or inputs for that value
* "#" is a comment
* "()" is the symbol for function, if these outputs are activated, an action will be ran. Adding more functions to the bot will require python code modification, likely in the reply method in run.py

#### Modifying the messages:
To modify the messages sent, navigate to the directory/file indicated in the first value of the relevant line in the key file. Modifying this documents will change the bot's output text.

A note on folders and randomness:
Folders with the name of the output in the key file have a random message, with the random messages contained within. The messages inside these folders must be numbered starting from 0 and going up.

### Adding events:
To manually load bot initiated events into the database, you'll need to modify assets/newEvents.csv

To add an event, enter it on a new line following the example format in the file. Save the csv using ";" as a separator.

Notes:
* Content field
  * Text messages: Put the message to be sent, no semicolons allowed
  * Images: Indicate the directory or file where the image is stored
* This document will be cleared as soon as the bot is ran and the information will be stored in the pandas dataframe.
