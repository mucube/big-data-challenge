import pandas as pd
import pickle

with open("../ml/rf_loc_cv.pkl", "rb") as f:
    search = pickle.load(f)

model = search.best_estimator_
df = pd.read_csv("input2.csv")

new_rows = []

for index, row in df.iterrows():
    new_row = pd.Series()
    new_row['id'] = row['id']
    for ssp in ['ssp245','ssp585']:
        for year in [2030, 2040, 2050]:
            var_str = f'{year}_{ssp}'
            X = pd.DataFrame([{
                "HarvestYear": year,
                "MWMT": row['MWMT_'+var_str],
                "MCMT": row['MCMT_'+var_str],
                "MAT": row['MAT_'+var_str],
                "MAP": row['MAP_'+var_str],
                "Potassium_g_kg_0-20_m": row["Potassium_g_kg_0-20_m"],
                "Nitrogen_g_kg_0-20_m": row["Nitrogen_g_kg_0-20_m"],
                "Phosphorus_g_kg_0-20_m": row["Phosphorus_g_kg_0-20_m"],
                "OrganicCarbon_g_kg_0-20_m": row["OrganicCarbon_g_kg_0-20_m"],
                'Lat': row['CentroidLon'],
                'Lon': row['CentroidLat']
            }])
            new_row["PredictedYield_"+var_str] = model.predict(X)
    new_row['baseline_yield'] = row['YieldTonHa_mean']
    new_rows.append(new_row)

new_df = pd.DataFrame(new_rows)
new_df.to_csv("output.csv", index=False)