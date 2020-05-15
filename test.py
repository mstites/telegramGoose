import datetime
import pandas as pd

columns = ['time', 'user', 'action', 'content']
df = pd.DataFrame(columns = columns)

# df = pd.read_pickle('assets/events.pkl')
t = datetime.datetime.now() + datetime.timedelta(minutes=1)
# test = Event(time, 774796474, )

row = {'time':t, 'user':774796474, 'action':'msg', 'content':'test'}
df = df.append(row, ignore_index=True)
print(df)

# df = df.reset_index()
df.to_pickle('assets/events.pkl')
