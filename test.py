import datetime
import pandas as pd

columns = ['time', 'user', 'action', 'content']
df = pd.DataFrame(columns = columns)
df.to_pickle('assets/events.pkl')
