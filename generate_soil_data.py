import pandas as pd
from dotenv import load_dotenv
import os
import requests

load_dotenv(override=True)

input_df = pd.read_csv("./generated_data.csv")

new_rows = []

api_username = os.getenv("USERNAME")
api_password = os.getenv("PASSWORD")

base_url = "https://api.isda-africa.com"

# first call the login endpoint to get the access token. Token expiry: 60 mins
payload = {"username": api_username, "password": api_password}
response = requests.post(f"{base_url}/login", data=payload)
access_token = response.json().get("access_token")

soil_properties = [
    "carbon_organic",
    "phosphorous_extractable",
    "nitrogen_total",
    "potassium_extractable",
    "ph"
]

failed_rows = []

def get_soil_property(lat, lon, soil_property):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"lon": lon, "lat": lat, "depth": "0-20", "property": soil_property}
    response = requests.get(f"{base_url}/isdasoil/v2/soilproperty", params=params, headers=headers)
    return response.json()["property"][soil_property][0]["value"]["value"]

for index, row in input_df.iterrows():
    new_row = {'id': row['id'], 'Lat': row['Lat'], 'Lon': row['Lon']}
    print("a")
    for soil_property in soil_properties:
        try:
            get_soil_property(row['Lat'], row['Lon'], soil_property)
        except:
            failed_rows.append({'id': row['id'], 'Lat': row['Lat'], 'Lon': row['Lon'], 'SoilProperty': soil_property})

    new_rows.append(new_row)

output_df = pd.concat(new_rows)

output_df.to_csv("soil_data.csv", index=False)

pd.concat(failed_rows).to_csv("failed_rows_soil.csv", index=False)