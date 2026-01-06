import pandas as pd
import json
from shapely.geometry import shape

df = pd.read_csv("./downsampled_soil_and_climate_data_raw.csv")

df.drop('system:index', axis='columns', inplace=True)

def geometry_string_to_wkt_and_centroid(s: str) -> str:
    if not isinstance(s, str) or not s.strip():
        return None

    # Remove surrounding parentheses if present
    s_clean = s.strip()
    if s_clean.startswith("(") and s_clean.endswith(")"):
        s_clean = s_clean[1:-1]

    # Replace JavaScript booleans with JSON booleans
    # Note: For valid JSON, lowercase true/false must be lowercase
    s_clean = s_clean.replace("false", "false").replace("true", "true")

    try:
        geojson_obj = json.loads(s_clean)
        geom = shape(geojson_obj)

        wkt = geom.wkt
        centroid = geom.centroid
        lon = centroid.x
        lat = centroid.y

        return wkt, lon, lat
    except Exception as e:
        print(f"Conversion error for string: {s}\nError: {e}")
        return None

# remove rows with no data
df = df[df['OrganicCarbon_g_kg_0-20_m'].notna() & (df['OrganicCarbon_g_kg_0-20_m'] != "")]
df = df[df['MAP_2030_ssp245'].notna() & (df['MAP_2030_ssp245'] != "") & (df['MAP_2030_ssp245'] != 0.0)]

results = df['.geo'].apply(geometry_string_to_wkt_and_centroid)

df["wkt"] = results.apply(lambda x: x[0])
df["CentroidLon"] = results.apply(lambda x: x[1])
df["CemtroidLat"] = results.apply(lambda x: x[2])

df.drop(columns=['.geo'], inplace=True)
df['id'] = range(len(df))

df.to_csv("./downsampled_soil_and_climate_data.csv", index=False)