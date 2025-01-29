# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:57:15 2025

@author: atakallou
"""

import os
import geopandas as gpd
import glob
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

path_shapefiles_pattern =  os.path.join(os.getcwd(), "shapefiles" , "merge", "*nhru_simplify_100.shp")
files = glob.glob(path_shapefiles_pattern)
files.append(os.path.join(os.getcwd(), "shapefiles" , "merge", "Region_10L_nhru_.shp"))
files.sort()
gauges = []

for file in files:
    shapefile = gpd.read_file(file)
    #convert the shapefile crs to WGS84
    shapefile_wgs84 = shapefile.to_crs(epsg=4326)
    for gaugeid in gpd.read_file(file).GAGEID.unique():
        print(gaugeid)
        gauges.append(gaugeid)
         #extract each gauge shapefile and save in another folder
        output_path  =  os.path.join(os.getcwd() , "Extract_shapefiles", f"{gaugeid}.shp" )
        shapefile_wgs84[shapefile_wgs84["GAGEID"] == gaugeid].to_file(output_path)