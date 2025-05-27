import numpy as np

def fun8(z3, beta, phi):
    ''' Input variables:
        z3 = EV of staying for Both firms
        beta = discount factor
        phi = fixed costs 
        Output variables:
        z8 = probability of Both firm's exit
    '''
    prhs = [z3, beta, phi]
    nrhs = len(prhs)
    if nrhs != 3:
        raise Warning(f'Error found fun8: 3 input arguments required, only {nrhs} given')
    
    stay = np.exp(phi + beta * z3)

    # Probability of exit for Both firms
    z8 = np.exp(0) / (np.exp(0) + stay)

    return z8