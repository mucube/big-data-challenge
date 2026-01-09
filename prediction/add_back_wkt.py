import pandas as pd

df1 = pd.read_csv("output.csv")
df2 = pd.read_csv("downsampled_soil_and_climate_data.csv")

newrows = []

for index, row in df1.iterrows():
    id = row['id']
    row2 = df2.loc[df2['id'] == id, 'wkt'].item()
    row['wkt'] = row2
    newrows.append(row)

newdf = pd.DataFrame(newrows)

newdf.to_csv("output.csv", index=False)