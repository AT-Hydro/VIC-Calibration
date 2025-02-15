# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 12:55:51 2025

@author: atakallou
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil



#Gauges information
metadata = "/mh1/Atakallou/VIC/Forcing/basin_metadata"
metadata = os.path.join(metadata, "gauge_information.txt")
gauges = pd.read_csv(metadata, 
                 sep=r'\t+', 
                 engine='python', 
                 names=['HUC_02', 'GAGE_ID', 'GAGE_NAME', 'LAT', 'LONG', 'DRAINAGE AREA (KM^2)'], skiprows= 1 )
gauges["GAGE_ID"] = gauges["GAGE_ID"].astype(str).str.zfill(8)
physical_char = pd.read_csv(os.path.join("/mh1/Atakallou/VIC/Forcing/basin_metadata", "basin_physical_characteristics.txt"),
                            delimiter='\\s+',skipinitialspace=True)
physical_char["BASIN_ID"] = physical_char["BASIN_ID"].astype(str).str.zfill(8)
gauges = pd.merge(gauges, physical_char, left_on= "GAGE_ID", right_on= "BASIN_ID", how="right")
gauges.rename(columns={"GAGE_ID": "gauge_id"}, inplace = True)

attrs_files = ["camels_clim.txt", "camels_geol.txt", "camels_hydro.txt", "camels_name.txt", "camels_soil.txt" , "camels_topo.txt", "camels_vege.txt"]


for file in attrs_files:
    path  = os.path.join("/mh1/Atakallou/VIC" , file)
    df = pd.read_csv(path, sep = ";" )
    df["gauge_id"]  = df["gauge_id"].astype(str).str.zfill(8)
    gauges = pd.merge (df,
                       gauges, 
                       on = "gauge_id", how="right", suffixes=("_df", "_gauges"))
    # gauges.drop(columns = ["GAGE_ID"],inplace = True)

gauges ["Bdensity"]= 2.685 * ( 1 - gauges.soil_porosity)
gauges.drop(columns = ["BASIN_ID", "BASIN_HUC", "HUC_02"], inplace  = True)


VIC_soil_param = pd.DataFrame()
VIC_soil_param["run_cell"] = 1.0
VIC_soil_param["gridcel"]  = gauges.gauge_id
VIC_soil_param["run_cell"] = 1.0
VIC_soil_param["lat"]      = gauges.LAT
VIC_soil_param["lon"]      = gauges.LONG
VIC_soil_param["infilt"]   = 0.3 # Calibration [0.0, 0.4]
VIC_soil_param["Ds"]       = 0.1 # Calibratio [0,1]
VIC_soil_param["Dsmax"]    = 10.0# Calibration[0,30]
VIC_soil_param["Ws"]       = 0.7 # Calibration[0,1]
VIC_soil_param["c"]        = 2.0 # Calibration[3, 15]
VIC_soil_param["expt1"]    = 12.0
VIC_soil_param["expt2"]    = 12.0
VIC_soil_param["expt3"]    = 12.0
VIC_soil_param["Ksat1"]    = gauges.soil_conductivity * 240
VIC_soil_param["Ksat2"]    = gauges.soil_conductivity * 240
VIC_soil_param["Ksat3"]    = gauges.soil_conductivity * 240
VIC_soil_param["phi_s1"]   = -99
VIC_soil_param["phi_s2"]   = -99
VIC_soil_param["phi_s3"]   = -99
VIC_soil_param["init_SM1"] = 15.00
VIC_soil_param["init_SM2"] = 46.00
VIC_soil_param["init_SM3"] = 154.00
VIC_soil_param["elev"]     = gauges.elev_mean
VIC_soil_param["Depth1"]   = 0.1 # Calibration [0.1, 1.5]
VIC_soil_param["Depth2"]   = 0.3 # Calibration [0.1, 1.5]
VIC_soil_param["Depth3"]   = 1.5 # Calibration [0.1, 1.5]
VIC_soil_param["avg_T"]    = -9999
VIC_soil_param["dp"]       = -9999
VIC_soil_param["bubble1"]  = 14.66 # Calibration [0,100]
VIC_soil_param["bubble2"]  = 14.66 # Same as the bubble 1
VIC_soil_param["bubble3"]  = 14.66 # Same as the bubble 1
VIC_soil_param["quartz1"]  = -9999
VIC_soil_param["quartz2"]  = -9999
VIC_soil_param["quartz3"]  = -9999
VIC_soil_param["Bdensity1"]= gauges.Bdensity
VIC_soil_param["Bdensity2"]= gauges.Bdensity
VIC_soil_param["Bdensity3"]= gauges.Bdensity
VIC_soil_param["Sdensity1"]= 2685
VIC_soil_param["Sdensity2"]= 2685
VIC_soil_param["Sdensity3"]= 2685
VIC_soil_param["off_gmt"]  = 0
VIC_soil_param["Wcr_FRACT1"]= 0.7 *  (gauges.max_water_content / gauges.soil_depth_statsgo) #Calibration [0.01,0.6]
VIC_soil_param["Wcr_FRACT2"]= 0.7 *  (gauges.max_water_content / gauges.soil_depth_statsgo) #Same as 1
VIC_soil_param["Wcr_FRACT3"]= 0.7 *  (gauges.max_water_content / gauges.soil_depth_statsgo) #Same as 1
VIC_soil_param["Wpwp_FRACT1"]= 0.7 * (gauges.max_water_content / gauges.soil_depth_statsgo) #Calibration [0.01,0.6]
VIC_soil_param["Wpwp_FRACT2"]= 0.7 * (gauges.max_water_content / gauges.soil_depth_statsgo) #Same as 1
VIC_soil_param["Wpwp_FRACT3"]= 0.7 * (gauges.max_water_content / gauges.soil_depth_statsgo) #Same as 1
VIC_soil_param["rough"]      = 0.01 #Calibration [0.0005,0.05]
VIC_soil_param["snow_rough"] = 0.03 #Calibration [0.00001, 0.05]
VIC_soil_param["annual_prec"]= gauges.p_mean * 365
VIC_soil_param["resid_moist1"]= 0.02 #calibration [0.005, 0.2]
VIC_soil_param["resid_moist2"]= 0.02  # Same as the bubble 1
VIC_soil_param["resid_moist3"]= 0.02  # Same as the bubble 1
VIC_soil_param["fs_active"]   = 0
VIC_soil_param["July_Tavge"]  = 20 #check the forcings and modify this 


