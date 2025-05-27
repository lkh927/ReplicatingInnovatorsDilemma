import numpy as np

def fun13(z4, beta, phi):

    ''' Input variables:
        z4 = EV of staying for both firms
        beta = discount factor
        phi = fixed costs '''

    prhs = [z4, beta, phi]
    nrhs = len(prhs)

    if nrhs != 3:
        raise Warning(f'Error found fun13: 3 input arguments required, {nrhs} given')

    stay = np.exp(phi + beta * z4)

    # Bellman Equation of New-only firms 
    z13 = np.log(np.exp(0) + stay)

    return z13