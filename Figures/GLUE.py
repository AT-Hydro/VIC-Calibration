# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 17:19:12 2025

@author: atakallou
"""

import numpy as np
import pyGLUE


def linear_model(params, x):
    a, b = params
    return a * x + b

def nse(observed, simulated):
    return 1 - np.sum((observed - simulated) ** 2) / np.sum((observed - np.mean(observed)) ** 2)

# True parameters
true_params = [2.0, 5.0]

# Input data
x_data = np.linspace(0, 10, 50)

# Generate observations with noise
np.random.seed(42)  # For reproducibility
observations = linear_model(true_params, x_data) + np.random.normal(0, 1.0, size=x_data.shape)




# Define parameter ranges
param_ranges = {
    'a': [0.0, 4.0],
    'b': [0.0, 10.0]
}

# Number of samples
n_samples = 1000

# Generate random samples
samples = np.random.uniform(
    low=[param_ranges['a'][0], param_ranges['b'][0]],
    high=[param_ranges['a'][1], param_ranges['b'][1]],
    size=(n_samples, 2)
)

# Evaluate model and compute likelihoods
likelihoods = []
for params in samples:
    simulated = linear_model(params, x_data)
    likelihood = nse(observations, simulated)
    likelihoods.append(likelihood)

likelihoods = np.array(likelihoods)

# Define threshold for behavioral models
threshold = 0.5  # For example, NSE > 0.5

# Select behavioral parameter sets
behavioral_indices = np.where(likelihoods > threshold)[0]
behavioral_params = samples[behavioral_indices]
