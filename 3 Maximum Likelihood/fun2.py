import numpy as np
from math import comb #, factorial

def fun2(z6, z7, z8, z9, z10, No, Nb, Nn, Npe, Npe_prime, Vprime):
    BA2 = np.zeros(129600)
    BS2 = np.zeros(10800)

    def index5d(xo, eb, xb, xn, en):
        return xo + 12*eb + 144*xb + 1728*xn + 25920*en

    def index4d(no_p, nb_p, nn_p, npe_p):
        return no_p + 12*nb_p + 144*nn_p + 2160*npe_p

    # Step 1: compute BA2
    if No > 1:
        for xo in range(int(No)):
            for eb in range(1, int(No - xo) + 1):
                for xb in range(int(Nb) + 1):
                    for xn in range(int(Nn) + 1):
                        for en in range(int(Npe) + 1):
                            p = (
                                comb(int(No) - 1, xo) *
                                comb(int(No) - 1 - xo, eb - 1) *
                                (z6 ** xo) * (z7 ** (eb - 1)) * ((1 - z6 - z7) ** (int(No) - 1 - xo - (eb - 1))) *
                                comb(int(Nb), xb) * (z8 ** xb) * ((1 - z8) ** (int(Nb) - xb)) *
                                comb(int(Nn), xn) * (z9 ** xn) * ((1 - z9) ** (int(Nn) - xn)) *
                                comb(int(Npe), en) * (z10 ** en) * ((1 - z10) ** (int(Npe) - en))
                            )
                            BA2[index5d(xo, eb, xb, xn, en)] = p
    else:
        for xb in range(int(Nb) + 1):
            for xn in range(int(Nn) + 1):
                for en in range(int(Npe) + 1):
                    p = (
                        comb(int(Nb), xb) * (z8 ** xb) * ((1 - z8) ** (int(Nb) - xb)) *
                        comb(int(Nn), xn) * (z9 ** xn) * ((1 - z9) ** (int(Nn) - xn)) *
                        comb(int(Npe), en) * (z10 ** en) * ((1 - z10) ** (int(Npe) - en))
                    )
                    BA2[index5d(0, 0, xb, xn, en)] = p

    # Step 2: map BA2 to future state probabilities BS2
    npe_prime = int(Npe_prime)
    for xo in range(int(No)):
        for eb in range(1, int(No - xo) + 1):
            for xb in range(int(Nb) + 1):
                for xn in range(int(Nn) + 1):
                    for en in range(int(Npe) + 1):
                        no_prime = max(0, min(11, int(No) - xo - eb))
                        nb_prime = max(0, min(11, int(Nb) - xb + eb))
                        nn_prime = max(0, min(14, int(Nn) - xn + en))

                        BS2[index4d(no_prime, nb_prime, nn_prime, npe_prime)] += BA2[index5d(xo, eb, xb, xn, en)]

    # Step 3: calculate expected value z2
    z2 = 0.0
    for no_p in range(12):
        for nb_p in range(12):
            for nn_p in range(15):
                z2 += (
                    BS2[index4d(no_p, nb_p, nn_p, npe_prime)] *
                    Vprime[1 + 3*no_p + 3*12*nb_p + 3*12*12*nn_p]
                )

    return z2