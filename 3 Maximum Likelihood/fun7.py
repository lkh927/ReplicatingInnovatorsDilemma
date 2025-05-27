import numpy as np

def fun7(z1, z2, beta, phi, kappa_inc, delta, year):

    ''' Input variables:
        z1 = EV of staying for Old-only firms 
        z2 = EV of adopting for Old-only firms
        beta = discount factor, phi = fixed costs, delta = rate of change in fixed costs
        kappa_inc = costs of adopting for incumbents, and year 
        
        Output variables:
        z7 = probability of Old-only firm adopting '''
    
    prhs = [z1, z2, beta, phi, kappa_inc, delta, year]
    nrhs = len(prhs)
    if nrhs != 7:
        raise Warning(f'Error found fun7: 7 input arguments required, only {nrhs} given')
    
    stay = np.exp(phi + beta * z1)
    adopt = np.exp(phi + beta * z2 - kappa_inc * (delta ** (year-1)))

    # Probability of Old-only firm adopting
    z7 = adopt / (np.exp(0) + stay + adopt)

    return z7
    
