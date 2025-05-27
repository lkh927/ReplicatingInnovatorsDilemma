# Calcutaes the transitions probability of staying for old only firms

# Setup
import numpy as np
from math import factorial

def fun1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):
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
        z1 = EV of staying for Old-only firms
    '''

    prhs = [z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime]
    nrhs = len(prhs)

    # checks for correct inputs
    if nrhs != 11:
        raise Warning(f'Error fun1: 11 input arguments required, only {nrhs} given')
    if prhs[10].size != 6480:
        raise Warning(f'Error fun1: Vprime must have 6480 rows, it has {prhs[10].size}')
    if np.isnan(prhs[10]).any():
        raise Warning(f'Error fun1: Vprime must have 6480 elements')


    def getBA1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe):
        '''
            xo = # of exits, old firms
            eb = # entry of both - aka # of adopts
            xb = # exit both firms
            xn = # exit new firms
            en = # entry potential firms
        '''

        BA1 = np.zeros((12*12*12*15*5))  # xo, eb, xb, xn, en
        for xo in range(No):
            for eb in range(No-xo):
                for xb in range(Nb+1):
                    for xn in range(Nn+1):
                        for en in range(Npe+1):
                            if No > 1:      # if number of old firms > 1
                                            # Intuitively: Ba1[xo][eb][xb][xn][en]
                                BA1[xo + 11*eb +(11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en] = (factorial(No) / (factorial(xo) * factorial(No - xo))) \
                                * (factorial(No - xo) / (factorial(eb) * factorial(No - xo - eb))) \
                                * z6**xo * z7**eb * ((1 - z6 - z7)**(No - xo - eb)) \
                                * (factorial(Nb + 1) / (factorial(xb) * factorial(Nb + 1 - xb))) \
                                * z8**xb * ((1 - z8)**(Nb + 1 - xb)) \
                                * (factorial(Nn + 1) / (factorial(xn) * factorial(Nn + 1 - xn))) \
                                * z9**xn * ((1 - z9)**(Nn + 1 - xn)) \
                                * (factorial(Npe + 1) / (factorial(en) * factorial(Npe + 1 - en))) \
                                * z10**en * ((1 - z10)**(Npe + 1 - en))
                            else:
                                BA1[0 + 11*0 + (11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en] = \
                                (factorial(Nb + 1) / (factorial(xb) * factorial(Nb + 1 - xb))) \
                                * z8**xb * ((1 - z8)**(Nb + 1 - xb)) \
                                * (factorial(Nn + 1) / (factorial(xn) * factorial(Nn + 1 - xn))) \
                                * z9**xn * ((1 - z9)**(Nn + 1 - xn)) \
                                * (factorial(Npe + 1) / (factorial(en) * factorial(Npe + 1 - en))) \
                                * z10**en * ((1 - z10)**(Npe + 1 - en))
        return BA1


    def getBS1(No, Nb, Nn, Npe, Npe_prime):
    # Step 2: map BA1 to future state probabilities BS1
        npe_prime = Npe_prime

        BA1 = getBA1(z6,z7,z8,z9,z10,No,Nb,Nn,Npe)

        BS1 = np.zeros((12*12*15*5))  # no', nb', nn', npe'
        for xo in range(No):
            for eb in range(No - xo):
                for xb in range(Nb):
                    for xn in range(Nn + 1):
                        for en in range(Npe + 1):
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

                            BS1[no_prime + 11*nb_prime + (11*11)*nn_prime + (11*11*14)*npe_prime] += \
                                BA1[xo + 11*eb + (11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en]
        return BS1

    def getEV1(No, Nb, Nn, Npe, Npe_prime, Vprime):
        npe_prime = Npe_prime
        BS1 = getBS1(No, Nb, Nn, Npe, Npe_prime)

        EV1 = 0.0  # Solution container
        for no_prime in range(12):
            for nb_prime in range(12):
                for nn_prime in range(15):
                    EV1 += BS1[no_prime + 11*nb_prime + (11*11)*nn_prime + (11*11*14)*npe_prime] \
                        * Vprime[0 + 2*no_prime + (2*11)*nb_prime + (2*11*11)*nn_prime]

        return EV1

    # Initialize result container
    # z1 = np.zeros(1)
    # BA1 = getBA1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe)
    # BS1 = getBS1(No, Nb, Nn, Npe, Npe_prime, BA1)
    z1 = getEV1(No, Nb, Nn, Npe, Npe_prime, Vprime)
    return z1