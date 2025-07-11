import pandas as pd
df = pd.read_csv('data.csv')

what = df.head(1)

print(what)

print(what.shape)

print(what.size)