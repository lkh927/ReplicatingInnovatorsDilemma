import math

def fun6(z1, z2, beta, phi, kappa_inc, delta, year):
    """
    Python version of fun6.c: computes the exit probability from the Old firm.

    Parameters
    ----------
    z1 : float
        EV_old for staying with the Old firm.
    z2 : float
        EV_both for adopting the Old firm.
    beta : float
    phi : float
    kappa_inc : float
    delta : float
    year : float or int
        Year index (matches MATLAB’s 1-based notion).

    Returns
    -------
    z6 : float
        Probability of exiting Old firm.
    """
    # phi + beta * z1
    term_stay = math.exp(phi + beta * z1)
    # phi + beta * z2 - kappa_inc * delta^(year-1)
    term_adopt = math.exp(phi + beta * z2 - kappa_inc * (delta ** (year - 1)))

    z6 = 1.0 / (1.0 + term_stay + term_adopt)
    return z6
