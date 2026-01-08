import pandas as pd

df = pd.read_csv("test.csv")
df = df[df['NUMPOINTS'] > 5]
df.to_csv("filtered_input_data.csv", index=False)