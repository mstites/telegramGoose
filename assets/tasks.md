To do:
1. Implement events spreadsheet for adding new events (this could later be expanded to include the keys and such)
2. Automatted load in of eventsMessages
1. Image events (when one is sent, schedule the next)
2. More advanced message recognition system
3. How are you doing?
4. Change events df to have attributes column. This way can add tags (eg: recurring (with time period), caption: CONTENT, random selection, from bot: T/F (to remove isBotMsg)) - this could be dictionary
5. Change from isGooseImg to if recurring, random selection

Expansion content:
* Random honks
* Pets
* Fun facts (bi)
* Send positivity
* Send messages w/ images -> need a way to parse images seperately from text? can the text just be made into a seperate item?
* Reminder system

Other:
* Amazon echo like: https://opensource.com/article/16/11/open-source-amazon-echo-projects
* Custom sticker pack
* Be able to send more than just text -> delay this goal

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

Reorganizingc code:
* Update classes
* Check events function
* msgkey class

events.py:
* New eventDf class. contains: readData, sortSave, removeEvent, addEvent
* EventHandler inherents from eventDF, eventDF inherits froom DF
* Move runEvent out of this class, this shoould be done in update. Call isEvent(), which returns a bool (build from checkTimeEvent). If it is True, run the next event and remove it from the dataframe - this should all be done in update

* Should be able to have reply handler object that handles having reply key throughout


eventManager
controller
supervisor


msgManager(pass dictionaries, reply method)

### Log
* Pass logging to all classes? Make global?
* log = Global logging
* Use debug for in between var names (EG msg, events)
* Use info for major var names (EG df and msg when updated)
* Use error for else statements  catches in places that should get caught in if or elif (stateHandler, msg, eventHandlerO)

Notes:
* Contain Time, name
* Could just make global basicConfig, will need to load into variables
* min level is the minimum
* logging.debug('This is a debug message')
* logging.info('This is an info message')
* logging.warning('This is a warning message')
* logging.error('This is an error message')
* logging.critical('This is a critical message')
