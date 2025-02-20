# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:55:39 2025

@author: atakallou
"""

import numpy as np
import random
import pandas as pd 
import os
import glob
import shutil
import subprocess
import time
from Routing import routing_model
from model_config import configure_simulation
from ParmChange import Soil_parm_change
from PfMetrics import NSE
from PfMetrics import KGE


def SampleInputMatrix(nrows, bu, bl, iseed):
    """
    Create an input parameter matrix for nrows simulations,
    for npars with bounds bu (upper bound) and bl (lower bound).
    
    distname specifies the initial sampling distribution (default: 'randomUniform').

    Returns:
        np.array: Generated sample matrix.
    """
    npars = bu.shape[0]
    np.random.seed(iseed)  # Set random seed for reproducibility
    
    # Generate random values in [0,1] and scale to bounds
    x = bl + np.random.rand(nrows, npars) * (bu - bl)
    
    return x

# This could be relplaced by your model
# This function only run the function and evaluate that 

def EvalObjF(initial_parm, states,number):
    gauges =  pd.read_csv("Gauges2.csv")

    gauge = gauges.gauge_id.unique()[number]
    Soil_parm_change(initial_parm, gauge)
    configure_simulation(
    gauge, startyear = 1979, startmonth = 1, startday = 2, 
    endyear = 2019, endmonth = 3, endday = 13,
    stateyear = 1985, statemonth = 1, stateday = 1,
    )
    # Define the working directory path
    directory = os.path.join(os.getcwd(), "CONUS", gauge.astype(str).zfill(8))
    script_path = os.path.join(directory, "submit_VIC.job")
    # Submit the SLURM job using sbatch
    # os.system(f"sbatch {script_path}")
    subprocess.run(['sbatch', '--wait', f'{script_path}'])

    #rout baseflow and runoff
    gauge        =  str(gauge).zfill(8)
    sim_path     = glob.glob(os.path.join("/mh1/Atakallou/VIC/CONUS", f'{gauge}', "results",'*.txt'))
    sim          = pd.read_csv(sim_path[0],sep = '\s+', skiprows=2)
    rout_inits   = np.array([0.5,0.5,0.5])
    Qflow    = np.zeros(len(sim))


    for idx in range(len(sim)):
        Qflow[idx], states[3],states[4],states[5] = routing_model(runoffs[idx],baseflows[idx],initial_parm[-1],states[3],states[4],states[5])
    sim['Qflow'] = Qflow
    obs_path    =  os.path.join("/mh1/Atakallou/VIC/Forcing/hourly_kretzert/usgs_streamflow", f"{gauge}-usgs-hourly.csv")
    obs         =  pd.read_csv(obs_path)
    obs['date'] =  pd.to_datetime(obs['date'])
    full_range  = pd.date_range(start=obs['date'].min(), end=obs['date'].max(), freq='h')
    obs         = obs.set_index('date').reindex(full_range).reset_index()
    obs.rename({'index': 'date'}, axis=1, inplace=True)
    obs.date = pd.to_datetime(obs.date)
    obs = obs.dropna(subset=['QObs(mm/h)'])
    sim["hour"] = sim["SEC"] / 3600
    sim.hour    = sim.hour.astype(int)
    sim['date'] = pd.to_datetime(sim[['YEAR', 'MONTH', 'DAY', 'hour']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
    sim = sim[sim['date'].isin(obs['date'])]
    sim = sim[sim.date >= pd.to_datetime("1980-10-01")]
    obs = obs[obs['date'].isin(sim['date'])]
    value= KGE(sim['Qflow'].to_numpy(), obs['QObs(mm/h)'].to_numpy())
    with open(f"{number}_KGE.txt", "a") as file:
        file.write(f"{value}\n")  # Adds the value at the end with a newline
    f = 1 - KGE(sim['Qflow'].to_numpy(), obs['QObs(mm/h)'].to_numpy())
    return f
    


def cceua(s,sf,bl,bu,icall,maxn,iseed , states,number):
#  This is the subroutine for generating a new point in a simplex
#
#   s(.,.) = the sorted simplex in order of increasing function values
#   s(.) = function values in increasing order
#
# LIST OF LOCAL VARIABLES
#   sb(.) = the best point of the simplex
#   sw(.) = the worst point of the simplex
#   w2(.) = the second worst point of the simplex
#   fw = function value of the worst point
#   ce(.) = the centroid of the simplex excluding wo
#   snew(.) = new point generated from the simplex
#   iviol = flag indicating if constraints are violated
#         = 1 , yes
#         = 0 , no

    nps,nopt=s.shape
    alpha = 1.0
    beta = 0.5

    # Assign the worst points:
    sw, fw = s[-1, :], sf[-1]

    # Compute the centroid of the simplex excluding the worst point:
    ce= np.mean(s[:-1,:],axis=0)

    # Attempt a reflection point
    snew = ce + alpha*(ce-sw)

    # Check if value is outside the bounds
    # Check upper lower bound
    # If out of bounds, resample within bounds

    if (snew < bl).any() or (snew > bu).any():
        snew = SampleInputMatrix(1, bu, bl, iseed)[0]  # Ensure new sample is within bounds

        
##    fnew = functn(nopt,snew);
    fnew = EvalObjF(snew, states,number)
    icall += 1

    # Reflection failed; now attempt a contraction point:
    if fnew > fw:
        snew = sw + beta*(ce-sw)
        fnew = EvalObjF(snew, states,number)
        icall += 1

    # Both reflection and contraction have failed, attempt a random point;
        if fnew > fw:
            snew = SampleInputMatrix(1,bu,bl,iseed)[0]  #checken!!
            fnew = EvalObjF(snew, states,number)
            icall += 1

    # END OF CCE
    return snew,fnew,icall








def sceua(x0,bl,bu,maxn,kstop,pcento,peps,ngs,iseed, states,number):
# This is the subroutine implementing the SCE algorithm,
# written by Q.Duan, 9/2004 - converted to python by Van Hoey S.2011
#
# Definition:
#  x0 = the initial parameter array at the start; np.array
#     = the optimized parameter array at the end;
#  f0 = the objective function value corresponding to the initial parameters
#     = the objective function value corresponding to the optimized parameters
#  bl = the lower bound of the parameters; np.array
#  bu = the upper bound of the parameters; np.array
#  iseed = the random seed number (for repetetive testing purpose)
#  iniflg = flag for initial parameter array (=1, included it in initial
#           population; otherwise, not included)
#  ngs = number of complexes (sub-populations)
#  npg = number of members in a complex
#  nps = number of members in a simplex
#  nspl = number of evolution steps for each complex before shuffling
#  mings = minimum number of complexes required during the optimization process
#  maxn = maximum number of function evaluations allowed during optimization
#  kstop = maximum number of evolution loops before convergency
#  percento = the percentage change allowed in kstop loops before convergency

# LIST OF LOCAL VARIABLES
#    x(.,.) = coordinates of points in the population
#    xf(.) = function values of x(.,.)
#    xx(.) = coordinates of a single point in x
#    cx(.,.) = coordinates of points in a complex
#    cf(.) = function values of cx(.,.)
#    s(.,.) = coordinates of points in the current simplex
#    sf(.) = function values of s(.,.)
#    bestx(.) = best point at current shuffling loop
#    bestf = function value of bestx(.)
#    worstx(.) = worst point at current shuffling loop
#    worstf = function value of worstx(.)
#    xnstd(.) = standard deviation of parameters in the population
#    gnrng = normalized geometric mean of parameter ranges
#    lcs(.) = indices locating position of s(.,.) in x(.,.)
#    bound(.) = bound on ith variable being optimized
#    ngs1 = number of complexes in current population
#    ngs2 = number of complexes in last population
#    iseed1 = current random seed
#    criter(.) = vector containing the best criterion values of the last
#                10 shuffling loops

    # Initialize SCE parameters:
    nopt=x0.size
    npg=2*nopt+1
    nps=nopt+1
    nspl=npg
    npt=npg*ngs
    iniflg = 1
    bound = bu-bl  #np.array

    # Create an initial population to fill array x(npt,nopt):
    x = SampleInputMatrix(npt,bu,bl,iseed)
    if iniflg==1:
        x[0,:]=x0

    nloop=0
    icall=0
    xf=np.zeros(npt)
    #evaluate all the population
    for i in range (npt):
        xf[i] = EvalObjF(x[i,:],states, number)
        icall += 1


    # Sort the population in order of increasing function values;
    idx = np.argsort(xf)
    xf = np.sort(xf)
    x=x[idx,:]

    # Record the best and worst points;
    bestx, bestf = x[0, :], xf[0]



    # Computes the normalized geometric range of the parameters
    gnrng=np.exp(np.mean(np.log((np.max(x,axis=0)-np.min(x,axis=0))/bound)))



    # Check for convergency;
    if icall >= maxn:
        print ('*** OPTIMIZATION SEARCH TERMINATED BECAUSE THE LIMIT')
        print ('ON THE MAXIMUM NUMBER OF TRIALS ')
        print (maxn)
        print ('HAS BEEN EXCEEDED.  SEARCH WAS STOPPED AT TRIAL NUMBER:')
        print (icall)
        print ('OF THE INITIAL LOOP!')

    if gnrng < peps:
        print ('THE POPULATION HAS CONVERGED TO A PRESPECIFIED SMALL PARAMETER SPACE')

    # Begin evolution loops:
    nloop = 0
    criter=[]
    criter_change=1e+5

    while icall<maxn and gnrng>peps and criter_change>pcento:
        nloop+=1

        # Loop on complexes (sub-populations);
        for igs in range(ngs):
            # Partition the population into complexes (sub-populations);
            cx=np.zeros((npg,nopt))
            cf=np.zeros((npg))

            k1=np.array(range(npg))
            k2=k1*ngs+igs
            cx[k1,:] = x[k2,:]
            cf[k1] = xf[k2]

            # Evolve sub-population igs for nspl steps:
            for loop in range(nspl):

                # Select simplex by sampling the complex according to a linear
                # probability distribution
                lcs=np.array([0]*nps)
                lcs[0] = 1
                for k3 in range(1,nps):
                    for i in range(1000):
##                        lpos = 1 + int(np.floor(npg+0.5-np.sqrt((npg+0.5)**2 - npg*(npg+1)*random.random())))
                        lpos = int(np.floor(npg+0.5-np.sqrt((npg+0.5)**2 - npg*(npg+1)*random.random())))
##                        idx=find(lcs(1:k3-1)==lpos)
                        idx=(lcs[0:k3]==lpos).nonzero()  
                        if idx[0].size == 0:
                            break

                    lcs[k3] = lpos
                lcs.sort()

                # Construct the simplex:
                s = np.zeros((nps,nopt))
                s=cx[lcs,:]
                sf = cf[lcs]

                snew,fnew,icall=cceua(s,sf,bl,bu,icall,maxn,iseed, states, number)

                # Replace the worst point in Simplex with the new point:
                s[-1,:] = snew
                sf[-1] = fnew

                # Replace the simplex into the complex;
                cx[lcs,:] = s
                cf[lcs] = sf

                # Sort the complex;
                idx = np.argsort(cf)
                cf = np.sort(cf)
                cx=cx[idx,:]

            # End of Inner Loop for Competitive Evolution of Simplexes
            #end of Evolve sub-population igs for nspl steps:

            # Replace the complex back into the population;
            x[k2,:] = cx[k1,:]
            xf[k2] = cf[k1]

        # End of Loop on Complex Evolution;

        # Shuffled the complexes;
        idx = np.argsort(xf)
        xf = np.sort(xf)
        x=x[idx,:]

        # Record the best and worst points;
        bestx=x[0,:]
        bestf=xf[0]

        # Computes the normalized geometric range of the parameters
        gnrng=np.exp(np.mean(np.log((np.max(x,axis=0)-np.min(x,axis=0))/bound)))

        criter=np.append(criter,bestf)

        if nloop >= kstop: 
            criter_change= np.abs(criter[nloop-1]-criter[nloop-kstop])*100
            criter_change= criter_change/np.mean(np.abs(criter[nloop-kstop:nloop]))




    # END of Subroutine sceua
    return bestx,bestf

























