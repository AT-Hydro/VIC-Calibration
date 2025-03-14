# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 12:11:40 2025

@author: atakallou
"""
import pandas as pd 
import numpy as np
import subprocess
import os
from datetime import timedelta
from Routing import routing_model



def glob_parm_set (gaugepath, start_date,
                   end_date = None, state_date = None,
                 forcingyear = 1979, forcingmonth = 1, forcingday = 2, read_state = False):
    if end_date is None:
        end_date = start_date + timedelta(days=1)
        
    endyear, endmonth, endday = str(end_date.year), str(end_date.month).zfill(2), str(end_date.day).zfill(2)
    if state_date is None:
        stateyear, statemonth, stateday = str(end_date.year), str(end_date.month), str(end_date.day)
    else:
        stateyear, statemonth, stateday = str(state_date.year), str(state_date.month), str(state_date.day)
    startyear, startmonth, startday = str(start_date.year), str(start_date.month).zfill(2), str(start_date.day).zfill(2)
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
    lines[71] = f'OUTFILE     {startyear}{startmonth}{startday}_fluxes\n'
        
    glob_parm_path =  os.path.join(parm_path, f"gp_{startyear}{startmonth}{startday}.basin.txt")
    with open(glob_parm_path, "w") as file:
        for line in lines:
            file.write(line)
    return 1


def model_evolve(gaugepath, startyear = 1979, startmonth = 1, startday = 2):
    VIC="/mh1/Atakallou/VIC/VIC/vic/drivers/classic/vic_classic.exe"
    glob_parm_path  =  os.path.join(gaugepath, "parameters",  f"gp_{str(startyear)}{str(startmonth).zfill(2)}{str(startday).zfill(2)}.basin.txt")
    subprocess.run([f'{VIC}', '-g', f'{glob_parm_path}'], check = True
              , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
def model_rout (res_path, parms, initialPath = None , stopdate = None):
    #Loading the routing states if its defined other wise this states should be 0.5 0.5 0.5
    if initialPath:
        rout_states = np.load(initialPath)
    else:
        rout_states = np.array([0.5, 0.5, 0.5])
    #reading the simulated result 
    sim      = pd.read_csv(res_path,sep = '\s+', skiprows=2)
    #if we want to stop routing in a time step :
    if stopdate:
        sim["hour"] = sim["SEC"] / 3600
        sim.hour    = sim.hour.astype(int)
        sim['date'] = pd.to_datetime(sim[['YEAR', 'MONTH', 'DAY', 'hour']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
        sim = sim[sim.date < pd.to_datetime(stopdate)]
    #rout the runoff from the time step 0 to the stopdate or end 
    Qflow    = np.zeros(len(sim))
    runoffs  = sim['OUT_RUNOFF'].to_numpy()
    baseflows= sim['OUT_BASEFLOW'].to_numpy()
    for idx in range(len(sim)):
        Qflow[idx], rout_states[0],rout_states[1],rout_states[2] = routing_model(runoffs[idx],baseflows[idx],parms[-1],
                                                                                 rout_states[0],rout_states[1],rout_states[2])
    parent_dir      =  os.path.dirname(res_path)
    if stopdate:
        rout_state_path =  os.path.join(parent_dir, f"Rout_{stopdate.year}{str(stopdate.month).zfill(2)}{str(stopdate.day).zfill(2)}.npy")
        np.save(rout_state_path, rout_states)
    # we will add this option (saving the routing states)if it necessitates in future
    # else:
    #     rout_state_path =  os.path.join(parent_dir,
    #                                     f"{sim['YEAR'].iat[-1]}{str(sim['MONTH'].iat[-1]).zfill(2)}{str(sim['DAY'].iat[-1]).zfill(2)}.npy")
    #     np.save(rout_state_path, rout_states)
    return Qflow, rout_states
