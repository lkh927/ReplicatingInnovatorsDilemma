import numpy as np

def fun6(z1, z2, beta, phi, kappa_inc, delta, year):
    """
    Computes the exit probability from the Old firm.
    z1 : EV_old for staying with the Old firm.
    z2 : EV_both for adopting the Old firm.
    beta : Discount factor
    phi : Fixed costs
    kappa_inc : Sunk cost of investment, incumbents
    delta : Rate of change in the sunk cost of investment
    year: Year

    Returns z6 : Probability of exiting Old firm.
    """
    # phi + beta * z1
    stay = np.exp(phi + beta * z1)
    # phi + beta * z2 - kappa_inc * delta^(year-1)
    adopt = np.exp(phi + beta * z2 - kappa_inc * (delta ** (year - 1)))

    z6 = np.exp(0) / (np.exp(0) + stay + adopt)
    return z6
