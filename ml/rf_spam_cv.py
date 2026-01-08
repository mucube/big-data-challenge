import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from sklearn.experimental import enable_halving_search_cv #needed
from sklearn.model_selection import HalvingGridSearchCV

import pickle

df = pd.read_csv("../training/final_data_with_spam_interpolated.csv")

X = df[[
    "HarvestYear",
    "MWMT", "MCMT", "MAT", "MAP",
    "Potassium_g_kg_0-20_m", "Nitrogen_g_kg_0-20_m",
    "Phosphorus_g_kg_0-20_m", "OrganicCarbon_g_kg_0-20_m",
    'interpolated_irr'
]]

y = df["YieldTonHa"]

rf = RandomForestRegressor(random_state=0)

cv_params = {'max_depth': [None, 10, 20], 
             'min_samples_leaf': [1,2,3],
             'min_samples_split': [2,5,10],
             'max_features': ["sqrt", "log2", None],
             'n_estimators': [200, 300, 400]
             }

cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

rf_cv = HalvingGridSearchCV(estimator=rf, param_grid=cv_params, scoring='r2', cv=cv, n_jobs=4, factor=3, verbose=1)

rf_cv.fit(X,y)

with open("rf_spam_cv.pkl", "wb") as f:
    pickle.dump(rf_cv, f)