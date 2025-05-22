# Calcutaes the transitions probabilities of old only firms

# Setup
import numpy as np
from math import comb

# def factorial(n):
    # return np.math.factorial(n)

def fun1(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):
    No, Nb, Nn, Npe, Npe_prime = int(No), int(Nb), int(Nn), int(Npe), int(Npe_prime)

    # Step 1: compute BA1
    BA1 = np.zeros((12, 12, 12, 12, 15))  # xo, eb, xb, xn, en
    if No > 1:      # if number of old firms > 1
        for xo in range(No):
            for eb in range(No - xo):
                for xb in range(Nb + 1):
                    for xn in range(Nn + 1):
                        for en in range(Npe + 1):
                            p = (
                                comb(No - 1, xo)
                                * comb(No - 1 - xo, eb)
                                * (z6**xo) * (z7**eb) * ((1 - z6 - z7)**(No - 1 - xo - eb))
                                * comb(Nb, xb) * (z8**xb) * ((1 - z8)**(Nb - xb))
                                * comb(Nn, xn) * (z9**xn) * ((1 - z9)**(Nn - xn))
                                * comb(Npe, en) * (z10**en) * ((1 - z10)**(Npe - en))
                            )
                            BA1[xo, eb, xb, xn, en] = p
    else:
        for xb in range(Nb + 1):
            for xn in range(Nn + 1):
                for en in range(Npe + 1):
                    p = (
                        comb(Nb, xb) * (z8**xb) * ((1 - z8)**(Nb - xb))
                        * comb(Nn, xn) * (z9**xn) * ((1 - z9)**(Nn - xn))
                        * comb(Npe, en) * (z10**en) * ((1 - z10)**(Npe - en))
                    )
                    BA1[0, 0, xb, xn, en] = p

    # Step 2: map BA1 to future state probabilities BS1
    BS1 = np.zeros((12, 12, 15, 15))  # no', nb', nn', npe'
    for xo in range(No if No > 1 else 1):
        for eb in range(No - xo if No > 1 else 1):
            for xb in range(Nb + 1):
                for xn in range(Nn + 1):
                    for en in range(Npe + 1):
                        no_p = min(max(No - xo - eb, 0), 11)
                        nb_p = min(max(Nb - xb + eb, 0), 11)
                        nn_p = min(max(Nn - xn + en, 0), 14)
                        npe_p = min(Npe_prime, 14)
                        BS1[no_p, nb_p, nn_p, npe_p] += BA1[xo, eb, xb, xn, en]

    # Step 3: calculate expected value z1
    z1 = 0.0        # Initial guess
    for no_p in range(12):
        for nb_p in range(12):
            for nn_p in range(15):
                idx = 0 + 3 * no_p + 3 * 12 * nb_p + 3 * 12 * 12 * nn_p
                z1 += BS1[no_p, nb_p, nn_p, Npe_prime] * Vprime[idx]

    return z1