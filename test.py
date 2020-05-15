import datetime
import pandas as pd

columns = ['time', 'user', 'action', 'content']
df = pd.DataFrame(columns = columns)

# df = pd.read_pickle('assets/events.pkl')
t = datetime.datetime.now() + datetime.timedelta(minutes=1)
# test = Event(time, ***REMOVED***, )

row = {'time':t, 'user':1, 'action':'msg', 'content':'test'}
row2 = {'time':t+datetime.timedelta(minutes=2), 'user':1, 'action':'msg', 'content':'test'}
row3 = {'time':t+datetime.timedelta(minutes=4), 'user':2, 'action':'msg', 'content':'test'}
row4 = {'time':t+datetime.timedelta(minutes=8), 'user':3, 'action':'msg', 'content':'test'}
df = df.append(row, ignore_index=True)
df = df.append(row2, ignore_index=True)
df = df.append(row3, ignore_index=True)
df = df.append(row4, ignore_index=True)
df = df.reset_index(drop = True)

df = df.query('user == 1')
print(df)
