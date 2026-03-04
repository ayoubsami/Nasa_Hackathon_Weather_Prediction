import pandas as pd
import os
from sklearn.cluster import KMeans
import numpy as np
import joblib


final_cols = [
    "lon", "lat", "day", "hour",
    "is_night", "is_day", "hour_sin", "hour_cos",
    "dist_center",  "radius",   "angle", "lat_bin", "lon_bin", "geo_cluster",
    "cluster_hour", "dist_hour_interaction",
    "temp", "wind", "precip",
]
data = pd.DataFrame(columns=final_cols)




for i in range(2000, 2025):
    df = pd.read_csv(f"data/merged_data_{i}.csv", parse_dates=['time'])

    # Extract year and day
    df['year'] = df['time'].dt.year
    df['day'] = df['time'].dt.day  # or df['time'].dt.day if you prefer calendar day
    df['hour'] = df['time'].dt.hour

    # Rename columns
    df = df.rename(columns={
        "T2M_C": "temp",
        "wind_speed": "wind",
        "PRECTOT": "precip"
    })

    df["is_night"] = df["hour"].isin([21, 22, 23, 0,1,2,3,4,5]).astype(int)
    df["is_day"] = df["hour"].isin([11, 12, 13, 14, 15, 16]).astype(int)


    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)


    center_lat = df["lat"].astype("float64").mean()
    center_lon = df["lon"].astype("float64").mean()
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # km
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        dphi = np.radians(lat2 - lat1)
        dlambda = np.radians(lon2 - lon1)
        a = np.sin(dphi/2)**2 +  np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
        return 2 * R * np.arcsin(np.sqrt(a))

    df["dist_center"] = haversine(df["lat"], df["lon"], center_lat, center_lon)


    df["radius"] = np.sqrt(df["lat"]**2 + df["lon"]**2)
    df["angle"] = np.arctan2(df["lat"], df["lon"])

    df["lat_bin"] = (df["lat"] * 100).astype(int)
    df["lon_bin"] = (df["lon"] * 100).astype(int)

    ## Spatial Clustering (Very Powerful)
    kmeans = KMeans(n_clusters=20, random_state=42)
    df["geo_cluster"] = kmeans.fit_predict(df[["lat","lon"]])


    df["cluster_hour"] = df["geo_cluster"]*24 + df["hour"]

    df["dist_hour_interaction"] = df["dist_center"] * df["hour_sin"]




    df_final = df[final_cols]

    df_final = df_final.sort_values(["lon", "lat", "day", "hour"])
    
    for col in df_final.select_dtypes('float'):
      df_final[col] = df_final[col].astype('float16')

    for col in df_final.select_dtypes('int'):
      df_final[col] = df_final[col].astype('int8')

    if i == 2000:
        data = df_final.copy()
    else:
        data = pd.concat([data, df_final], ignore_index=True)
    print(i, "is done!")

joblib.dump(kmeans, "kmeans_feature.pkl")

data.to_csv("data.csv", index=False)