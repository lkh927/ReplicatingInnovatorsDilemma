# Calcutaes the transitions probabilities of old only firms

# Setup
import numpy as np
from math import factorial

def factorial(n):
    return np.math.factorial(n)

def getBA1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime):
# Step 1: compute BA1
    BA1 = np.zeros((12, 12, 12, 12, 15))  # xo, eb, xb, xn, en
    for xo in range(0,No+1):
        for eb in range(0, No-xo):
            for xb in range(0, Nb+1):
                for xn in range(0, Nn+1):
                    for en in range(1, Npe+2):
                        if No > 1:      # if number of old firms > 1
                            BA1[xo + 12*eb +(12*12)*xb + (12*12*12)xn + (12*12*12*15)en] = \
                            (factorial(No - 1) / (factorial(xo) * factorial(No - 1 - xo))) \
                            * (factorial(No - 1 - xo) / (factorial(eb) * factorial(No - 1 - xo - eb))) \
                            * z6**xo * z7**eb * ((1 - z6 - z7)**(No - 1 - xo - eb)) \
                            * (factorial(Nb) / (factorial(xb) * factorial(Nb - xb))) \
                            * z8**xb * ((1 - z8)**(Nb - xb)) \
                            * (factorial(Nn) / (factorial(xn) * factorial(Nn - xn))) \
                            * z9**xn * ((1 - z9)**(Nn - xn)) \
                            * (factorial(Npe) / (factorial(en) * factorial(Npe - en))) \
                            * z10**en * ((1 - z10)**(Npe - en))
                        else:
                            BA1[0 + 12*0 + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*en] = \
                            (factorial(Nb) / (factorial(xb) * factorial(Nb - xb))) \
                            * z8**xb * ((1 - z8)**(Nb - xb)) \
                            * (factorial(Nn) / (factorial(xn) * factorial(Nn - xn))) \
                            * z9**xn * ((1 - z9)**(Nn - xn)) \
                            * (factorial(Npe) / (factorial(en) * factorial(Npe - en))) \
                            * z10**en * ((1 - z10)**(Npe - en))
    return BA1


def getBS1(getBA1, z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime):
# Step 2: map BA1 to future state probabilities BS1
    npe_prime = Npe_prime

    BS1 = np.zeros((12, 12, 15, 15))  # no', nb', nn', npe'
    for xo in range(0, No):
        for eb in range(0, No - xo):
            for xb in range(0, Nb):
                for xn in range(0, Nn + 1):
                    for en in range(0, Npe + 1):
                        xo = max(xo, 0)
                        eb = max(eb, 1)

                        no_prime = No - xo - eb
                        no_prime = max(0, no_prime)
                        no_prime = min(no_prime, 11)

                        nb_prime = Nb - xb + eb
                        nb_prime = max(0, nb_prime)
                        nb_prime = min(nb_prime, 11)

                        nn_prime = Nn - xn + en
                        nn_prime = max(0, nn_prime)
                        nn_prime = min(nn_prime, 14)

                        BS1[no_prime + 12*nb_prime + (12*12)*nn_prime + (12*12*15)*npe_prime] += getBA1[xo + 12*eb + (12*12)*xb + (12*12*12)*xn + (12*12*12*15)*en]
    return BS1

def getEV1(getBS1, Npe_prime, Vprime):
    npe_prime = Npe_prime

    z1 = []      # Solution container
    for no_prime in range(0,12):
        for nb_prime in range(0,12):
            for nn_prime in range(0,15):
                z1 += getBS1[no_prime + 12*nb_prime + (12*12)*nn_prime + (12*12*15)*npe_prime] \
                * Vprime[0 + 3*no_prime + (3*12)*nb_prime + (3*12*12)*nn_prime]

    return


def fun1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):
    # Step 3: calculate expected value z1

    # nrhs = input arguments, should be 11 
    # prhs = input variables = 
        # z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime

    prhs = [z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime]
    nrhs = len(prhs)

    # checks for correct inputs
    if nrhs != 11:
        print(f'Error fun1: 11 input arguments required, only {nrhs} given')
    if len(prhs[10]) != 6480:
        print(f'Error fun1: Vprime must have 6480 rows, it has {len(prhs[9])}')
    if prhs[10].any() == np.nan:
        print(f'Error fun1: Vprime must have 6480 elements')

    # Initialize result container
    z1 = np.zeros(1,1)
    BA1 = BA1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime)
    BS1 = BS1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime)
    z1 = getEV1(BS1, Npe_prime, Vprime)

    return z1