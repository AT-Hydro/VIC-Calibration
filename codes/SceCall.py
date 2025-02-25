# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:49:21 2025

@author: atakallou
"""


import numpy as np
from SCEUA import sceua



# SCE HyperParameters
maxn=10000
kstop=30
pcento=0.001
peps=0.001
iseed= 42
ngs=5


# define the upper and lower limit for the parameters
bl=np.array([-5 ,-5])
bu=np.array([5 ,5])
x0=np.array([2.5 ,2.5])
bestx,bestf = sceua(x0,bl,bu,maxn,kstop,pcento,peps,ngs,iseed = 20)