import pandas as pd

df1 = pd.read_csv("filtered_input_data_old.csv")
df2 = pd.read_csv("downsampled_soil_and_climate_data.csv")

ids = df1['id']

filtered = df2[df2["id"].isin(ids)]
filtered.to_csv("filtered_input_data.csv", index=False)