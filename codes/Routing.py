# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 22:16:20 2025

@author: atakallou
"""

import numpy as np


def routing_model(runoff,baseflow, Kq, xquick1,xquick2,xquick3):
    xquick1 = (1-Kq)*xquick1 + (1-Kq)*runoff
    outflow1 = (Kq/(1-Kq))*xquick1
    xquick2 = (1-Kq)*xquick2 + (1-Kq)* outflow1
    outflow2 = (Kq/(1-Kq))*xquick2
    xquick3 = (1-Kq)*xquick3 + (1-Kq)* outflow2
    outflow3 = (Kq/(1-Kq))*xquick3
    streamflow =  outflow3 + baseflow
    return streamflow, xquick1, xquick2, xquick3