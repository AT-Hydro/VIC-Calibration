# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 14:57:14 2025

@author: atakallou
"""
import numpy as np
import os


def read_state(Ens_folder,date):
    year, month, day = str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2)
    state_file_path = os.path.join(Ens_folder, "States", f"States_{year}{month}{day}_00000")
    rout_file_path = os.path.join(Ens_folder, "results", f"Rout_{year}{month}{day}.npy")
    rout_states      = np.load(rout_file_path)
    with open(state_file_path, "r") as f:
        lines = f.readlines()
    state_line = lines[3].split(" ")
    states = np.array([float(state_line[2]), float(state_line[3]), float(state_line[4]), float(state_line[12]), rout_states[0], rout_states[1], rout_states[2]])
    return states

def write_state(Ens_folder,date, states):
    year, month, day = str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2)
    state_file_path = os.path.join(Ens_folder, "States", f"States_{year}{month}{day}_00000")
    rout_file_path = os.path.join(Ens_folder, "results", f"Rout_{year}{month}{day}.npy")
    rout_states      = np.load(rout_file_path)
    with open(state_file_path, "r") as f:
        lines = f.readlines()
    state_line = lines[3].split(" ")
    state_line[2] = str(states[0])
    state_line[3] = str(states[1])
    state_line[4] = str(states[2])
    state_line[12] = str(states[3])
    rout_states[0]= states[4]
    rout_states[1]= states[5]
    rout_states[2]= states[6]
    lines[3] = " ".join(state_line) 
    with open(state_file_path, "w") as f:
        f.writelines(lines)
    np.save(rout_file_path , rout_states)
    return 1