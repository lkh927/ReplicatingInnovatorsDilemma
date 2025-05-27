import numpy as np
from math import factorial
import numpy as np

def fun5(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):

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
        z5 = EV of entering for Potential Entrants
    '''

    prhs = [z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime]
    nrhs = len(prhs)

    # checks for correct inputs
    if nrhs != 11:
        raise Warning(f'Error fun5: 11 input arguments required, only {nrhs} given')
    if prhs[10].size != 6480:
        raise Warning(f'Error fun5: Vprime must have 6480 rows, it has {prhs[10].size}')
    if np.isnan(prhs[10]).any():
        raise Warning(f'Error fun5: Vprime must have 6480 elements')


    def getBA5(z6, z7, z8, z9, z10, No, Nb, Nn, Npe):
        '''
        Objective: compute BA5, possible actions of all firms

            xo = # exit old firms
            eb = # old firms left after exits
            xb = # exit both firms
            xn = # exit new firms
            en = # entry potential firms ??
        '''

        # Initialize solution container
        BA5 = np.zeros((12, 12, 12, 15, 5))    # xo, eb, xb, xn, en

        for xo in range(No+1):
            for eb in range(No+1-xo):
                for xb in range(Nb+1):
                    for xn in range(Nn+1):
                        for en in range(1, Npe+1):

                            if Npe > 1:
                                # Intuitively: BA5[xo][eb][xb][xn][en]
                                BA5[xo + 12*eb + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*en] = \
                                (factorial(No) / (factorial(xo) * factorial(No-xo))) \
                                * (factorial(No-xo) / (factorial(eb) * factorial(No-xo-eb))) \
                                * z6**xo * z7**eb * (1-z6-z7)**(No-xo-eb) \
                                * (factorial(Nb) / (factorial(xb) * factorial(Nb-xb))) \
                                * z8**xb * (1-z8)**(Nb-xb) \
                                * (factorial(Nn) / (factorial(xn) * factorial(Nn-xn))) \
                                * z9**xn * (1-z9)**(Nn-xn) \
                                * (factorial(Npe-1) / (factorial(en-1) * factorial(Npe-1-(en-1)))) \
                                * z10**(en-1) * (1-z10)**(Npe-1-(en-1)) 
                            
                            else: 
                                # Intuitively: BA5[xo][eb][xb][xn][0]
                                BA5[xo + 12*eb + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*0] = \
                                (factorial(No) / (factorial(xo) * factorial(No-xo))) \
                                * (factorial(No-xo) / (factorial(eb) * factorial(No-xo-eb))) \
                                * z6**xo * z7**eb * (1-z6-z7)**(No-xo-eb) \
                                * (factorial(Nb) / (factorial(xb) * factorial(Nb-xb))) \
                                * z8**xb * (1-z8)**(Nb-xb) \
                                * (factorial(Nn) / (factorial(xn) * factorial(Nn-xn))) \
                                * z9**xn * (1-z9)**(Nn-xn)
                                # No term for Potential Entrants
        
        return BA5


    def getBS5(No, Nb, Nn, Npe, Npe_prime):
        '''
        Objective: map BA5 to future state probabilities into BS5
        '''
        
        npe_prime = Npe_prime
        BA5 = getBA5(z6,z7,z8,z9,z10,No,Nb,Nn,Npe)

        # initialize solution container
        BS5 = np.zeros((12, 12, 15, 15))    #no', nb', nn', npe'
        for xo in range(0, No+1):
            for eb in range(0, No +1 - xo):
                for xb in range(0, Nb + 1):
                    for xn in range(0, Nn + 1):
                        for en in range(0, Npe + 1):
                            
                            no_prime = No - xo - eb
                            nb_prime = Nb - xb + eb
                            nn_prime = Nn - xn + en

                            no_prime = max(no_prime,0)
                            no_prime = min(no_prime,11)

                            nb_prime = max(nb_prime,0)
                            nb_prime = min(nb_prime,11)

                            nn_prime = max(nn_prime,0)
                            nn_prime = min(nn_prime,14)
                            
                            BS5[no_prime + 12*nb_prime + (12*12)*nn_prime + (12*12*15)*npe_prime] \
                            += BA5[xo + 12*eb + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*en]
        return BS5


    def getEV5(Npe_prime, Vprime):

        npe_prime = Npe_prime

        BS5 = getBS5(No, Nb, Nn, Npe, Npe_prime)

        EV5 = 0.0     # Solution container
        for no_prime in range(12):
            for nb_prime in range(12):
                for nn_prime in range(15):

                    EV5 += BS5[no_prime + 12*nb_prime + (12*12)*nn_prime + (12*12*15)*npe_prime] \
                        * Vprime[2 + 3*no_prime + (3*12)*nb_prime + (3*12*12)*nn_prime]
                    
        return EV5

    # Initialize result container
    z5 = getEV5(Npe_prime, Vprime)

    return z5