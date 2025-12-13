# split data based on year to input into ClimateAF
import pandas as pd

df = pd.read_csv("generated_data.csv")

df.insert(1, 'placeholder1', '.')
df['placeholder2'] = '.'
df.drop(columns=["Source", "YieldTonHa"], inplace=True)

unique_years = df['HarvestYear'].unique()
for year in unique_years:
    annual_df = df[df['HarvestYear'] == year]
    annual_df.to_csv(f'./annual_entries/{year}.csv', index=False)