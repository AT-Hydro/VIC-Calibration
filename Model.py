# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 17:25:08 2025

@author: atakallou
"""
import os
import glob
import shutil
import subprocess
from datetime import datetime, timedelta

def model_evlove(MasterFolder, startyear, startmonth, startday,
                 forcingyear = 1979, forcingmonth = 1, forcingday = 2, read_state = False):
    start_date = datetime(int(startyear), int(startmonth), int(startday))
    end_date = start_date + timedelta(days=1)
    endyear, endmonth, endday = str(startyear), str(startmonth).zfill(2), str(startday).zfill(2)
    stateyear, statemonth, stateday = str(end_date.year), str(end_date.month), str(end_date.day)
    startyear, startmonth, startday = str(startyear), str(startmonth).zfill(2), str(startday).zfill(2)
    forcingyear, forcingmonth, forcingday = str(forcingyear), str(forcingmonth).zfill(2), str(forcingday).zfill(2)
        #Land surface Parameters
    parm_path = os.path.join(MasterFolder, "parameters")
    soil_parm_path = os.path.join(parm_path, "basin_soil.txt")
    veg_lib_path   = os.path.join(parm_path, "basin_veglib.txt")
    veg_parm_path  = os.path.join(parm_path, "basin_vegparam.txt")
    log_path       = os.path.join(MasterFolder, "LogFolder", "Logs")
    res_path    = os.path.join(MasterFolder, "results")
    # state day write
    state_path     = os.path.join(MasterFolder, "States", "States")
    # forcing path
    forcing_path = os.path.join(MasterFolder, "forcings", "full_data_")
    with open("global_param.STEHE.txt", 'r') as f:
        lines = f.readlines()
    #read state 
    if read_state == True:
        state_file = f"States_{startyear}{startmonth}{startday}_00000"
        init_path  = os.path.join(MasterFolder, "States", state_file)
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
    lines[69] = f'LOG_DIR\t\t{log_path}\n'
    lines[70] = f'RESULT_DIR     {res_path}  # Results directory path\n'
    
    glob_parm_path =  os.path.join(parm_path, "global_param.basin.txt")
    with open(glob_parm_path, "w") as file:
        for line in lines:
            file.write(line)
    VIC="/mh1/Atakallou/VIC/VIC/vic/drivers/classic/vic_classic.exe"
    subprocess.run([f'{VIC}', '-g', f'{glob_parm_path}'], check = True
                  , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    old_name    = glob.glob(os.path.join(res_path, "flux*.txt"))[0]
    new_name    = os.path.join(res_path, f"{startyear}{startmonth}{startday}.txt")
    os.rename(old_name, new_name)
    return 1


def Create_ens_folder(gauge, Ens_Size):
    source_folder =  '/icebox/data/shares/mh1/Atakallou/VIC/DA'
    os.makedirs(os.path.join(source_folder, f"Ensemble_run_{str(gauge).zfill(8)}"), exist_ok=True)
    for i in range(Ens_Size):
        dest = os.path.join(source_folder, f"Ensemble_run_{str(gauge).zfill(8)}", f"Ens_{i}")
        if not os.path.exists(dest):
            shutil.copytree(os.path.join(source_folder, str(gauge).zfill(8)), dest)
