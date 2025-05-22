import numpy as np
from math import factorial

def fun3(z6, z7, z8, z9, z10,
         no, nb, nn, npe, npe_prime,
         Vprime):
    """
    Python version of fun3.c (fills BA3 & BS3 and computes z3).
    
    Inputs:
      z6…z10       : policy probabilities (floats)
      no, nb, nn   : integers (No, Nb, Nn)
      npe          : integer (Npe)
      npe_prime    : integer (Npe_prime)
      Vprime       : 1D numpy array, length 6480 (3×12×12×15), 
                     ordered as in the MEX code.
    Returns:
      z3           : float
    """

    # pre‐allocate flat buffers exactly as in the C code:
    BA3 = np.zeros(12 * 12 * 12 * 15 * 5)
    BS3 = np.zeros(12 * 12 * 15 * 5)

    # === fillBA3 ===
    for xo in range(no + 1):
        for eb in range(no - xo + 1):
            # in C: xb <= Nb-1, but if Nb<=1 they force xb=0, so:
            max_xb = nb - 1 if nb > 1 else 0
            for xb in range(max_xb + 1):
                for xn in range(nn + 1):
                    for en in range(npe + 1):
                        idxBA = (
                            xo
                            + 12 * eb
                            + 12 * 12 * xb
                            + 12 * 12 * 12 * xn
                            + 12 * 12 * 12 * 15 * en
                        )

                        # start building the same product of binomials & powers:
                        term = (
                            factorial(no) /
                            (factorial(xo) * factorial(no - xo))
                        )
                        term *= (
                            factorial(no - xo) /
                            (factorial(eb) * factorial(no - xo - eb))
                        )
                        term *= (z6**xo) * (z7**eb) * ((1 - z6 - z7)**(no - xo - eb))

                        if nb > 1:
                            term *= (
                                factorial(nb - 1) /
                                (factorial(xb) * factorial(nb - 1 - xb))
                            )
                            term *= (z8**xb) * ((1 - z8)**(nb - 1 - xb))
                        # else: no “both‐type” term

                        term *= (
                            factorial(nn) /
                            (factorial(xn) * factorial(nn - xn))
                        )
                        term *= (z9**xn) * ((1 - z9)**(nn - xn))

                        term *= (
                            factorial(npe) /
                            (factorial(en) * factorial(npe - en))
                        )
                        term *= (z10**en) * ((1 - z10)**(npe - en))

                        BA3[idxBA] = term

    # === fillBS3 ===
    for xo in range(no + 1):
        for eb in range(no - xo + 1):
            max_xb = nb - 1 if nb > 1 else 0
            for xb in range(max_xb + 1):
                for xn in range(nn + 1):
                    for en in range(npe + 1):
                        idxBA = (
                            xo
                            + 12 * eb
                            + 12 * 12 * xb
                            + 12 * 12 * 12 * xn
                            + 12 * 12 * 12 * 15 * en
                        )

                        # compute “primed” counts and clamp them
                        no_p = no - xo - eb
                        nb_p = nb - xb + eb
                        nn_p = nn - xn + en

                        no_p = min(max(no_p, 0), 11)
                        nb_p = min(max(nb_p, 0), 11)
                        nn_p = min(max(nn_p, 0), 14)

                        idxBS = (
                            no_p
                            + 12 * nb_p
                            + 12 * 12 * nn_p
                            + 12 * 12 * 15 * npe_prime
                        )

                        BS3[idxBS] += BA3[idxBA]

    # === getEV3 ===
    z3 = 0.0
    # In the MEX, z3 += BS3[...] * Vprime[1 + 3*no_p + 36*nb_p + 432*nn_p].
    # Converting from MATLAB's 1‐based indexing to Python's 0‐based,
    # that becomes Vprime[3*no_p + 36*nb_p + 432*nn_p].
    for no_p in range(12):
        for nb_p in range(12):
            for nn_p in range(15):
                idxBS = (
                    no_p
                    + 12 * nb_p
                    + 12 * 12 * nn_p
                    + 12 * 12 * 15 * npe_prime
                )
                idxV = 3 * no_p + 36 * nb_p + 432 * nn_p
                z3 += BS3[idxBS] * Vprime[idxV]

    return z3
