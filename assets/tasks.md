To do:
1. Update run.py structure: Handler class, reply and event handlers. Create main loop outside of classes
2. Logging class, store errors
3. Image events (when one is sent, schedule the next)
4. More advanced message recognition system
5. How are you doing?

Expansion content:
* Random honks
* Pets
* Fun facts (bi)
* Send positivity
* Reminder system
* Disable adding to groups

Other:
* Explain folder structure (keys)
* logs -> store all the variable changes as txt
* Add ability to take commands (eg: reboot, load events) -> take user input in loop
* Handeling mispellings
* Disable adding to groups

Reminder system:
weeks, get number before
month, get number before
day, get number before
day of week, get time between

print back reminder time

Message recognition system:
* One that matches most keywords
* Create new version that inherits from Message
* Then just use the msgopen from message to open

python-telegram-bot change over process:
* Initialize bot with token -> telegram.Bot(token)
* Read messages
* Get message, userID
* send message -> bot.send_message(id, text)
  * send_photo
  * send_document
  * send_audio
  * send_sticker
  * send_video
