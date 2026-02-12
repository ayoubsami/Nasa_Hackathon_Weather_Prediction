
import os
import glob
import xarray as xr
import numpy as np
import pandas as pd
import earthaccess
from pathlib import Path

def clean_data_folder(out_dir="./data"):
    data_path = Path(out_dir)
    if not data_path.exists():
        print(f"{out_dir} does not exist.")
        return

    for file_ext in ("*.nc4", "*.csv"):
        for file in data_path.glob(file_ext):
            try:
                file.unlink()  # deletes the file
                print(f"Deleted {file}")
            except Exception as e:
                print(f"Could not delete {file}: {e}")

def download_data(short_name, start, end, bbox, out_dir="./data"):
    
    os.makedirs(out_dir, exist_ok=True)

    auth = earthaccess.login(strategy="environment")
    
    print("Authenticated:", auth.authenticated)


    granules = earthaccess.search_data(
        short_name=short_name,
        temporal=(start, end),
        bounding_box=bbox
    )


    earthaccess.download(granules, out_dir)
    all_files = glob.glob(os.path.join(out_dir, "*.nc4"))
    print("All files:", all_files)

    # filter only for the dataset
    if "SLV" in short_name.upper():
        return [f for f in all_files if "slv_Nx" in f]
    if "FLX" in short_name.upper():
        return [f for f in all_files if "flx_Nx" in f]
    return all_files

def slicing(files_slv, files_flx, out_csv="subset.csv"):
    
    print("\n\n\n")
    print("SLV files:", files_slv[0])
    print("FLX files:", files_flx[0])
    ds = xr.open_dataset(files_slv[0])
    ds2 = xr.open_dataset(files_flx[0])
    print(ds2.data_vars)
    print(ds.data_vars)

    ds, ds2 = xr.align(ds, ds2, join="inner")

    t2m = ds["T2M"]
    u50m = ds["U50M"]
    v50m = ds["V50M"]
    pre = ds2["PRECTOT"]



    windspeed = np.sqrt(u50m**2 + v50m**2)


    merged = xr.merge([t2m, u50m, v50m, windspeed.rename("wind_speed"), pre])

    subset = merged.sel(
        lat=slice(20.90484, 36.45832),   # ascending
        lon=slice(-18.64305, 0.04817)
    )


    df = subset.to_dataframe().reset_index()
    df["T2M_C"] = df["T2M"] - 273.15  # Kelvin → Celsius

   
    df = df[["time", "lon","lat","T2M_C","wind_speed","PRECTOT"]]
    df.to_csv(out_csv, index=False)
    print(f"Saved {len(df)} rows to {out_csv}")

    return df


if __name__ == "__main__":

    bbox = (-18, 20, 0, 36) 

    for i in range(21, 25):
        for j in range(1,6):
            time = f"{2000+i}-10-{j:02d}" 
            files_slv = download_data("M2T1NXSLV", time,time, bbox)
            files_flx = download_data("M2T1NXFLX", time,time, bbox)
            slicing(files_slv, files_flx, out_csv=f"data_{time}.csv")
            print(f"{time} is done!")
            clean_data_folder("./data")

