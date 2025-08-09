# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 18:49:01 2025

@author: atakallou
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from varstool import VARS, GVARS, Model


def ishigami(x, a=7, b=0.1):
    '''Ishigami test function'''
    # check whether the input x is a dataframe
    
    if not isinstance(x, (pd.core.frame.DataFrame, pd.core.series.Series, np.ndarray, list)):
        raise TypeError('`x` must be of type pandas.DataFrame, numpy.ndarray, pd.Series, or list')
    
    if len(x) > 3:
        raise ValueError('`x` must have only three arguments at a time')
    
    return np.sin(x[0]) + a*(np.sin(x[1])**2) + b*(x[2]**4)*np.sin(x[0])

ishigami_model = Model(ishigami)

x=pd.Series({#name  #value
             'x1'   : 0 ,
             'x2'   : 0 ,
             'x3'   : 0 ,
             })
ishigami_model(x)

# Define Experiment 1

my_parameters = { 'x1': [ -3.14, 3.14 ], 
                  'x2': [ -3.14, 3.14 ], 
                  'x3': [ -3.14, 3.14 ], }

experiment_1 = VARS(parameters     = my_parameters,
                    num_stars      = 100,
                    delta_h        = 0.1,
                    ivars_scales   = (0.1,0.5),
                    sampler        = 'plhs',
                    seed           = 123456789,
                    model          = ishigami_model,
                    bootstrap_flag = False,
                    bootstrap_size = 100,
                    bootstrap_ci   = 0.9,
                    grouping_flag  = False,
                    num_grps       = 2,
                    report_verbose = True,
                    )


experiment_1.run_online()