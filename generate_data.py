import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

survey_df = pd.read_excel("./GROW-Africa-Database/GROW-Africa_LSMS_survey.xlsx")
point_df = pd.read_excel("./GROW-Africa-Database/GROW-Africa_Point.xlsx")
cropcut_df = pd.read_excel("./GROW-Africa-Database/GROW-Africa_LSMS_cropcut.xlsx")

# filter to only include maize
survey_df = survey_df[survey_df["Crop"] == "Maize"]
point_df = point_df[point_df["Crop"] == "Maize"]
cropcut_df = cropcut_df[cropcut_df["Crop"] == "Maize"]

l0_gdf = gpd.read_file("./GROW-Africa-Database/Shapefiles/GADM_level0_ECG.shp")

# check if given coordinates lies inside the given country
def validate_lat_lon(lat, lon, l0_gid):
    row = l0_gdf[l0_gdf['GID'] == l0_gid]
    country_polygon = row.geometry.iloc[0]
    return country_polygon.covers(Point(lon, lat))

# '[]' needs to be counted as nan because of two stupid entries from uganda
def isna(x):
    if x == '[]':
        return True
    else:
        return pd.isna(x)

def read_survey_df():
    new_df = pd.DataFrame(columns=["Lat", "Lon", "HarvestYear", "Source", "YieldTonHa"])

    for index, row in survey_df.iterrows():
        if not isna(row["YieldUsingGPS_ton_ha_"]):
            yield_ton_ha = row["YieldUsingGPS_ton_ha_"]
        elif not isna(row["Yield_ton_ha_"]):
            yield_ton_ha = row["Yield_ton_ha_"]
        elif not isna(row["YieldEst2UsingGPS_ton_ha_"]):
            yield_ton_ha = row["YieldEst2UsingGPS_ton_ha_"]
        elif not isna(row["YieldEst2_ton_ha_"]):
            yield_ton_ha = row["YieldEst2_ton_ha_"]
        
        # if there is no lat/lon given, use the center of the lowest-level administrative division given
        if not isna(row["GPS_lat"]) and not isna(row["GPS_lon"]) and validate_lat_lon(row["GPS_lat"], row["GPS_lon"], row["L0_GID"]):
            lat = row["GPS_lat"]
            lon = row["GPS_lon"]
        else:
            continue

        new_row = pd.DataFrame([{"Lat": lat,
                                "Lon": lon,
                                "HarvestYear": row["AgYearEnd"],
                                "Source": row["Source"],
                                "YieldTonHa": yield_ton_ha,
                                }])
        new_df = pd.concat([new_df, new_row], ignore_index=True)
    return new_df

def read_point_df():
    new_df = pd.DataFrame(columns=["Lat", "Lon", "HarvestYear", "Source", "YieldTonHa"])

    for index, row in point_df.iterrows():
        # CEEPA_time_avg data points are averages over multiple years, so we don't want them
        if row["Source"] == "CEEPA_time_avg":
            continue

        # if there is no lat/lon given, use the center of the lowest-level administrative division given
        if not isna(row["Latitude"]) and not isna(row["Longitude"]) and validate_lat_lon(row["Latitude"], row["Longitude"], row["L0_GID"]):
            lat = row["Latitude"]
            lon = row["Longitude"]
        else:
            continue
        
        new_row = pd.DataFrame([{"Lat": lat,
                                "Lon": lon,
                                "HarvestYear": row["HarvestYear"],
                                "Source": row["Source"],
                                "YieldTonHa": row["Yield_ton_ha_"],
                                }])
        new_df = pd.concat([new_df, new_row], ignore_index=True)
    return new_df

def read_cropcut_df():
    new_df = pd.DataFrame(columns=["Lat", "Lon", "HarvestYear", "Source", "YieldTonHa"])

    for index, row in cropcut_df.iterrows():
        new_row = pd.DataFrame([{"Lat": row["GPS_lat"],
                                "Lon": row["GPS_lon"],
                                "HarvestYear": row["Year"],
                                "Source": row["Source"],
                                "YieldTonHa": row["Yield_ton_ha_"]}])
        new_df = pd.concat([new_df, new_row], ignore_index=True)
    return new_df


generated_df = pd.concat([read_survey_df(), read_point_df(), read_cropcut_df()], ignore_index=True)

# give each data entry an id
generated_df = generated_df.rename_axis("id").reset_index()

# make sure year column is an integer
generated_df["HarvestYear"] = generated_df["HarvestYear"].astype(int)

generated_df.to_csv("generated_data.csv", index=False)