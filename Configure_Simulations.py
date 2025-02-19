# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 20:19:17 2025

@author: atakallou
"""
import os
import pandas as pd
import numpy as np

def ch_Parglob_ln(lines, i,text,replace):
    if lines[i].find(text) != -1:
        lines[i] = lines[i][:lines[i].find(text)] + replace + lines[i][lines[i].find(text) + len(replace):]
    return lines


list_folders =  os.listdir(os.path.join(os.getcwd(), "CONUS"))
for folder in list_folders:
    Log_path = os.path.join(os.getcwd(), "CONUS" ,  folder, "LogFolder")
    if not os.path.exists(Log_path):
        os.makedirs(Log_path)
    results_path = os.path.join(os.getcwd(), "CONUS" ,  folder, "results")
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    ST_path = os.path.join(os.getcwd(), "CONUS" ,  folder, "States")
    if not os.path.exists(ST_path):
        os.makedirs(ST_path)


# def Simulation_generalize(gauge, startyear, start)
# start and end of the simulations

def configure_simulation(
    gauge, startyear, startmonth, startday, 
    endyear, endmonth, endday,
    stateyear, statemonth, stateday,
    forcingyear, forcingmonth, forcingday, initstate = ""
):

    # define start and end of smulation and period of forcings
    startyear, startmonth, startday = str(startyear), str(startmonth).zfill(2), str(startday).zfill(2)
    endyear, endmonth, endday = str(endyear), str(endmonth).zfill(2), str(endday).zfill(2)
    stateyear, statemonth, stateday = str(stateyear), str(statemonth), str(stateday)
    forcingyear, forcingmonth, forcingday = str(forcingyear), str(forcingmonth).zfill(2), str(forcingday).zfill(2)

    
    #Land surface Parameters
    parm_path = os.path.join(os.getcwd(), "CONUS", gauge, "parameters")
    soil_parm_path = os.path.join(parm_path, "basin_soil.txt")
    veg_lib_path   = os.path.join(parm_path, "basin_veglib.txt")
    veg_parm_path  = os.path.join(parm_path, "basin_vegparam.txt")
    log_path       = os.path.join(os.getcwd(), "CONUS", gauge, "LogFolder", "Logs")
    res_path    = os.path.join(os.getcwd(), "CONUS", gauge, "results")
    if len(initstate) > 0:
        init_path   = os.path.join(os.getcwd(), "CONUS", gauge, "States", initstate)
    # state day write
    state_path     = os.path.join(os.getcwd(), "CONUS", gauge, "States", "States")
    # forcing path
    forcing_path = os.path.join(os.getcwd(), "CONUS", gauge, "forcings", "full_data_")
    with open("global_param.STEHE.txt", 'r') as f:
        lines = f.readlines()



    lines = ch_Parglob_ln(lines, 12,"1949", startyear)
    lines = ch_Parglob_ln(lines, 13, "01", startmonth)
    lines = ch_Parglob_ln(lines, 14, "01", startday)
    lines = ch_Parglob_ln(lines, 15, "1949", endyear)
    lines = ch_Parglob_ln(lines, 16, "01", endmonth)
    lines = ch_Parglob_ln(lines, 17, "10", endday)
    lines = ch_Parglob_ln(lines, 26, "1949", stateyear)
    lines[27] = f'STATEMONTH  {statemonth}  # month to save model state\n'
    lines[28] = f'STATEDAY    {stateday}  # day to save model state\n'
    lines[25] = f'STATENAME {state_path}  # Output state file path/prefix. The time (STATEYEAR,STATEMONTH,STATEDAY,STATESEC) will be appended to the prefix automatically in the format yyyymmdd.\n'
    lines[35] = f'FORCING1             {forcing_path}    # Forcing file path and prefix, ending in "_"\n'
    lines = ch_Parglob_ln(lines, 46, "1949", forcingyear)
    lines = ch_Parglob_ln(lines, 47, "01", forcingmonth)
    lines = ch_Parglob_ln(lines, 48, "01", forcingday)
    lines[55] = f'SOIL                {soil_parm_path}     # Soil parameter path/file\n'
    lines[59] = f'VEGLIB              {veg_lib_path}    # Veg library path/file\n'
    lines[60] = f'VEGPARAM            {veg_parm_path}  # Veg parameter path/file\n'
    lines[69] = f'LOG_DIR\t\t{log_path}\n'
    lines[70] = f'RESULT_DIR     {res_path}  # Results directory path\n'
    
    glob_parm_path =  os.path.join(parm_path, "global_param.basin.txt")
    with open(glob_parm_path, "w") as file:
        for line in lines:
            file.write(line)



# configure_simulation(
#     gauge, startyear = 1979, startmonth = 1, startday = 2, 
#     endyear = 2019, endmonth = 3, endday = 13,
#     stateyear = 1980, statemonth = 1, stateday = 1,
#     forcingyear = 1979, forcingmonth = 1, forcingday = 2
# )