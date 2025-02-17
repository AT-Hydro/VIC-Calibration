# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:51:22 2025

@author: atakallou
"""



import pandas as pd 
import numpy as np
import os
import glob
import shutil



# Vegetation parameters creation

gauges = pd.read_csv("Gauges.csv")
gauges['Class'] = -999

# Strip leading and trailing spaces from 'dom_land_cover'
gauges['dom_land_cover'] = gauges['dom_land_cover'].str.strip()

# Assign classes based on land cover types
class_mapping = {
    'Evergreen Needleleaf Forest': 1,
    'Evergreen Broadleaf Forest': 2,
    'Deciduous Broadleaf Forest': 4,
    'Mixed Forests': 5,
    'Woody Savannas': 5,
    'Grasslands': 10,
    'Closed Shrublands': 8,
    'Open Shrublands': 9,
    'Croplands': 11,
    'cropland/natural vegetation mosaic' : 11,
    'Savannas' : 7,
    'Barren or Sparsely Vegetated': 9
    
}

# Map the values to the 'Class' column
gauges['Class'] = gauges['dom_land_cover'].map(class_mapping).fillna(-999)

list_folders =  os.listdir(os.path.join(os.getcwd(), "CONUS"))
for folder in list_folders:
    VEG_lib_path = os.path.join(os.getcwd(), "CONUS" ,  folder, "parameters", "basin_veglib.txt")
    if not os.path.exists(VEG_lib_path):
        shutil.copy("gauge_veglib.txt", VEG_lib_path)

gauges['root_depth_99'] = gauges.groupby('dom_land_cover')['root_depth_99'].transform(lambda x: x.fillna(x.mean()))
gauges['root_depth_50'] = gauges.groupby('dom_land_cover')['root_depth_50'].transform(lambda x: x.fillna(x.mean()))


for unit in gauges["gauge_id"]:
    gauge = str(unit).zfill(8)
    header_line = f"{unit} {2}"
    if gauges[gauges.gauge_id == unit]["Class"].iat[0] != 5:
        data1 = [
        [gauges[gauges.gauge_id == unit]["Class"].iat[0], gauges[gauges.gauge_id == unit].dom_land_cover_frac.iat[0],
         gauges[gauges.gauge_id == unit]["root_depth_50"].iat[0],
         0.5, gauges[gauges.gauge_id == unit]["root_depth_99"].iat[0] - gauges[gauges.gauge_id == unit]["root_depth_50"].iat[0],
         0.5]
        ]
    
        data2 = [
        [5, 1 - gauges[gauges.gauge_id == unit].dom_land_cover_frac.iat[0],
         gauges[gauges.gauge_id == unit]["root_depth_50"].iat[0],
         0.5, gauges[gauges.gauge_id == unit]["root_depth_99"].iat[0] - gauges[gauges.gauge_id == unit]["root_depth_50"].iat[0],
         0.5]
        ]
        df = pd.DataFrame(data1 + data2) 
    else:
        data1 = [
        [gauges[gauges.gauge_id == unit]["Class"].iat[0], 1.0,
         gauges[gauges.gauge_id == unit]["root_depth_50"].iat[0],
         0.5, gauges[gauges.gauge_id == unit]["root_depth_99"].iat[0] - gauges[gauges.gauge_id == unit]["root_depth_50"].iat[0],
         0.5]
        ]
        df = pd.DataFrame(data1)
        
    file_path = os.path.join(os.getcwd(), "CONUS", gauge, "parameters", "basin_vegparam.txt")
    with open(file_path, "w") as file:
        file.write(header_line + "\n")  # Write the header line
        df.to_csv(file, sep=" ", index=False, header=False, float_format="%.6f")  # Write the data
