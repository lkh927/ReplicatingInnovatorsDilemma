import numpy as np

'''Calculates the choice probability of Old firm's exit'''

def fun12(z3, beta, phi):

    # Input variables: 
        # z3 = Expected value of staying for Both firms
        # beta = discount factor
        # phi = fixed cost
    
    plhs = [z3, beta, phi]
    nrhs = len(plhs)

    if nrhs != 3:
        print(f'Error found fun12: 3 input arguments required, {nrhs} given')

    z12 = np.log(1 + np.exp(phi + beta * z3))

    return z12
