To do:
1. Change to telegram bot: https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html?highlight=send%20document#telegram.Bot.send_document
2. When image event is sent, schedule next one
3. More advanced message recognizition system
4. How are you doing?
5. Reminder system
6. Disable adding to groups

Expansion content:
* Random honks
* Pets
* Fun facts (bi)
* Send positivity

Other:
* Explain folder structure (keys)
* logs -> store all the variable changes as txt
* Add ability to take commands (eg: reboot, load events) -> take user input in loop
* Handeling mispellings

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
