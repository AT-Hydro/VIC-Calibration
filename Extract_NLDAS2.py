import glob
import os
import pandas as pd
import geopandas as gpd
from exactextract import exact_extract
import xarray as xr
import time
import gc
import sys
import copy

idx = int(sys.argv[1])
#idx = 0



# NLDAS_files_pattern =  os.path.join("/mh1/Atakallou/VIC/Forcing/NLDAS",  "*", "*.grb.SUB.nc4")
# NLDAS_files  = glob.glob(NLDAS_files_pattern)
# NLDAS_files.sort()
def timestr(f):
    year  = f.split("A")[5][:4]
    month = f.split("A")[5][4:6]
    day   = f.split("A")[5][6:8]
    hour  = f.split("A")[5].split(".")[1][:2]
    minute= f.split("A")[5].split(".")[1][2:4]
    dt = pd.to_datetime(f"{year}-{month}-{day} {hour}:{minute}")
    return dt 
# year = 1
# NLDAS_files = NLDAS_files[(year - 1) * 8195: year * 8195]

def chunk_list(lst, n):
    """Yield successive n-sized chunks from a list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
def allocate(files, gaugeid, year):
    
    gauges = pd.read_csv("gauges.csv")
    Hourly_df = pd.read_csv(f"Gauges_Forcings/{gaugeid}_{year}.csv")
    Hourly_df["time"] = pd.to_datetime(Hourly_df["time"])
    basin = gpd.read_file(f'./Extract_shapefiles/{gaugeid}.shp')
    
    # load basin
    basin = basin.dissolve()
    for file in files:
        ds = xr.open_dataset(file)
        ds = ds.rio.write_crs("EPSG:4326")
        #allocate the precipitation value to the prc column
        filetime = timestr(file)
        row_idx = Hourly_df[Hourly_df["time"] == filetime].index[0]
        Hourly_df.at[row_idx, "prc"]    =  exact_extract(ds["APCP"].isel(time=0),basin, ['mean'])[0]['properties']['mean']
        #allocate temperature                              
        Hourly_df.at[row_idx, "temp"]   = exact_extract(ds["TMP"].isel(time=0 , height = 0),basin, ['mean'])[0]['properties']['mean']
        #allocate U wind                                                        
        Hourly_df.at[row_idx, "Uwind"]  = exact_extract(ds["UGRD"].isel(time=0 , height_2 = 0),basin, ['mean'])[0]['properties']['mean']
        #allocate V wind                                 
        Hourly_df.at[row_idx, "Vwind"]  = exact_extract(ds["VGRD"].isel(time=0 , height_2 = 0),basin, ['mean'])[0]['properties']['mean']
        #allocate specefic Humidity                                                               
        Hourly_df.at[row_idx, "SPFH"]   = exact_extract(ds["SPFH"].isel(time=0 , height = 0),basin, ['mean'])[0]['properties']['mean']
        #allocate Pressure                                            
        Hourly_df.at[row_idx, "P"]      = exact_extract(ds["PRES"].isel(time=0),basin, ['mean'])[0]['properties']['mean']
        #allocate shortwave radiation
        Hourly_df.at[row_idx, "SWRF"]   = exact_extract(ds["DSWRF"].isel(time=0),basin, ['mean'])[0]['properties']['mean']                                                 
        #allocate longwave radiation
        Hourly_df.at[row_idx, "LWRF"]   = exact_extract(ds["DLWRF"].isel(time=0),basin, ['mean'])[0]['properties']['mean'] 
        #allocate convective fraction                                                                       
        Hourly_df.at[row_idx, "CNfrac"] = exact_extract(ds["CONVfrac"].isel(time=0),basin, ['mean'])[0]['properties']['mean'] 
        ds.close()
    Hourly_df.to_csv(f"Gauges_Forcings/{gaugeid}_{year}.csv", index = False)

    return 1

basin_id = os.listdir(os.path.join(os.getcwd(), "Gauges_Forcings"))[idx].split("_")[0]
year     = os.listdir(os.path.join(os.getcwd(), "Gauges_Forcings"))[idx].split("_")[1].split(".")[0]
integer_year = int(year) + 1979
NLDAS_files_pattern =  os.path.join("/mh1/Atakallou/VIC/Forcing/NLDAS",  "*", f"*{integer_year}*.grb.SUB.nc4")
NLDAS_files  = glob.glob(NLDAS_files_pattern)
NLDAS_files.sort()
a = allocate(NLDAS_files, basin_id, year)
print(a)