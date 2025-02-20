# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 17:41:06 2025

@author: atakallou
"""
import pandas as pd
import os
import numpy as np

def Soil_parm_change(initial_parm, gauge):
    unit = gauge
    gauge = gauge.astype(str).zfill(8)
    soil_all = pd.read_csv("VIC_Soilall.csv")
    gauge_soil = soil_all[soil_all.gridcel == unit].copy()
    gauge_soil[['init_SM1', 'init_SM2', 'init_SM3']] = [15.0, 50.0, 150.0]
    #assign bubble pressure according to expt
    for i in range(1, 4):
        gauge_soil[f'bubble{i}'] = 0.32 * gauge_soil[f'expt{i}'] + 4.3
    gauge_path = os.path.join(os.getcwd(), "CONUS", gauge)
    parm_path  = os.path.join(gauge_path, "parameters")
    if not os.path.exists(parm_path):
        os.makedirs(parm_path)
    soil_parm_path = os.path.join(parm_path, "basin_soil.txt")


    #writing the soil parameter file for the gauge
    header_line = "# " + "\t".join(gauge_soil.columns) + "\n"
    with open(soil_parm_path, "w") as file:
        file.write(header_line)  # Write the column names as the header
        gauge_soil.to_csv(file, sep='\t', index=False, header=False)  # Append data without headers

    # if not os.path.exists(soil_parm_path):
    # df.to_csv(soil_parm_path, sep=' ', index=False, header=False)
    frozensoil_parm_path = os.path.join(parm_path, "basin_soil.FROZEN_SOIL.txt")
    # if not os.path.exists(frozensoil_parm_path):
    gauge_soil['fs_active'] = 1
    gauge_soil.to_csv(frozensoil_parm_path, sep=' ', index=False, header=False)

    
#binfilt Ds DsMax Ws expt1 expt2 expt3 Depth1 Depth2 Depth3
bU = np.array([0.4,1.0,50.0,1.0,30,30,30,0.5,1.5,1.5])
bL = np.array([0.00001, 0.001,0.1, 0.001,3.0,3.0,3.0,0.01,0.1,0.1])
# soil_all[['infilt', 'Ds', 'Dsmax', 'Ws',
#        'expt1', 'expt2', 'expt3','Depth1', 'Depth2', 'Depth3']]
initial_parm  =  np.array([0.3,0.1,10.0,0.7,12.0,12.0,12.0,0.1,0.3,1.5])

gauges =  pd.read_csv("Gauges.csv")
gauge = gauges.gauge_id.unique()[0]
print(gauge)
Soil_parm_change(initial_parm, gauge)