import numpy as np
from math import factorial

# Import choice probabilities
import fun6, fun7, fun8, fun9, fun10

def factorial(n):
    return np.math.factorial(n)

def getBA5(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime):
    
    # Initialize solution container
    BA5 = np.zeros((12, 12, 12, 12, 15))    # xo, eb, xb, xn, en

    for xo in range(0,No+1):
        for eb in range(0, No+1-xo):
            for xb in range(0, Nb+1):
                for xn in range(0, Nn+1):
                    for en in range(0, Npe+1):

                        if Npe > 1:
                            BA5[xo + 12*eb + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*en] = \
                            (factorial(No) / (factorial(xo) * factorial(No-xo))) * (factorial(No-xo) / (factorial(eb) * factorial(No-xo-eb))) \
                            * z6**xo * z7**eb * (1-z6-z7)**(No-xo-eb) \
                            * (factorial(Nb) / (factorial(xb) * factorial(Nb-xb))) \
                            * z8**xb * (1-z8)**(Nb-xb) \
                            * (factorial(Nn) / (factorial(xn) * factorial(Nn-xn))) \
                            * z9**xn * (1-z9)**(Nn-xn) \
                            * (factorial(Npe-1) / (factorial(en-1) * factorial(Npe-1-(en-1)))) \
                            * z10**(en-1) * (1-z10)**(Npe-1-(en-1)) 
                        
                        else: 
                            BA5[xo + 12*eb + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*0] = \
                            (factorial(No) / (factorial(xo) * factorial(No-xo))) * (factorial(No-xo) / (factorial(eb) * factorial(No-xo-eb))) \
                            * z6**xo * z7**eb * (1-z6-z7)**(No-xo-eb) \
                            * (factorial(Nb) / (factorial(xb) * factorial(Nb-xb))) \
                            * z8**xb * (1-z8)**(Nb-xb) \
                            * (factorial(Nn) / (factorial(xn) * factorial(Nn-xn))) \
                            * z9**xn * (1-z9)**(Nn-xn)
    
    return BA5


def getBS5(getBA5, z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime):
    
    npe_prime = Npe_prime

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

                        if no_prime < 0:
                            no_prime = 0
                        elif no_prime > 11:
                            no_prime = 11

                        if nb_prime < 0:
                            nb_prime = 0
                        elif nb_prime > 11:
                            nb_prime = 11

                        if nn_prime < 0:
                            nn_prime = 0
                        elif nb_prime > 14:
                            nb_prime = 14
                        
                        BS5[no_prime + 12*nb_prime + (12*12)*nn_prime + (12*12*15)*npe_prime] \
                        += getBA5[xo + 12*eb + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*en]
    return BS5


def getEV5(getBS5, Npe_prime, Vprime):

    npe_prime = Npe_prime

    z5 = []      # Solution container
    for no_prime in range(0,12):
        for nb_prime in range(0,12):
            for nn_prime in range(0,15):

                z5 += getBS5[no_prime + 12*nb_prime + (12*12)*nn_prime + (12*12*15)*npe_prime] \
                      * Vprime[2 + 3*no_prime + (3*12)*nb_prime + (3*12*12)*nn_prime]
                
    return


def fun5(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):

    prhs = [z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime]
    nrhs = len(prhs)

    # Check for correct inputs
    if nrhs != 11:
        print(f'Error found fun1: 11 input arguments required, only {nrhs} given')
    if len(prhs[10]) != 6480:
        print(f'Error fun1: Vprime must have 6480 rows, it has {len(prhs[9])}')
    if prhs[10].any() == np.nan:
        print(f'Error found fun5: Vprime must have 6480 elements')

    # Initialize result container
    z5 = np.zeros(1,1)
    BA5 = getBA5(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime)
    BS5 = getBS5(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime)
    z5 = getEV5(BS5, Npe_prime, Vprime)

    return z5