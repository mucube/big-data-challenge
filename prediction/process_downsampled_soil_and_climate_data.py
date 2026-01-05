import pandas as pd

df = pd.read_csv("./downsampled_soil_and_climate_data_raw.csv")

df.drop('system:index', axis='columns', inplace=True)

# remove rows with no data
df = df[df['OrganicCarbon_g_kg_0-20_m'].notna() & (df['OrganicCarbon_g_kg_0-20_m'] != "")]
df = df[df['MAP_2030_ssp245'].notna() & (df['MAP_2030_ssp245'] != "")]

df['id'] = range(len(df))

df.to_csv("./downsampled_soil_and_climate_data.csv", index=False)