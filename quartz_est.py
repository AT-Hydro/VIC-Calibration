# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 16:18:51 2025

@author: atakallou
"""
import pandas as pd

def estimate_quartz_content(sand, silt, clay):
    """
    Estimates the quartz content (fraction) of a soil sample based on
    the percentage of sand, silt, and clay.
    
    :param sand: Percent sand (0-100)
    :param silt: Percent silt (0-100)
    :param clay: Percent clay (0-100)
    :return: Estimated quartz content as a fraction (0-1)
    """


    # Assign typical quartz fractions
    quartz_sand = 0.9   # 80-100% quartz
    quartz_silt = 0.5   # 40-60% quartz
    quartz_clay = 0.2   # 10-30% quartz

    # Weighted average based on composition
    quartz_content = (sand * quartz_sand + silt * quartz_silt + clay * quartz_clay) / 100

    return round(quartz_content, 3)  # Rounded to 3 decimals
gauges   = pd.read_csv("Gauges.csv")
soil_all = pd.read_csv("VIC_Soilall.csv")

gauges['quartz_estimated'] = gauges.apply(
    lambda row: estimate_quartz_content(row['sand_frac'], row['clay_frac'], row['silt_frac']),
    axis=1
)
soil_all = soil_all.merge(
    gauges[['gauge_id', 'quartz_estimated']], 
    left_on='gridcel', 
    right_on='gauge_id', 
    how='left'
)

soil_all[['quartz1', 'quartz2', 'quartz3']] = soil_all[['quartz1', 'quartz2', 'quartz3']].fillna(soil_all['quartz_estimated'])
soil_all.quartz1 = soil_all['quartz_estimated']
soil_all.quartz2 = soil_all['quartz_estimated']
soil_all.quartz3 = soil_all['quartz_estimated']

soil_all.drop(columns=['gauge_id','quartz_estimated'], inplace=True)
soil_all.to_csv("VIC_Soilall.csv", index = False)