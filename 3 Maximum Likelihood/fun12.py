import numpy as np

def fun12(z3, beta, phi):
    '''Input variables: 
        z3 = EV of staying for Both firms
        beta = discount factor
        phi = fixed cost '''
    
    plhs = [z3, beta, phi]
    nrhs = len(plhs)

    if nrhs != 3:
        raise Warning(f'Error found fun12: 3 input arguments required, {nrhs} given')

    stay = np.exp(phi + beta * z3)

    z12 = np.log(np.exp(0) + stay)

    return z12
