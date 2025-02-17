# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 00:42:20 2025

@author: atakallou
"""
import pandas as pd 
import numpy as np
import os
import glob

VIC_forcings_all = pd.read_csv("VIC_Forcing_all.csv")
gauges = pd.read_csv("Gauges.csv")
VIC_forcings_all['air_density'] = 1.293
VIC_forcings_all['WIND'] = np.sqrt(VIC_forcings_all['wind_u'] ** 2 + VIC_forcings_all['wind_v'] ** 2)
VIC_forcings_all['VP']   = (VIC_forcings_all['specific_humidity'] * VIC_forcings_all['pressure']) / (0.622 + 0.378 * VIC_forcings_all['specific_humidity'])
VIC_forcings_all['VP']   =  VIC_forcings_all['VP'] / 1000
VIC_forcings_all['pressure'] = VIC_forcings_all['pressure'] / 1000


#create forcings in folders 
for gauge in VIC_forcings_all.gauge_id.unique():
    unit = gauge
    gauge = gauge.astype(str).zfill(8)
    if not os.path.exists(os.path.join(os.getcwd(), "CONUS", gauge)):
        os.makedirs(os.path.join(os.getcwd(), "CONUS", gauge))
    else:
        gauge_path = os.path.join(os.getcwd(), "CONUS", gauge)
        if not os.path.exists(os.path.join(gauge_path, "forcings")):
            os.makedirs(os.path.join(gauge_path, "forcings"))
        else:
            column_order = ['total_precipitation', 'temperature', 'shortwave_radiation',
                           'longwave_radiation', 'air_density' , 'pressure', 'VP', 
                           'WIND']
            lat_value = round(gauges[gauges.gauge_id == unit]['LAT'].iloc[0], 4)
            lon_value = round(gauges[gauges.gauge_id == unit]['LONG'].iloc[0], 4)
            df = VIC_forcings_all[VIC_forcings_all.gauge_id == unit]
            filename = f"full_data_{lat_value}_{lon_value}"
            filepath = os.path.join(gauge_path, "forcings", filename)
            
            df[column_order].to_csv(filepath, sep='\t', index=False, header=False)