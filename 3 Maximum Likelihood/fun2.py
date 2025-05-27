# Calcutaes the transitions probability of adopting for old only firms

# Setup
import numpy as np
from math import factorial

def factorial(n):
    return np.math.factorial(n)


def fun2(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):

    '''
    Input variables:
        z6, z7, z8, z9, z10 = choice probabilities, fun6 - fun 10
        No = integer,  # Old-only firms
        Nb = integer, # of Both firms
        Nn = integer, # of New firms
        Npe = integer, # of Potential Entrants
        Npe_prime = integer, # of Potential Entrants next period
        Vprime = array of size 6480,1 with value function results over time, type and # of firms

    Output:
        z2 = EV of adopting for Old-only firms
    '''

    prhs = [z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime]
    nrhs = len(prhs)

    # checks for correct inputs
    if nrhs != 11:
        raise Warning(f'Error fun2: 11 input arguments required, only {nrhs} given')
    if len(prhs[10]) != 6480:
        raise Warning(f'Error fun2: Vprime must have 6480 rows, it has {len(prhs[9])}')
    if prhs[10].any() == np.nan:
        raise Warning(f'Error fun2: Vprime must have 6480 elements')


    def getBA2(z6, z7, z8, z9, z10, No, Nb, Nn, Npe):
        # Step 1: compute BA2

        # Initialize solution container
        BA2 = np.zeros((12, 12, 12, 12, 15))       # xo, eb, xb, xn, en
        for xo in range(No):
            for eb in range(1, No+1 - xo):
                for xb in range(Nb+1):
                    for xn in range(Nn+1):
                        for en in range(Npe+1):
                            if No > 1:
                                BA2[xo + 11*eb + (11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en] = \
                                (factorial(No) / (factorial(xo) * factorial(No-xo))) \
                                * (factorial(No-xo) / (factorial(eb-1) * factorial(No-xo-(eb-1)))) \
                                * (z6**xo) * (z7**(eb - 1)) * ((1 - z6 - z7)**(No - xo - (eb - 1))) \
                                * (factorial(Nb+1) / (factorial(xb) * factorial(Nb+1-xb))) \
                                * (z8**xb) * ((1 - z8)**(Nb+1 - xb)) \
                                * (factorial(Nn+1) / (factorial(xn) * factorial(Nn+1-xn))) \
                                * (z9**xn) * ((1-z9)**(Nn+1-xn)) \
                                * (factorial(Npe+1) / (factorial(en) * factorial(Npe+1-en))) \
                                * (z10**en) * ((1-z10)**(Npe+1-en))

                            else:
                                BA2[0 + 12*0 + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*en] = \
                                (factorial(Nb+1) / (factorial(xb) * factorial(Nb+1-xb))) \
                                * (z8**xb) * ((1-z8)**(Nb+1-xb)) \
                                * (factorial(Nn+1) / (factorial(xn) * factorial(Nn+1-xn))) \
                                * (z9**xn) * ((1-z9)**(Nn+1-xn)) \
                                * (factorial(Npe+1) / (factorial(en) * factorial(Npe+1-en))) \
                                * (z10**en) * ((1-z10)**(Npe+1-en))
        
        return BA2

    def getBS2(No, Nb, Nn, Npe, Npe_prime):
        # Step 2: map BA2 to future state probabilities BS2
        npe_prime = Npe_prime

        # Initialize solution container
        BS2 = np.zeros((12, 12, 15, 15))  # no', nb', nn', npe'

        # Loop over all possible combinations of states 
        for xo in range(No):
            for eb in range(1, No+1 - xo):
                for xb in range(Nb+1):
                    for xn in range(Nn+1):
                        for en in range(Npe+1):

                            xo = max(xo, 0)
                            eb = max(eb, 0)

                            no_prime = No - xo - eb
                            no_prime = max(0, no_prime)
                            no_prime = min(no_prime, 11)

                            nb_prime = Nb - xb + eb
                            nb_prime = max(0, nb_prime)
                            nb_prime = min(nb_prime, 11)

                            nn_prime = Nn - xn + en
                            nn_prime = max(0, nn_prime)
                            nn_prime = min(nn_prime, 14)

                            BS2[no_prime + 11*nb_prime + (11*11)*nn_prime + (11*11*14)*npe_prime] += \
                                getBA2[xo + 11*eb + (11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en]
                        
        return BS2


    def getEV2(Npe_prime, Vprime):
        npe_prime = Npe_prime

        BS2 = getBS2(No, Nb, Nn, Npe, Npe_prime)
        EV2 = 0.0     # Solution container
        for no_prime in range(12):
            for nb_prime in range(12):
                for nn_prime in range(15):
                    EV2 += BS2[no_prime + 11*nb_prime + (11*11)*nn_prime + (11*11*14)*npe_prime] \
                    * Vprime[1 + 2*no_prime + (2*11)*nb_prime + (2*11*11)*nn_prime]

        return EV2

    # Step 3: calculate expected value z2
    z2 = getEV2(Npe_prime, Vprime)

    return z2