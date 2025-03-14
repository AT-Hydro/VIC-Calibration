# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 14:51:52 2025

@author: atakallou
"""
import numpy as np
import pandas as pd 
import os
import glob
import subprocess
from Routing import routing_model
from model_config import configure_simulation
from ParmChange import Soil_parm_change
from PfMetrics import KGE



gauges =  pd.read_csv("Gauges2.csv")
states        =  np.array([15.0, 50.0,150.0, 0.5,0.5,0.5])
number =  1
gauge = gauges.gauge_id.unique()[number]
initial_parm = np.load(os.path.join(os.getcwd(), "Valid_Parms", f"Parm_{number}.npy"))
Soil_parm_change(initial_parm, gauge)
configure_simulation(
gauge, startyear = 1979, startmonth = 1, startday = 2, 
endyear = 2019, endmonth = 3, endday = 13,
stateyear = 1985, statemonth = 1, stateday = 1,
)
directory = os.path.join(os.getcwd(), "CONUS", gauge.astype(str).zfill(8))
script_path = os.path.join(directory, "submit_VIC.job")
# Submit the SLURM job using sbatch
# os.system(f"sbatch {script_path}")
# subprocess.run(['sbatch', '--wait', f'{script_path}'], check = True)
glob_parm_path =  os.path.join(directory, "parameters", "global_param.basin.txt")
VIC="/mh1/Atakallou/VIC/VIC/vic/drivers/classic/vic_classic.exe"
subprocess.run([f'{VIC}', '-g', f'{glob_parm_path}'], check = True
          , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
gauge        =  str(gauge).zfill(8)
sim_path     = glob.glob(os.path.join("/mh1/Atakallou/VIC/CONUS", f'{gauge}', "results",'*.txt'))
sim          = pd.read_csv(sim_path[0],sep = '\s+', skiprows=2)
rout_inits   = np.array([0.5,0.5,0.5])
Qflow    = np.zeros(len(sim))
runoffs  = sim['OUT_RUNOFF'].to_numpy()
baseflows= sim['OUT_BASEFLOW'].to_numpy()
for idx in range(len(sim)):
    Qflow[idx], states[3],states[4],states[5] = routing_model(runoffs[idx],baseflows[idx],initial_parm[-1],states[3],states[4],states[5])
sim['Qflow'] = Qflow
obs_path    =  os.path.join("/mh1/Atakallou/VIC/Forcing/hourly_kretzert/usgs_streamflow", f"{gauge}-usgs-hourly.csv")
obs         =  pd.read_csv(obs_path)
obs['date'] =  pd.to_datetime(obs['date'])
full_range  = pd.date_range(start=obs['date'].min(), end=obs['date'].max(), freq='h')
obs         = obs.set_index('date').reindex(full_range).reset_index()
obs.rename({'index': 'date'}, axis=1, inplace=True)
obs.date = pd.to_datetime(obs.date)
obs = obs.dropna(subset=['QObs(mm/h)'])
sim["hour"] = sim["SEC"] / 3600
sim.hour    = sim.hour.astype(int)
sim['date'] = pd.to_datetime(sim[['YEAR', 'MONTH', 'DAY', 'hour']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
sim = sim[sim.date >= pd.to_datetime("1980-10-01")]
sim = sim[sim['date'].isin(obs['date'])]
obs = obs[obs['date'].isin(sim['date'])]
# years = sim['date'].dt.year.unique()
# excluded_years = years[int(len(years) / 5 ) * -1:]
# sim = sim[~sim['date'].dt.year.isin(excluded_years)]
sim = sim[sim['date'].dt.year % 2 != 0] 
obs = obs[obs['date'].isin(sim['date'])]
print(KGE(sim['Qflow'].to_numpy(), obs['QObs(mm/h)'].to_numpy()))
