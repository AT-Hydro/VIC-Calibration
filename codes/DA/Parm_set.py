# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 09:59:45 2025

@author: atakallou
"""


import pandas as pd
import os


def set_soil_parms(calParmPath ,  parm_path):
    soil_parm_path = os.path.join(parm_path, "basin_soil.txt")
    gauge_soil = pd.read_csv(calParmPath, header = 0, sep = ' ')
    #writing the soil parameter file for the gauge
    header_line = "# " + "\t".join(gauge_soil.columns) + "\n"
    with open(soil_parm_path, "w") as file:
        file.write(header_line)  # Write the column names as the header
        gauge_soil.to_csv(file, sep='\t', index=False, header=False)  # Append data without headers
    
    frozensoil_parm_path = os.path.join(parm_path, "basin_soil.FROZEN_SOIL.txt")
    with open(frozensoil_parm_path, "w") as file:
        file.write(header_line)  # Write the column names as the header
        gauge_soil.to_csv(file, sep='\t', index=False, header=False)  # Append data without headers