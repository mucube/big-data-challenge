import pandas as pd

df = pd.read_csv("./generated_data.csv")

variables = [
    "MWMT",
    "MCMT",
    "MAP"
]

rows = []

for index, row in df.iterrows():
    id = row['id']
    year = row['HarvestYear']
    if year > 2020 or year < 2000:
        continue
    climate_df = pd.read_csv(f'./annual_climate/{year}.csv')
    climate_row = climate_df.loc[climate_df["id"] == id].iloc[0]
    for variable in variables:
        row[variable] = climate_row[variable]
    rows.append(row)

new_df = pd.DataFrame(rows)

new_df.to_csv("data_with_climate.csv", index=False)