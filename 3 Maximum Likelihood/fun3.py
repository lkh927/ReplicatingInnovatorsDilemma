# Calcutaes the expected value of staying for both firms

# Setup
import numpy as np
from math import factorial
from fun0 import pow

def fun3(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):
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
        z3 = EV of staying for both firms
    '''

    prhs = [z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime]
    nrhs = len(prhs)

    # checks for correct inputs
    if nrhs != 11:
        raise Warning(f'Error fun3: 11 input arguments required, only {nrhs} given')
    if prhs[10].size != 6480:
        raise Warning(f'Error fun3: Vprime must have 6480 rows, it has {prhs[10].size}')
    if np.isnan(prhs[10]).any():
        raise Warning(f'Error fun3: Vprime must have 6480 elements')


    def getBA3(z6, z7, z8, z9, z10, No, Nb, Nn, Npe):
        '''
            xo = # of exits, old firms
            eb = # entry of both - aka # of adopts
            xb = # exit both firms
            xn = # exit new firms
            en = # entry potential firms
        '''

        BA3 = np.zeros((12*12*12*15*5))  # xo, eb, xb, xn, en
        for xo in range(No+1):
            for eb in range(No+1-xo):
                for xb in range(Nb):
                    for xn in range(Nn+1):
                        for en in range(Npe+1):
                            if Nb > 1:      # if number of both firms > 1
                                            # Intuitively: BA3[xo][eb][xb][xn][en]
                                BA3[xo + 11*eb +(11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en] = \
                                (factorial(No) / (factorial(xo) * factorial(No-xo))) \
                                * (factorial(No-xo) / (factorial(eb) * factorial(No-xo-eb))) \
                                * pow(z6,xo) * pow(z7,eb) * pow((1-z6-z7),(No-xo-eb)) \
                                * (factorial(Nb-1) / (factorial(xb) * factorial(Nb-1-xb))) \
                                * pow(z8,xb) * pow((1-z8),(Nb-1-xb)) \
                                * (factorial(Nn) / (factorial(xn) * factorial(Nn-xn))) \
                                * pow(z9,xn) * pow((1-z9),(Nn-xn)) \
                                * (factorial(Npe) / (factorial(en) * factorial(Npe-en))) \
                                * pow(z10,en) * pow((1-z10),(Npe-en))
                            
                            else:
                                            # Intuitively: BA3[xo][eb][0][xn][en]
                                BA3[xo + 11*eb + (11*11)*0 + (11*11*11)*xn + (11*11*11*14)*en] = \
                                (factorial(No) / (factorial(xo) * factorial(No-xo))) \
                                * (factorial(No-xo) / (factorial(eb) * factorial(No-xo-eb))) \
                                * pow(z6,xo) * pow(z7,eb) * pow((1-z6-z7),(No-xo-eb)) \
                                * (factorial(Nn) / (factorial(xn) * factorial(Nn-xn))) \
                                * pow(z9,xn) * pow((1-z9),(Nn-xn)) \
                                * (factorial(Npe) / (factorial(en) * factorial(Npe-en))) \
                                * pow(z10,en) * pow((1-z10),(Npe-en))
        return BA3


    def getBS3(No, Nb, Nn, Npe, Npe_prime):
    # Step 2: map BA3 to future state probabilities BS3
        npe_prime = Npe_prime

        BA3 = getBA3(z6,z7,z8,z9,z10,No,Nb,Nn,Npe)

        BS3 = np.zeros((12*12*15*5))  # no', nb', nn', npe'
        for xo in range(No+1):
            for eb in range(No + 1 - xo):
                for xb in range(Nb):
                    for xn in range(Nn + 1):
                        for en in range(Npe + 1):
                            xb = max(xb, 0)

                            no_prime = No - xo - eb
                            no_prime = max(0, no_prime)
                            no_prime = min(no_prime, 11)

                            nb_prime = Nb - xb + eb
                            nb_prime = max(0, nb_prime)
                            nb_prime = min(nb_prime, 11)

                            nn_prime = Nn - xn + en
                            nn_prime = max(0, nn_prime)
                            nn_prime = min(nn_prime, 14)

                            BS3[no_prime + 11*nb_prime + (11*11)*nn_prime + (11*11*14)*npe_prime] += \
                                BA3[xo + 11*eb + (11*11)*xb + (11*11*11)*xn + (11*11*11*14)*en]
        return BS3

    def getEV3(Npe_prime, Vprime):
        npe_prime = Npe_prime
        BS3 = getBS3(No, Nb, Nn, Npe, Npe_prime)

        EV3 = 0.0  # Solution container
        for no_prime in range(12):
            for nb_prime in range(12):
                for nn_prime in range(15):
                    EV3 += BS3[no_prime + 11*nb_prime + (11*11)*nn_prime + (11*11*14)*npe_prime] \
                        * Vprime[1 + 2*no_prime + (2*11)*nb_prime + (2*11*11)*nn_prime]
        return EV3

    z3 = getEV3(Npe_prime, Vprime)
    return z3