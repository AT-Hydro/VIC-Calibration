# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 12:11:30 2025

@author: atakallou
"""
import os
import numpy as np
import time
from datetime import datetime
from ColdStart import glob_parm_set, model_evolve, model_rout
from pathlib import Path


###########################################################################################
""" This code is for Cold start of the model and create intial condition for Warm start """
#############################################################################################

# first we need to create the ensemble run of cold start
#parm and master folder should be modified accordingly
s =  time.time()
parm     =  np.load("/icebox/data/shares/mh1/Atakallou/VIC/Calib_Parms/Parm_2.npy")
base_folder = os.getcwd()
DA_path     = os.path.join(base_folder, "DA")
Master_folder = os.path.join(DA_path, "Ensemble_run_01047000")
# start end and state outputs
start_date  = datetime(1979, 1, 2)
end_date    = datetime(2019, 3, 13)
state_date  =  datetime(2013,10,1)
for ens in range(100):
    gaugepath = os.path.join(Master_folder ,  f"Ens_{ens}")
    glob_parm_set(gaugepath, start_date, end_date, state_date)
print(time.time() - s)
s = time.time()

# 1.5 Seconds
# step 2
# we run the model for all the ensemble memebers 
for ens in range(1):
    gaugepath = os.path.join(Master_folder ,  f"Ens_{ens}")
    model_evolve(gaugepath)
print(time.time()  - s)
#13 Seconds

#Step 3 
#rout results and create the routing state of the model in  10/01/2013
s = time.time()

for ens in range(1):
    resdir = os.path.join(Master_folder ,  f"Ens_{ens}", "results")
    resdir = Path(resdir)
    latest_result = max(resdir.iterdir(), key=lambda f: f.stat().st_ctime)
    flow, states = model_rout(latest_result,parm, initialPath = None, stopdate= state_date)
#4.5 Seconds
print(time.time() - s)    