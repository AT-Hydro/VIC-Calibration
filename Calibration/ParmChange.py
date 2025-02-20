import pandas as pd 
import numpy as np
import os
import glob
import shutil
import subprocess

def Soil_parm_change(initial_parm, gauge):
    unit = gauge
    gauge = gauge.astype(str).zfill(8)
    soil_all = pd.read_csv("VIC_Soilall.csv")
    gauge_soil = soil_all[soil_all.gridcel == unit].copy()
    gauge_soil[['init_SM1', 'init_SM2', 'init_SM3']] = [15.0, 50.0, 150.0]
    #assign bubble pressure according to expt
    # soil_all[['infilt', 'Ds', 'Dsmax', 'Ws',
    #        'expt1', 'expt2', 'expt3','Depth1', 'Depth2', 'Depth3' Kq(routing)]]
    gauge_soil['infilt'] = initial_parm[0]
    gauge_soil['Ds'] = initial_parm[1]
    gauge_soil['Dsmax'] = initial_parm[2]
    gauge_soil['Ws'] = initial_parm[3]
    gauge_soil['expt1'] = initial_parm[4]
    gauge_soil['expt2'] = initial_parm[5]
    gauge_soil['expt3'] = initial_parm[6]
    gauge_soil['Depth1'] = initial_parm[7]
    gauge_soil['Depth2'] = initial_parm[8]
    gauge_soil['Depth3'] = initial_parm[9] 
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