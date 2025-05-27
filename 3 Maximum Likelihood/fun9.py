import numpy as np

def fun9(z4, beta, phi):
    ''' 
    Input variables:
        z4 = EV of staying for New-only firms,
        beta = discount factor,
        phi = fixed costs    
    Output variables:
        z9 = probability of New-only firms exit
    '''
    prhs = [z4, beta, phi]
    nrhs = len(prhs)
    if nrhs != 3:
        raise Warning(f'Error found fun9: 3 input arguments require, only {nrhs} given')
    
    stay = np.exp(phi + beta * z4)

    # Probability of New firm's exit
    z9 = np.exp(0) / (np.exp(0) + stay)

    return z9