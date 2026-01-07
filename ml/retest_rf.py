import pickle

with open("lr_cv.pkl", "rb") as f:
    search = pickle.load(f)

#best_model = search.best_estimator_

best_params = search.best_params_

best_score = search.best_score_

print(best_score)
print(best_params)