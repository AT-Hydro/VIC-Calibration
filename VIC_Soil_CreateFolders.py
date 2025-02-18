# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 20:16:27 2025

@author: atakallou
"""

import os
import pandas as pd
import numpy as np

VIC_forcings_all = pd.read_csv("VIC_Forcing_all.csv")
gauges = pd.read_csv("Gauges.csv")
VIC_forcings_all['air_density'] = 1.293
VIC_forcings_all['WIND'] = np.sqrt(VIC_forcings_all['wind_u'] ** 2 + VIC_forcings_all['wind_v'] ** 2)
VIC_forcings_all['VP']   = (VIC_forcings_all['specific_humidity'] * VIC_forcings_all['pressure']) / (0.622 + 0.378 * VIC_forcings_all['specific_humidity'])
VIC_forcings_all['VP']   =  VIC_forcings_all['VP'] / 1000
VIC_forcings_all['pressure'] = VIC_forcings_all['pressure'] / 1000

#create paramter forlder and soil folders
listgauges = VIC_forcings_all.gauge_id.unique()
soil_all = pd.read_csv("VIC_Soilall.csv")
soil_all['Bdensity1'] = soil_all['Bdensity1'] * 1000
soil_all['Bdensity2'] = soil_all['Bdensity1']
soil_all['Bdensity3'] = soil_all['Bdensity1']

for gauge in listgauges:
    unit = gauge
    gauge = gauge.astype(str).zfill(8)
    gauge_path = os.path.join(os.getcwd(), "CONUS", gauge)
    parm_path  = os.path.join(gauge_path, "parameters")
    if not os.path.exists(parm_path):
        os.makedirs(parm_path)
    soil_parm_path = os.path.join(parm_path, "basin_soil.txt")
    # df = soil_all[soil_all.gridcel == unit].drop(columns=['lat', 'lon'])
    df = soil_all[soil_all.gridcel == unit]
    df.run_cell = int(df.run_cell)
    header_line = "# " + "\t".join(df.columns) + "\n"

    # Write to file with header
    with open(soil_parm_path, "w") as file:
        file.write(header_line)  # Write the column names as the header
        df.to_csv(file, sep='\t', index=False, header=False)  # Append data without headers

    # if not os.path.exists(soil_parm_path):
    # df.to_csv(soil_parm_path, sep=' ', index=False, header=False)
    frozensoil_parm_path = os.path.join(parm_path, "basin_soil.FROZEN_SOIL.txt")
    # if not os.path.exists(frozensoil_parm_path):
    df['fs_active'] = 1
    df.to_csv(frozensoil_parm_path, sep=' ', index=False, header=False)

        
