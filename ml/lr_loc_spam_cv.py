import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_validate

df = pd.read_csv("../training/final_data_with_spam_interpolated.csv")

X = df[[
    "HarvestYear",
    "MWMT", "MCMT", "MAT", "MAP",
    "Potassium_g_kg_0-20_m", "Nitrogen_g_kg_0-20_m",
    "Phosphorus_g_kg_0-20_m", "OrganicCarbon_g_kg_0-20_m",
    'interpolated_irr', 'Lat', 'Lon'
]]

y = df["YieldTonHa"]

lr = LinearRegression()

cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_validate(
    lr,
    X,
    y,
    cv=cv,
    scoring={
        "r2": "r2",
        "rmse": "neg_root_mean_squared_error"
    },
    n_jobs=4
)

print("Mean R²:", scores["test_r2"].mean())
print("Std R²:", scores["test_r2"].std())
print("Mean RMSE:", -scores["test_rmse"].mean())
print("Std RMSE:", scores["test_rmse"].std())