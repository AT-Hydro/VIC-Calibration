import glob
import os
import pandas as pd
import geopandas as gpd
from exactextract import exact_extract
import xarray as xr
import time
import sys

idx = int(sys.argv[1])
gauges = pd.read_csv("gauges.csv")
gaugeid = gauges["gauge_id"].iat[idx].astype(str).zfill(8)
basin = gpd.read_file(f'./Extract_shapefiles/{gaugeid}.shp')

# load basin
basin = basin.dissolve()
Hourly_df = pd.DataFrame()
dates = pd.date_range("01-01-1980" , "31-12-2014", freq = "h")

Hourly_df['time'] = dates
Hourly_df['prc']  = -999.00
Hourly_df["temp"] = -999.00
Hourly_df['Uwind']= -999.00
Hourly_df['Vwind']= -999.00
Hourly_df['SPFH'] = -999.00
Hourly_df['P']    = -999.00
Hourly_df['SWRF'] = -999.00
Hourly_df['LWRF'] = -999.00
Hourly_df['CNfrac'] = -999.00

NLDAS_files_pattern =  os.path.join("/mh1/Atakallou/VIC/Forcing/NLDAS",  "*", "*.grb.SUB.nc4")
NLDAS_files  = glob.glob(NLDAS_files_pattern)
NLDAS_files.sort()
def timestr(file):
    year  = file.split("A")[5][:4]
    month = file.split("A")[5][4:6]
    day   = file.split("A")[5][6:8]
    hour  = file.split("A")[5].split(".")[1][:2]
    minute= file.split("A")[5].split(".")[1][2:4]
    dt = pd.to_datetime(f"{year}-{month}-{day} {hour}:{minute}")
    return dt 
    
for file in NLDAS_files:
    # open dataset
    ds = xr.open_dataset(file)
    ds = ds.rio.write_crs("EPSG:4326")  # Use the CRS of the basin
    #allocate the precipitation value to the prc column
    filetime = timestr(file)
    #allocate precipitation
    Hourly_df.loc[Hourly_df["time"] == filetime, "prc"]   = exact_extract(ds["APCP"].isel(time=0)
                                                                    ,basin, ['mean'], output='pandas')['mean'].values[0]
    #allocate temperature
    Hourly_df.loc[Hourly_df["time"] == filetime, "temp"]  = exact_extract(ds["TMP"].isel(time=0 , height = 0)
                                                                     ,basin, ['mean'], output='pandas')['mean'].values[0]
    #allocate U wind 
    Hourly_df.loc[Hourly_df["time"] == filetime, "Uwind"] = exact_extract(ds["UGRD"].isel(time=0 , height_2 = 0)
                                                                      ,basin, ['mean'], output='pandas')['mean'].values[0]
    #allocate V wind
    Hourly_df.loc[Hourly_df["time"] == filetime, "Vwind"] = exact_extract(ds["VGRD"].isel(time=0 , height_2 = 0)
                                                                      ,basin, ['mean'], output='pandas')['mean'].values[0]
    #allocate specefic Humidity
    Hourly_df.loc[Hourly_df["time"] == filetime, "SPFH"]  = exact_extract(ds["SPFH"].isel(time=0 , height = 0)
                                                                      ,basin, ['mean'], output='pandas')['mean'].values[0]
    #allocate Pressure
    Hourly_df.loc[Hourly_df["time"] == filetime, "P"]     = exact_extract(ds["PRES"].isel(time=0)
                                                                      ,basin, ['mean'], output='pandas')['mean'].values[0]
    #allocate shortwave radiation
    Hourly_df.loc[Hourly_df["time"] == filetime, "SWRF"]  = exact_extract(ds["DSWRF"].isel(time=0)
                                                                      ,basin, ['mean'], output='pandas')['mean'].values[0] 
    #allocate longwave radiation
    Hourly_df.loc[Hourly_df["time"] == filetime, "LWRF"]  = exact_extract(ds["DLWRF"].isel(time=0)
                                                                      ,basin, ['mean'], output='pandas')['mean'].values[0] 
    #allocate convective fraction 
    Hourly_df.loc[Hourly_df["time"] == filetime, "CNfrac"]  = exact_extract(ds["CONVfrac"].isel(time=0)
                                                                      ,basin, ['mean'], output='pandas')['mean'].values[0]    
Hourly_df["gauge_id"] = gaugeid
Hourly_df.to_csv(f"./Extract_forcings/{gaugeid}.csv", index = False)