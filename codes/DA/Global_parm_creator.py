# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 19:13:38 2025

@author: atakallou
"""

import numpy as np 
import pandas as pd
import os
import glob
import subprocess
from datetime import datetime, timedelta


def ens_glob_parms (gaugepath, startyear, startmonth, startday,
                 forcingyear = 1979, forcingmonth = 1, forcingday = 2, read_state = False):
    start_date = datetime(int(startyear), int(startmonth), int(startday))
    end_date = start_date + timedelta(days=1)
    endyear, endmonth, endday = str(startyear), str(startmonth).zfill(2), str(startday).zfill(2)
    stateyear, statemonth, stateday = str(end_date.year), str(end_date.month), str(end_date.day)
    startyear, startmonth, startday = str(startyear), str(startmonth).zfill(2), str(startday).zfill(2)
    forcingyear, forcingmonth, forcingday = str(forcingyear), str(forcingmonth).zfill(2), str(forcingday).zfill(2)

    parm_path      = os.path.join(gaugepath, "parameters")
    soil_parm_path = os.path.join(parm_path, "basin_soil.txt")
    veg_lib_path   = os.path.join(parm_path, "basin_veglib.txt")
    veg_parm_path  = os.path.join(parm_path, "basin_vegparam.txt")
    log_path       = os.path.join(gaugepath, "LogFolder", "Logs")
    res_path       = os.path.join(gaugepath, "results")
    # state day write
    state_path     = os.path.join(gaugepath, "States", "States")
    # forcing path
    forcing_path   = os.path.join(gaugepath, "forcings", "full_data_")
    with open("global_param.STEHE.txt", 'r') as f:
        lines = f.readlines()
    #read state 
    if read_state == True:
        state_file = f"States_{startyear}{startmonth}{startday}_00000"
        init_path  = os.path.join(gaugepath, "States", state_file)
        lines[24]   =f'INIT_STATE {init_path} # Initial state path/file, where YYYY = year, MM = month, DD = day, SSSSS = seconds, for example 19490111_00000\n'
    #change the lines 
    lines[12] = f'STARTYEAR             {startyear}   # year model simulation starts\n'
    lines[13] = f'STARTMONTH            {startmonth}     # month model simulation starts\n'
    lines[14] = f'STARTDAY              {startday}     # day model simulation starts\n'
    lines[15] = f'ENDYEAR               {endyear}   # year model simulation ends\n'
    lines[16] = f'ENDMONTH              {endmonth}     # month model simulation ends\n'
    lines[17] = f'ENDDAY                {endday}     # day model simulation ends\n'
    lines[26] = f'STATEYEAR   {stateyear}    # year to save model state\n'
    lines[27] = f'STATEMONTH  {statemonth}  # month to save model state\n'
    lines[28] = f'STATEDAY    {stateday}  # day to save model state\n'
    lines[25] = f'STATENAME {state_path}  # Output state file path/prefix. The time (STATEYEAR,STATEMONTH,STATEDAY,STATESEC) will be appended to the prefix automatically in the format yyyymmdd.\n'
    lines[35] = f'FORCING1             {forcing_path}    # Forcing file path and prefix, ending in "_"\n'
    lines[46] = f'FORCEYEAR            {forcingyear}  # Year of first forcing record\n'
    lines[47] = f'FORCEMONTH           {forcingmonth}    # Month of first forcing record\n'
    lines[48] = f'FORCEDAY             {forcingday}    # Day of first forcing record\n'

    lines[55] = f'SOIL                {soil_parm_path}     # Soil parameter path/file\n'
    lines[59] = f'VEGLIB              {veg_lib_path}    # Veg library path/file\n'
    lines[60] = f'VEGPARAM            {veg_parm_path}  # Veg parameter path/file\n'
    lines[69] = f'\n'
    lines[70] = f'RESULT_DIR     {res_path}  # Results directory path\n'
        
    glob_parm_path =  os.path.join(parm_path, f"gp_{startyear}{startmonth}{startday}.basin.txt")
    with open(glob_parm_path, "w") as file:
        for line in lines:
            file.write(line)

def gpAllCreator(ensemble_master_folder):
    start_date = datetime(1979, 1, 2)
    end_date = datetime(2019, 3, 13)
    # evolve one day as cold start 
    current_date = start_date
    year, month, day = current_date.year, current_date.month, current_date.day
    for ens in range(100):
        gaugepath = os.path.join(ensemble_master_folder,  f"Ens_{ens}" )
        ens_glob_parms(gaugepath , year, month, day)
    #create warmed global parameters
    current_date += timedelta(days=1)
    while current_date <= end_date:
        year, month, day = current_date.year, current_date.month, current_date.day
        for ens in range(100):
            gaugepath = os.path.join(ensemble_master_folder, "Ensemble_run_01047000" ,  f"Ens_{ens}")
            ens_glob_parms(gaugepath , year, month, day, read_state = True)
        current_date += timedelta(days=1)