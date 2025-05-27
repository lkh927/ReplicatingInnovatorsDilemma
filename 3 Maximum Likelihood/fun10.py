import numpy as np

def fun10(z5, beta, kappa_ent, delta, year):
    '''
    Input variables:
        z5 = EV of entering for Potential Entrants,
        beta = discount factor, delta = rate of change in sunk costs,
        kappa_ent = costs of innovating for entrants,
        and year     
    Output variables:
        z10 = Probability of Potential Entrants entry 
    '''  
    prhs = [z5, beta, kappa_ent, delta, year]
    nrhs = len(prhs)
    if nrhs != 5:
        raise Warning(f'Error found fun10: 5 input arguments required, only {nrhs} given')
    
    enter = np.exp(beta * z5 - kappa_ent * (delta ** (year-1)))

    # Probability of Potential Entrant entry, exp(0) = stay out
    z10 = enter / (np.exp(0) + enter)

    return z10
