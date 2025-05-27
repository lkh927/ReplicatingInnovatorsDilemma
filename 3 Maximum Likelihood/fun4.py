# Calcutaes the transitions probability of staying for New-only firms

# Setup
import numpy as np
from math import factorial

def fun4(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):
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
        z4 = EV of staying for New-only firms
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


    def getBA4(z6, z7, z8, z9, z10, No, Nb, Nn, Npe):
        '''
        Objective: compute BA4, mapping of actions for New firms

            xo = # of exits, old firms
            eb = # entry of both - aka # of adopts
            xb = # exit both firms
            xn = # exit new firms
            en = # entry potential firms
        '''

        BA4 = np.zeros((12*12*12*15*5))  # xo, eb, xb, xn, en
        for xo in range(No+1):
            for eb in range(No+1-xo):
                for xb in range(Nb+1):
                    for xn in range(Nn):
                        for en in range(Npe+1):
                            if Nn > 1:      # if number of new firms > 1
                                            # Intuitively: BA4[xo][eb][xb][xn][en]
                                BA4[xo + 11*eb +(11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en] = \
                                (factorial(No+1) / (factorial(xo) * factorial(No+1-xo))) \
                                * (factorial(No+1-xo) / (factorial(eb) * factorial(No+1-xo-eb))) \
                                * (z6**xo) * (z7**eb) * ((1-z6-z7)**(No+1-xo-eb)) \
                                * (factorial(Nb+1) / (factorial(xb) * factorial(Nb+1 - xb))) \
                                * (z8**xb) * ((1-z8)**(Nb+1 - xb)) \
                                * (factorial(Nn) / (factorial(xn) * factorial(Nn-xn))) \
                                * (z9**xn) * ((1-z9)**(Nn-xn)) \
                                * (factorial(Npe+1) / (factorial(en) * factorial(Npe+1-en))) \
                                * (z10**en) * ((1-z10)**(Npe+1-en))
                            else:
                                            # Intuitively: BA4[xo][eb][xb][0][en]
                                BA4[xo + 11*eb + (11*11)*xb + (11*11*11)*0 + (11*11*11*14)*en] = \
                                (factorial(No+1) / (factorial(xo) * factorial(No+1 - xo))) \
                                * (factorial(No+1-xo) / (factorial(eb) * factorial(No+1-xo-eb))) \
                                * (z6**xo) * (z7**eb) * ((1-z6-z7)**(No+1-xo-eb)) \
                                * (factorial(Nb+1) / (factorial(xb) * factorial(Nb+1 - xb))) \
                                * (z8**xb) * ((1-z8)**(Nb+1-xb)) \
                                * (factorial(Npe+1) / (factorial(en) * factorial(Npe+1 - en))) \
                                * (z10**en) * ((1 - z10)**(Npe+1 - en))
        return BA4


    def getBS4(No, Nb, Nn, Npe, Npe_prime):
    # Step 2: map BA1 to future state probabilities BS1
        npe_prime = Npe_prime

        BA4 = getBA4(z6,z7,z8,z9,z10,No,Nb,Nn,Npe)

        BS4 = np.zeros((12*12*15*5))  # no', nb', nn', npe'
        for xo in range(No+1):
            for eb in range(No+1 - xo):
                for xb in range(Nb+1):
                    for xn in range(Nn):
                        for en in range(Npe + 1):
                            xn = max(xn,0)

                            # Number of Old-only firms next period = 
                            # Number of Old firms - exits of old firms - old firms adopting
                            no_prime = No - xo - eb
                            no_prime = max(0, no_prime)
                            no_prime = min(no_prime, 11)

                            # Number of Both firms next period =
                            # Number of Both - exits of both firms + number of old firms adopting
                            nb_prime = Nb - xb + eb     
                            nb_prime = max(0, nb_prime)
                            nb_prime = min(nb_prime, 11)

                            # Number of New firms next period = 
                            # Number of new firms - exits + entrants
                            nn_prime = Nn - xn + en
                            nn_prime = max(0, nn_prime)
                            nn_prime = min(nn_prime, 14)

                            BS4[no_prime + 11*nb_prime + (11*11)*nn_prime + (11*11*14)*npe_prime] += \
                                BA4[xo + 11*eb + (11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en]
        return BS4

    def getEV4(No, Nb, Nn, Npe, Npe_prime, Vprime):
        npe_prime = Npe_prime
        BS4 = getBS4(No, Nb, Nn, Npe, Npe_prime)

        EV4 = 0.0  # Solution container
        for no_prime in range(0,12):
            for nb_prime in range(0,12):
                for nn_prime in range(0,15):
                    EV4 += BS4[no_prime + 11*nb_prime + (11*11)*nn_prime + (11*11*14)*npe_prime] \
                        * Vprime[1 + 2*no_prime + (2*11)*nb_prime + (2*11*11)*nn_prime]

        return EV4

    # Initialize result container
    # z1 = np.zeros(1)
    # BA1 = getBA1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe)
    # BS1 = getBS1(No, Nb, Nn, Npe, Npe_prime, BA1)
    z4 = getEV4(No, Nb, Nn, Npe, Npe_prime, Vprime)
    
    return z4