# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:32:48 2025

@author: atakallou
"""
import pandas as pd
import numpy as np


def classify_soil_texture(sand, clay,silt):
    """
    Classify soil texture based on approximate USDA criteria
    given sand and clay percentages (both in [0, 100]).
    Silt is inferred as 100 - (sand + clay).
    Returns a string such as 's', 'ls', 'sl', 'l', 'scl', 'cl', etc.
    """

    
    
    # --- Example USDA-like classification (simplified) ---
    if clay >= 40:
        # Clay ≥ 40% => “Clay (C)”, “Sandy Clay (SC)”, or “Silty Clay (SIC)”
        if silt >= 40:
            return "sic"  # Silty Clay
        elif sand >= 45:
            return "sc"   # Sandy Clay
        else:
            return "c"    # Clay
    elif clay >= 27:
        # Clay Loam (CL), Silty Clay Loam (SICL), Sandy Clay Loam (SCL)
        if silt >= 50:
            return "sicl"  # Silty Clay Loam
        elif sand >= 45:
            return "scl"   # Sandy Clay Loam
        else:
            return "cl"    # Clay Loam
    elif clay >= 20:
        # Could be SCL or Loam (L) or Silty Loam (SIL)
        if sand >= 45 and sand <= 80:
            return "scl"
        else:
            # Check if it's silty loam vs loam
            if silt >= 50 and silt < 80:
                return "sil"  # Silty Loam
            else:
                return "l"    # Loam
    elif clay < 7:
        # Could be Sand (S), Loamy Sand (LS), or Silt (SI)
        if sand >= 85:
            return "s"   # Sand
        elif silt >= 80:
            return "si"  # Silt
        else:
            return "ls"  # Loamy Sand
    else:
        # 7 <= clay < 20
        # Could be Sandy Loam (SL), Loam (L), Silt (SI), Silty Loam (SIL)
        if silt >= 80:
            return "si"
        elif silt >= 50:
            return "sil"
        else:
            # Possibly sandy loam (SL) or loam (L)
            if sand >= 43 and sand <= 85:
                return "sl"   # Sandy Loam
            else:
                return "l"    # Loam
soil_data = {
    "s":    {"field_capacity": 0.08, "wilting_point": 0.03},
    "ls":   {"field_capacity": 0.15, "wilting_point": 0.06},
    "sl":   {"field_capacity": 0.21, "wilting_point": 0.09},
    "sil":  {"field_capacity": 0.32, "wilting_point": 0.12},
    "si":   {"field_capacity": 0.28, "wilting_point": 0.08},
    "l":    {"field_capacity": 0.29, "wilting_point": 0.14},
    "scl":  {"field_capacity": 0.27, "wilting_point": 0.17},
    "sicl": {"field_capacity": 0.36, "wilting_point": 0.21},
    "cl":   {"field_capacity": 0.34, "wilting_point": 0.21},
    "sc":   {"field_capacity": 0.31, "wilting_point": 0.23},
    "sic":  {"field_capacity": 0.37, "wilting_point": 0.25},
    "c":    {"field_capacity": 0.36, "wilting_point": 0.27},
}

def get_soil_properties(sand, clay, silt):
    """
    Given sand (%) and clay (%), classify the soil using the function above,
    then return its Field Capacity and Wilting Point from your table.
    """
    soil_class = classify_soil_texture(sand, clay, silt)
    if not soil_class:
        return None, None, None  # Could not classify
    
    # Look up the data in your dictionary
    props = soil_data.get(soil_class)
    if props:
        return soil_class, props["field_capacity"], props["wilting_point"]
    else:
        return None, None, None

gauges   = pd.read_csv("Gauges.csv")
soil_all = pd.read_csv("VIC_Soilall.csv")
 
gauges[['Soil Type', 'Field Capacity', 'Wilting Point']] = gauges.apply(
    lambda row: pd.Series(get_soil_properties(row['sand_frac'], row['clay_frac'], row['silt_frac'])),
    axis=1
)
gauges['Crp_frac'] = (gauges['Field Capacity'] / gauges['soil_porosity']) * 0.7
gauges['Pwp_frac'] = gauges['Wilting Point'] / gauges['soil_porosity']
gauges.loc[gauges.Pwp_frac > gauges.Crp_frac, 'Pwp_frac'] = gauges.loc[gauges.Pwp_frac > gauges.Crp_frac, 'Crp_frac']

soil_all = soil_all.merge(gauges[['gauge_id', 'Soil Type', 'Field Capacity', 'Wilting Point', 'Crp_frac', 'Pwp_frac' ]],
               left_on = 'gridcel', right_on='gauge_id', how='left')

soil_all['Wpwp_FRACT1'] = soil_all['Pwp_frac']
soil_all['Wpwp_FRACT2'] = soil_all['Pwp_frac']
soil_all['Wpwp_FRACT3'] = soil_all['Pwp_frac']
soil_all['Wcr_FRACT1']  = soil_all['Crp_frac']
soil_all['Wcr_FRACT2']  = soil_all['Crp_frac']
soil_all['Wcr_FRACT3']  = soil_all['Crp_frac']
soil_all.drop(columns  = ['Soil Type','Field Capacity', 'Wilting Point', 'Crp_frac', 'Pwp_frac', 'gauge_id' ], inplace = True)

soil_all.to_csv("VIC_Soilall.csv", index = False)