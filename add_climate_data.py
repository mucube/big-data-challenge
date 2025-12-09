import pandas as pd

import requests

url = ('https://power.larc.nasa.gov/api/temporal/climatology/openapi').json
params = {
    "latitude": 40,
    "longitude": -75,
    "community": "ag",
    "parameters": "T2M",
    "start": 2001,
    "end": 2020,
    "format": "json",
}

response = requests.get(url, params=params).json()

Latitude = []
Longitude = []
Elevation = []
ParameterName = []
Units = []
LongName = []
Jan = []
Feb = []
Mar = []
Apr = []
May = []
Jun = []
Jul = []
Aug = []
Sep = []
Oct = []
Nov = []
Dec = []
Ann = []

Latitude.append(response["geometry"]["coordinates"][1])
Longitude.append(response["geometry"]["coordinates"][0])
Elevation.append(response["geometry"]["coordinates"][2])

for param in response["parameters"]:
    ParameterName.append(param)
    Units.append(response["parameters"][param]["units"])
    LongName.append(response["parameters"][param]["longname"])
param_key = list(response["properties"]["parameter"].keys())[0] 
values = response["properties"]["parameter"][param_key]

Jan.append(values["1"])
Feb.append(values["2"])
Mar.append(values["3"])
Apr.append(values["4"])
May.append(values["5"])
Jun.append(values["6"])
Jul.append(values["7"])
Aug.append(values["8"])
Sep.append(values["9"])
Oct.append(values["10"])
Nov.append(values["11"])
Dec.append(values["12"])
Ann.append(values["13"])


d = {"Parameter": ParameterName,"Units": Units,"LongName": LongName,"Latitude": Latitude,
    "Longitude": Longitude,"Elevation": Elevation,
    "Jan": Jan,"Feb": Feb,"Mar": Mar,"Apr": Apr,"May": May,"Jun": Jun,"Jul": Jul,"Aug": Aug,"Sep": Sep,"Oct": Oct,"Nov": Nov,"Dec": Dec, "Ann": Ann
}
df = pd.DataFrame(d)
df.to_csv("generated_data.csv", index=False)

