import numpy as np

def fun11(z1, z2, beta, phi, kappa_inc, delta, year):

    ''' Input variables:
        z1 = EV of staying for Old-only firms
        z2 = EV of adopting for Old-only firms
        beta = discount factor, phi = fixed costs, delta = rate of change in sunk cost
        kappa_inc = costs of inovating for incumbents, 
        and year '''

    prhs = [z1, z2, beta, phi, kappa_inc, delta, year]
    nrhs = len(prhs)

    if nrhs != 7:
        raise Warning(f'Error found fun11: 7 inputs required, {nrhs} given')
    
    stay = np.exp(phi + beta * z1)
    adopt = np.exp(phi + beta * z2 - kappa_inc * delta**(year-1))

    z11 = np.log(np.exp(0) + stay + adopt)
    
    return z11