import datetime
import pandas as pd

columns = ['time', 'user', 'action', 'content']
df = pd.DataFrame(columns = columns)
t = datetime.datetime.now() + datetime.timedelta(minutes=5)
# test = Event(time, ***REMOVED***, )

row = {'time':t, 'user':***REMOVED***, 'action':'msg', 'content':'test'}
df = df.append(row, ignore_index=True)
print(df)
df.to_pickle('assets/events.pkl')
