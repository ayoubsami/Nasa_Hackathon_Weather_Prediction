import joblib
import pandas as pd
import glob
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.multioutput import MultiOutputRegressor
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, huber_loss, mean_pinball_loss
import matplotlib.pyplot as plt

dataframes = pd.read_csv("data.csv")


dataframes["precip"] = np.clip(dataframes["precip"], -10, 10)

for col in dataframes.select_dtypes('float'):
  dataframes[col] = dataframes[col].astype('float16')

for col in dataframes.select_dtypes('int'):
  dataframes[col] = dataframes[col].astype('int8')
  dataframes['cluster_hour'] = dataframes['cluster_hour'].astype('int8')


dataframes.dtypes


dataframes.head()


dataframes.memory_usage(deep=True).sum() / (1024**2)



target_vars = ["temp", "wind", "precip"]
feature_vars = ["lon", "lat", "day", "is_night", "is_day", "hour_sin", "hour_cos",
                "dist_center",  "radius",   "angle", "lat_bin", "lon_bin", "geo_cluster",
                "cluster_hour", "dist_hour_interaction"]
x = dataframes[feature_vars]
y = dataframes[target_vars]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.1, random_state=42
)



base = lgb.LGBMRegressor(
    n_estimators=5000,
    learning_rate=0.05,
    num_leaves=64,
    subsample=0.8,
    colsample_bytree=0.8,
    n_jobs=-1,
    random_state=42
)

model = MultiOutputRegressor(base, n_jobs=-1)
model.fit(x_train, y_train)

print("Model training complete.")

joblib.dump(model, "multi_lgbm_newest.pkl")


# This snipet extract and shows a tree from the model
estimator = model.estimators_[0]
booster = estimator.booster_
lgb.plot_tree(booster, tree_index=4800, figsize=(200, 100))
plt.show()


y_pred = model.predict(x_test)


i = 0  # target index 0/1/2, each refers to a specific estimator
yt = y_test.iloc[:, i] if hasattr(y_test, "iloc") else y_test[:, i]
yp = y_pred[:, i]
tab = ['tempature', 'wind', 'precipatation']

plt.figure(figsize=(5,5))
plt.scatter(yt, yp, alpha=0.01)
plt.xlabel("True")
plt.ylabel("Predicted")
plt.title(f"Predicted vs True ({tab[i]})")
plt.show()


r2_score(y_test.iloc[:,2], y_pred[:,2])


lgb.plot_importance(model.estimators_[1])


mae = mean_absolute_error(y_test.iloc[:,2], y_pred[:,2])
print("MAE:", mae)
mse = mean_squared_error(y_test.iloc[:,2], y_pred[:,2])
print("MSE:", mse)


i = 2
tab = ['tempature', 'wind', 'precipatation']
residuals = y_test.iloc[:,i] - y_pred[:,i]
plt.scatter(y_pred[:,i], residuals, alpha=0.01)
plt.axhline(0)
plt.xlabel("Predicted")
plt.ylabel("Residuals")
plt.title(f"residual plot for {tab[i]}")
plt.show()


loss = huber_loss(y_test.iloc[:,0], y_pred[:,0])
print("Huber Loss:", loss)