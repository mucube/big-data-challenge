import ee
import pandas as pd
import eemont
import geemap
from functools import reduce

ee.Authenticate()
ee.Initialize(project="data-481404")

k_image = ee.Image("ISDASOIL/Africa/v1/potassium_extractable")
p_image = ee.Image("ISDASOIL/Africa/v1/phosphorus_extractable")
n_image = ee.Image("ISDASOIL/Africa/v1/nitrogen_total")
soc_image = ee.Image("ISDASOIL/Africa/v1/carbon_organic")

df = pd.read_csv("./generated_data.csv")

chunk_size = 200
dfs = []
for start in range(0, len(df), chunk_size):
    chunk_df = df.iloc[start:start + chunk_size]
    fc = chunk_df.toEEFeatureCollection(latitude = 'Lat',longitude = 'Lon') #eemont feature
    fc_k_point_samp = k_image.sampleRegions(collection=fc, scale=10)
    fc_p_point_samp = p_image.sampleRegions(collection=fc, scale=10)
    fc_n_point_samp = n_image.sampleRegions(collection=fc, scale=10)
    fc_soc_point_samp = soc_image.sampleRegions(collection=fc, scale=10)
    
    k_df = geemap.ee_to_df(fc_k_point_samp)
    p_df = geemap.ee_to_df(fc_p_point_samp)
    n_df = geemap.ee_to_df(fc_n_point_samp)
    soc_df = geemap.ee_to_df(fc_soc_point_samp)

    k_df = k_df[['id', 'mean_0_20']]
    p_df = p_df[['id', 'mean_0_20']]
    n_df = n_df[['id', 'mean_0_20']]
    soc_df = soc_df[['id', 'mean_0_20']]

    k_df.rename(columns={'mean_0_20': 'Potassium_g_kg_0-20_m'}, inplace=True)
    n_df.rename(columns={'mean_0_20': 'Nitrogen_g_kg_0-20_m'}, inplace=True)
    p_df.rename(columns={'mean_0_20': 'Phosphorus_g_kg_0-20_m'}, inplace=True)
    soc_df.rename(columns={'mean_0_20': 'OrganicCarbon_g_kg_0-20_m'}, inplace=True)

    dfs_to_merge = [k_df, n_df, p_df, soc_df]
    merged_df = reduce(lambda left, right: pd.merge(left, right, on='id', how='outer'), dfs_to_merge)
    dfs.append(merged_df)

df_with_climate = pd.read_csv("./data_with_climate.csv")

final_df = pd.concat(merged_df, ignore_index=True)
final_df = pd.merge(final_df, df_with_climate, on='id', how='inner')
final_df.to_csv("final_data.py")