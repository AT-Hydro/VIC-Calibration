# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:29:06 2025

@author: atakallou
"""

######################################################
""" This code is for saving the cold start states"""
######################################################
import os
import shutil
import pandas as pd
import numpy as np

Curr_dir = os.getcwd()
os.makedirs("ColdStates", exist_ok= True)
gauges = pd.read_csv("Gauges2.csv")
for gauge in gauges.gauge_id:
    os.makedirs(f"ColdStates/{gauge}_state", exist_ok= True)
    lsm_state = os.path.join(Curr_dir, "DA", f"Ensemble_{gauge}", "Ens_0", "States", "States_20131001_00000")
    rt_state  = os.path.join(Curr_dir, "DA", f"Ensemble_{gauge}", "Ens_0", "results", "Rout_20131001.npy")
    stdir     = os.path.join(Curr_dir, "ColdStates", f"{gauge}_state" )
    shutil.copy2(lsm_state,stdir)
    shutil.copy2(rt_state, stdir)