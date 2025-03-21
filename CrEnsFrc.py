###################################################
"""This code is for perturbing the Forcings"""
####################################################
import os
import pandas as pd
import numpy as np
import sys
from DAFunctions import lognormPerturb, normPerturb

base_folder   = os.getcwd()
gauges = pd.read_csv("Gauges2.csv")
gauge         = gauges.gauge_id[int(sys.argv[1])]
forcing_folder  =  os.path.join(os.getcwd(),  "CONUS", str(gauge).zfill(8), "forcings")
forcing_file    =  os.path.join(os.getcwd(),  "CONUS", 
                                str(gauge).zfill(8), "forcings", os.listdir(forcing_folder)[0])
forcing         = pd.read_csv(forcing_file, sep ="\t", names  = ["PREC", "AIR_TEMP", "SWDOWN", "LWDOWN",
                                                                   "AirD", "PRESSURE", "VP", "WIND"])
forcing_err = 0.25
np.random.seed(42)
prc_pert = lognormPerturb(forcing['PREC'].to_numpy(),forcing_err, 100,  len(forcing['PREC']))
temp_pert= normPerturb(forcing['AIR_TEMP'].to_numpy(),forcing_err, 100, len(forcing['AIR_TEMP']))
sw_pert  = lognormPerturb(forcing['SWDOWN'].to_numpy(), forcing_err, 100, len(forcing['SWDOWN']))
lw_pert  = lognormPerturb(forcing['LWDOWN'].to_numpy(), forcing_err, 100, len(forcing['LWDOWN']))
vp_pert  = lognormPerturb(forcing["VP"].to_numpy(), forcing_err, 100, len(forcing['VP']))
w_pert   = lognormPerturb(forcing["WIND"].to_numpy(), forcing_err, 100, len(forcing['WIND']))

#allocate to ensemble folder forcing file
for ens in range(100):
    ens_forcingfile = os.path.join(os.getcwd(), "DA", f"Ensemble_{gauge}", f"Ens_{ens}", "forcings", os.listdir(forcing_folder)[0])
    ens_forcing     = pd.read_csv(ens_forcingfile, sep ="\t", names  = ["PREC", "AIR_TEMP", "SWDOWN", "LWDOWN",
                                                                       "AirD", "PRESSURE", "VP", "WIND"])
    ens_forcing["PREC"]    = prc_pert[:,ens]
    ens_forcing["AIR_TEMP"]= temp_pert[:,ens]
    ens_forcing['SWDOWN']  = sw_pert[:,ens]
    ens_forcing['LWDOWN']  = lw_pert[:,ens]
    ens_forcing["VP"]      = vp_pert[:,ens]
    ens_forcing["WIND"]    = w_pert[:,ens]
    ens_forcing.to_csv(ens_forcingfile, sep = "\t", index = False, header = False)
