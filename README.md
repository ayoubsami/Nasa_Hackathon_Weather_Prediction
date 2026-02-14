

# Nasa Hackathon Weather Prediction



## Table of contents

* [Getting Data](#Getting-Data)
* [Merging and Cleaning Data](#Merging-and-Cleaning-Data)



----
### Getting Data:

In this project we couldn't use any data we want, we had to use data from a specific list of platforms (if this wasn't the case, we could use more specific data of a small area (city metropolis) 
and it would give us more specific prediction). the NASA owned Eartdata platform was the best option we had,so we used it.
In the platform we extracted 4 variables:

    U50M (eastward_wind_at_50_meters) from MERRA-2 code: M2T1NXSLV
    V50M (northward_wind_at_50_meters) from MERRA-2 code: M2T1NXSLV
    T2M (2-meter_air_temperature) from MERRA-2 code: M2T1NXSLV
    PRECTOT (total_precipitation) from MERRA-2 code: M2T1NXFLX

The task of downloading files, choosing these 4 variables and converting each file from .nc4 to .csv (NetCDF-4 files are multi-dimentioanl and for this project we only need 2, plus 
csv files are easier to work with in python) is automated in the file auto.py. we choose to only work on the area of Morocco (-18, 20, 0, 36) instead of the world and the area is 
specified in the variable "bbox", so what's happening each time is:
  +  We choose the day we want, we access earthdata database directly using earthdata python modul, we download 2 granules (granule in Nasa terms is a set of data usually in
one day in one file ) one is M2T1NXSLV and the other is M2T1NXFLX.
  +  The two .nc4 files are parsed using xarray python model.
  +  We extract the 4 variables.
  +  We calculate windspeed variable using U50M and V50M.
  +  We convert the tempature to °c.
  +  We define lat (Latitude) and lon (Longitude) variables, so that every spot/pixel can have PRECTOT, T2M and windspeed.
  +  We extract the whole info into a csv file.

------
### Merging and Cleaning Data
