import numpy as np

''' Calcualtes the choice probability of '''

def fun13(z4, beta, phi):

    prhs = [z4, beta, phi]
    nrhs = len(prhs)

    if nrhs != 3:
        print(f'Error found fun13: 3 input arguments required, {nrhs} given')

    # Initialize solution container
    z13 = np.log(1 + np.exp(phi + beta * z4))

    return z13