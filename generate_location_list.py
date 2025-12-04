# Generate location list used by ClimateAF application
import pandas as pd

df = pd.read_csv("generated_data.csv")
df = df[["Lat", "Lon"]]
df.to_csv("location_list.txt", index=False, header=False)