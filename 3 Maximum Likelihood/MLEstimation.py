
import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
import logging

# Logging setup (replaces diary in MATLAB)
logging.basicConfig(filename='Diary.log', level=logging.INFO, format='%(message)s')
log = logging.info

Pi = loadmat('CheckPi.mat')['Pi']

T = Pi.shape[0]
beta = 0.88      # Discount factor
delta = 0.9388   # Decline in SC
scaling = 1000   # Scaling factor
iterMLE = 1

log("\n  -----------------------------------------")
log(" | STRATEGIC (RATIONAL-EXPECTATIONS) MODEL |")
log("  -----------------------------------------")

log("\n ----- Basic parameters to be \"calibrated\" -----")
log(f"   Profit/value scaling      :     {scaling:4.0f}")
log(f"   Discount factor (beta)    :     {beta:1.4f}")
log(f"   Adoption cost drop (delta):     {delta:1.4f}")
log(" -----------------------------------------------\n")

# Rescale profits
Pi = Pi / scaling

# Terminal Values
V = np.zeros((T, 3, 12, 12, 15))
V[T-1,:,:,:,:] = Pi[T-1,:,:,:,:] / (1 - beta)

# Initialize Solutions
EV = np.zeros((T, 5, 12, 12, 15))
Policy = np.zeros((T-1, 5, 12, 12, 15))

# Placeholder for Likelihood function (needs to be defined)
def Likelihood(theta, flag):
    # Dummy implementation – to be replaced
    phi, kappa_inc, kappa_ent = theta
    LL = -np.sum(np.square(theta))  # Just a dummy negative log-likelihood
    return -LL  # Negative for minimization

# MLE Estimation
x0 = [1, 1, 1]
options = {'disp': True, 'maxiter': 1000, 'xatol': 1e-4, 'fatol': 1e-8}

res = minimize(lambda theta: Likelihood(theta, 1), x0, method='Nelder-Mead', options=options)
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

Vhat = np.linalg.inv(logLderiv.T @ logLderiv)

log("\n ----- Maximum Likelihood Estimation Results for (phi & kappa_inc) -----")
log(" Coeff.: " + " ".join([f"{v:8.8f}" for v in Theta]))
log(" S.E.  : " + " ".join([f"{v:8.8f}" for v in np.sqrt(np.diag(Vhat))]))
log(" -----------------------------------------------------------------------\n")

