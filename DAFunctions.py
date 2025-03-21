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
        end_date = start_date
        
    endyear, endmonth, endday = str(end_date.year), str(end_date.month).zfill(2), str(end_date.day).zfill(2)
    if state_date is None:
        state_date = start_date  + timedelta(days=1)
        stateyear, statemonth, stateday = str(state_date.year), str(state_date.month), str(state_date.day)
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
        
    # we will add this option (saving the routing states)if necessary in future
    # else:
    #     rout_state_path =  os.path.join(parent_dir,
    #                                     f"{sim['YEAR'].iat[-1]}{str(sim['MONTH'].iat[-1]).zfill(2)}{str(sim['DAY'].iat[-1]).zfill(2)}.npy")
    #     np.save(rout_state_path, rout_states)
    return Qflow, rout_states
    
def Cleaner(Master_folder):
    for ens in range(0,100):
        directory =  os.path.join(Master_folder, f"Ens_{ens}", "results")
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            os.remove(file_path)
    for ens in range(0,100):
        directory =  os.path.join(Master_folder, f"Ens_{ens}", "States")
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            os.remove(file_path)

def read_state(Ens_folder,date):
    year, month, day = str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2)
    state_file_path = os.path.join(Ens_folder, "States", f"States_{year}{month}{day}_00000")
    rout_file_path = os.path.join(Ens_folder, "results", f"Rout_{year}{month}{day}.npy")
    rout_states      = np.load(rout_file_path)
    with open(state_file_path, "r") as f:
        lines = f.readlines()
    state_line = lines[3].split(" ")
    states = np.array([float(state_line[2]), float(state_line[3]), float(state_line[4]), float(state_line[12]), rout_states[0], rout_states[1], rout_states[2]])
    return states

def write_state(Ens_folder,date, states):
    year, month, day = str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2)
    state_file_path = os.path.join(Ens_folder, "States", f"States_{year}{month}{day}_00000")
    rout_file_path = os.path.join(Ens_folder, "results", f"Rout_{year}{month}{day}.npy")
    rout_states      = np.load(rout_file_path)
    with open(state_file_path, "r") as f:
        lines = f.readlines()
    state_line = lines[3].split(" ")
    state_line[2] = str(states[0])
    state_line[3] = str(states[1])
    state_line[4] = str(states[2])
    state_line[12] = str(states[3])
    rout_states[0]= states[4]
    rout_states[1]= states[5]
    rout_states[2]= states[6]
    lines[3] = " ".join(state_line) 
    if len(lines) > 5:
        if float(lines[4].split(" ")[2]) > 0.0:
            lines[4] = " ".join(state_line) 
    with open(state_file_path, "w") as f:
        f.writelines(lines)
    np.save(rout_file_path , rout_states)
    return 1

def resampling(w):
    wc = np.cumsum(w)  # Cumulative sum of weights
    mw = max(w.shape)  # Number of particles
    u = (np.arange(mw) + np.random.rand()) / mw  # Uniform CDF
    Index = np.zeros(mw, dtype=int)  # Initialize indices
    k = 0  # Start count at 1
    for j in range(mw):
        if k < mw:
            while  u[j] > wc[k]:  # Compare cumulative weight and uniform CDF
                k += 1
            Index[j] = k  # Save index which exceeds uniform CDF
    return Index

def lognormPerturb(m, err, n_sample, nda):
    """
    This function perturbs the input using a lognormal error assumption
    err is the coefficient of variation and Qin current value
    This function uses a heteroschedastic assumption.
     variable that you perturb
    """
    
    m[m == 0] = 0.01
    m = m[:nda]
    CV = err * np.ones(nda)

    mu = 0.5 * np.log((m ** 2) / ((CV ** 2) + 1))
    sigma_L = np.sqrt(np.log(CV ** 2 + 1))
    pr_pert = np.zeros((nda, n_sample))
    
    for t in range(nda):
        pr_pert[t, :] = np.random.lognormal(mean=mu[t], sigma=sigma_L[t], size=n_sample)
    
    return pr_pert
    

def normPerturb(m, err, n_sample, nda):
    
    """
    This function perturbs the input using a normal error assumption.
    err is the coefficient of variation and Qin current value.
    This function uses a heteroschedastic assumption.
    """
    pr_pet = np.zeros((nda, n_sample))
    for t in range(nda):
        pr_pet[t, :] = m[t] + np.random.randn(n_sample) * m[t] * err
    return pr_pet