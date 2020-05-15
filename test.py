import datetime
import pandas as pd

columns = ['time', 'user', 'action', 'content']
df = pd.DataFrame(columns = columns)

# df = pd.read_pickle('assets/events.pkl')
t = datetime.datetime.now() + datetime.timedelta(minutes=1)
# test = Event(time, ***REMOVED***, )

row = {'time':t, 'user':***REMOVED***, 'action':'msg', 'content':'test'}
row2 = {'time':t+datetime.timedelta(minutes=2), 'user':***REMOVED***, 'action':'msg', 'content':'test'}
df = df.append(row, ignore_index=True)
df = df.append(row2, ignore_index=True)
df = df.reset_index(drop = True)
print(df)

nextEvent = df.iloc[0]
print(nextEvent)
df = df.drop(0)
df = df.reset_index(drop = True)
# df = df.reset_index()
# df.to_pickle('assets/events.pkl')
