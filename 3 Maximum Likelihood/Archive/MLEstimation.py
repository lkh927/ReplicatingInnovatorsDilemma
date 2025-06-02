
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.io import loadmat
from Likelihood import Likelihood
from functools import partial

Pi = loadmat('CheckPi.mat')['Pi']

T = Pi.shape[0]
beta = 0.88      # Discount factor
delta = 0.9388   # Decline in SC
scaling = 1000   # Scaling factor
iterMLE = 1

print(f"  -----------------------------------------")
print(f" | STRATEGIC (RATIONAL-EXPECTATIONS) MODEL |")
print(f"  -----------------------------------------")

print(f" ----- Basic parameters to be \"calibrated\" -----")
print(f"   Profit/value scaling      :     {scaling:4.0f}")
print(f"   Discount factor (beta)    :     {beta:1.4f}")
print(f"   Adoption cost drop (delta):     {delta:1.4f}")
print(" -----------------------------------------------\n")

# Rescale profits
Pi = Pi / scaling

# Terminal Values
V = np.zeros((T, 3, 12, 12, 15))
V[T-1,:,:,:,:] = Pi[T-1,:,:,:,:] / (1 - beta)

# Initialize Solutions
EV = np.zeros((T, 5, 12, 12, 15))
Policy = np.zeros((T-1, 5, 12, 12, 15))

# MLE Estimation
x0 = [1, 1, 1]
options = {'disp': True, 'maxiter': 1000, 'xatol': 1e-4, 'fatol': 1e-8}

objective_function = partial(Likelihood, beta=beta, delta=delta, Pi=Pi, V=V, EV=EV, Policy=Policy, State=State, Exit=Exit, Adopt=Adopt, T=T, iterMLE=iterMLE, output_type=1)

res = minimize(objective_function, x0, method='Nelder-Mead', options=options)
Theta = res.x

# Numerical derivatives for standard errors
perturb = 0.001
logL = Likelihood(Theta, 2)
logLderiv = np.zeros((1, 3))

for k in range(3):
    Theta_perturbed = np.copy(Theta)
    Theta_perturbed[k] += perturb
    logL_perturbed = Likelihood(Theta_perturbed, 2)
    logLderiv[0, k] = (logL_perturbed - logL) / perturb

# Derive the Value estimate
Vhat = np.linalg.inv(logLderiv.T @ logLderiv)

print(f"\n ----- Maximum Likelihood Estimation Results for (phi & kappa_inc) -----")
print(f" Coeff.: " + " ".join([f"{v:8.8f}" for v in Theta]))
print(f" S.E.  : " + " ".join([f"{v:8.8f}" for v in np.sqrt(np.diag(Vhat))]))
print(f" -----------------------------------------------------------------------\n")

