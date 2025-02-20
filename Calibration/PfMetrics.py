import numpy as np
import pandas as pd 

def KGE (sim,obs):

    correlation = np.corrcoef(sim,obs)[1,0]

    sim_mean_value = np.mean(sim)
    obs_mean_value = np.mean(obs)
    sim_std_value =  np.std(sim)
    obs_std_value = np.std(obs)
    
    kge = 1.0 - np.sqrt((correlation-1.0)**2.0 + (sim_std_value/obs_std_value - 1.0)**2.0 + (sim_mean_value/obs_mean_value - 1.0)**2.0)
    return kge

def NSE(sim,obs):

    NSE = 1 - np.sum((sim-obs)**2) / np.sum((obs - np.mean(obs))**2)

    return NSE
    
def RMSE(sim,obs):
    if type(obs) == pd.DataFrame:
        obs = obs['Qobs'].to_numpy()
    
    RMSE = np.sqrt(np.mean((sim - obs)**2))
    return RMSE