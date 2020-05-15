import pandas as pd
import datetime

utc = datetime.datetime.now()
columns = ['time', 'user', 'action', 'content']
df = pd.DataFrame(columns = columns)

#
# row1 = {'time':utc, 'user':123, 'action':'msg', 'content':'hello world'}
# row2 = {'time':utc - datetime.timedelta(days=10), 'user':1, 'action':'msg', 'content':'hello world'}
#
# df = df.append(row1, ignore_index=True)
# df = df.append(row2, ignore_index=True)
# df = df.sort_values(by='time')
# df = df.reset_index()
print(df)
#
df.to_pickle('assets/events.pkl')
#
# nextEvent = df.iloc[0]['time']
# print(nextEvent)
#
# event = df.iloc[0]
# test = event['action']
# print(test)
# print(type(test))
# # sort by timestamp
#
# df = df.drop(0)
# print(df)
