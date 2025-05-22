# Confidence intervals for Likelihood ratios

# Setup
import numpy as np
import pandas as pd

State = pd.read_csv('/Users/annaabildskov/Desktop/Documents/Polit/3. sem KA/Dyn. Prog/TP_local/Translated/1 Summary Statistics/Data/State.csv')
Pi = pd.read_csv('/Users/annaabildskov/Desktop/Documents/Polit/3. sem KA/Dyn. Prog/TP_local/Translated/1 Summary Statistics/Data/Pi.csv')

# Parameters taken as given
scaling = 1000          # For re-scaling of profits
beta = 0.80             # Discount factor (not explicitly estimated in the paper)
delta = 1.10            # Decline in sunk costs, SC 
npe = 4                 # Number of potential entrants (assumption, constant for all years)
State.iloc[:,3] = npe * np.ones(18,1)
T = len(State[0])       # Number of periods (years)

# Simulation parameters
phi = -0.147362421730779
kappa_inc = 1.24394591815957
kappa_ent = 2.25381667717391
Theta = [phi, kappa_inc, kappa_ent]

# def print():

# Import Pi for scaling of profits
Pi = Pi / scaling

# Terminal Values
V = np.zeros(T, 3, 12, 12, 15)                # Values 
V[T,:,:,:,:] = Pi[T,:,:,:,:] / (1 - beta)     # Values scaled down by Pi(T)

# Initialize Solutions
EV = np.zeros(T, 5, 12, 12, 15)                        # Expected Values over states
Choice_probabilities = np.zeros(T-1, 5, 12, 12, 15)    # Choice probabilities

# Initialize for solving the model and evaluating LL
LL_1 = np.zeros(101,1)
LL_2 = np.zeros(101,1)
LL_3 = np.zeros(101,1)
grid_1 = np.zeros(101,1)
grid_2 = np.zeros(101,1)
grid_3 = np.zeros(101,1)