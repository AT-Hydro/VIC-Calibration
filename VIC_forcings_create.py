# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 20:39:29 2025

@author: atakallou
"""

import pandas as pd
import numpy as np

def calculate_vapor_pressure(P, q):
    """
    Calculate vapor pressure using specific humidity and total pressure.

    Parameters:
        P (float): Total atmospheric pressure in Pa.
        q (float): Specific humidity (dimensionless, kg water/kg air).

    Returns:
        float: Vapor pressure in Pa.
    """
    e = q * P / (0.622 + 0.378 * q)
    return e

gauge = "01013500"
forcing = pd.read_csv(f"Extract_forcings/{gauge}.csv")
forcing["VP"] = calculate_vapor_pressure(forcing.P, forcing.SPFH)
VICforcing = pd.DataFrame()
VICforcing["PREC"]    = forcing["prc"]
VICforcing["AIR_TEMP"]= forcing["temp"] + -273.15
VICforcing["SWDOWN"]  = forcing["SWRF"]
VICforcing["LWDOWN"]  = forcing["LWRF"]
VICforcing["AirD"]    = 1.0
VICforcing["PRESSURE"]= forcing["P"] / 1000
VICforcing["VP"]      = forcing["VP"] / 1000
VICforcing["WIND"]    = np.sqrt(forcing["Uwind"] **2 + forcing["Vwind"] ** 2)
VICforcing.to_csv(f'./VIC_Forcings/{gauge}.txt', sep='\t', index=False, header=False)