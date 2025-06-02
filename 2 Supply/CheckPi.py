# Checking FOC's for output

import numpy as np

# Import data found using FindMC.py and FindPi.py
# MC
# Pi (import Bigq, BigQ, BigP and BigPi)


# Check for non-negativety 

def check_negativity(x, name=''):
    # Used to check for non-negativity and real numbers for Bigq, BigQ, BigP and BigPi
    # Takes input = x, which is either Bigq, BigQ, or BigP

    # y = number of types
    # For Bigq, type can be 1-4 (quantity of old by old and both, quantity of new by both and new)
    # For BigQ, type can be 1-2 (aggregate quantity of generation)
    # For BigP, type can be 1-2 (prices of old and new)
    y = x.shape[1]

    print(f'Checking {name} for non-negativity and real numbers...')

    for t in range(18):
        for No in range(12):
            for Nb in range(12):
                for Nn in range(15):
                    for type in range(y):
                        check = x[t, type, No, Nb, Nn]
                        if check < -0.01:
                            print(f'Negative at year {1981+t}, (No,Nb,Nn,type)=({No},{Nb},{Nn},{type})')
                        if np.isreal(check) == 0:
                            print(f'Complex at year {1981+t}, (No,Nb,Nn,type)=({No},{Nb},{Nn},{type})')
    return

def check_negativity_Pi(BigPi):
    # Used to check for non-negativity and real numbers for Bigq, BigQ, BigP and BigPi
    # Takes input = x, which is either Bigq, BigQ, BigP or BigPi

    # y = number of types, can be 1-3 (for profit of old, both and new type firm)
    y = BigPi.shape[1]

    print(f'Checking BigPi for non-negativity and real numbers...')

    for t in range(18):
        for No in range(12):
            for Nb in range(12):
                for Nn in range(15):
                    for type in range(y):
                        check = BigPi[t, type, No, Nb, Nn]
                        if check < -0.01:
                            print(f'Negative at year {1981+t}, (No,Nb,Nn,type)=({No},{Nb},{Nn},{type})')
                            BigPi[t, type, No, Nb, Nn] = 0.0  # Set to zero
                        if np.isreal(check) == 0:
                            print(f'Complex at year {1981+t}, (No,Nb,Nn,type)=({No},{Nb},{Nn},{type})')
    return


def check_monotonicity_old(x, name=''):
    # Used to check for monotonocity in number of old-only firms.
    # Can be used for qo (quantity of old-only) and Pi_o (profit of old-only)
    # Takes input = x, which is either qo or Pi_o

    print(f'Checking {name} for monotonicity in number of old firms, No...')

    count = 0
    for t in range(18):
        for Nb in range(12):
            for Nn in range(15):
                No = 1
                x_prev = x[t, 0, No, Nb, Nn]
                for No in range(2, 12):
                    x_curr = x[t, 0, No, Nb, Nn]
                    if x_curr > x_prev:
                        #print(f'qo rose at year {t}, (No,Nb,Nn)=({No},{Nb},{Nn})')
                        count += 1
                    x_prev = x_curr
    print(f'{name} rose {count} times')
    return

def check_monotonicity_bothold(x, name=''):
    # Used to check for monotonocity in number of both-old firms.
    # Can be used for qbo (quantity of both) and Pi_b (profit of both)
    # Takes input = x, which is either qbo or Pi_b

    print(f'Checking {name} for monotonicity in number of both/old firms, Nb...')

    count = 0
    for t in range(18):
        for No in range(12):
            for Nn in range(15):
                Nb = 1
                x_prev = x[t, 1, No, Nb, Nn]
                for No in range(2, 12):
                    x_curr = x[t, 1, No, Nb, Nn]
                    if x_curr > x_prev:
                        #print(f'{x} rose at year {t}, (No,Nb,Nn)=({No},{Nb},{Nn})')
                        count += 1
                    x_prev = x_curr
    print(f'{name} rose {count} times')
    return


def check_monotonicity_bothnew(x, name=''):
    # Used to check for monotonocity in number of both-new firms.
    # Can be used for qbn (quantity of both-new) and Pi_n (profit of new)
    # Takes input = x, which is either qbn and Pi_n

    print(f'Checking {name} for monotonicity in number of both/new firms, Nb...')

    count = 0
    for t in range(18):
        for No in range(12):
            for Nb in range(12):
                Nn = 1
                x_prev = x[t, 1, No, Nb, Nn]
                for No in range(2, 12):
                    x_curr = x[t, 1, No, Nb, Nn]
                    if x_curr > x_prev:
                        #print(f'{name} rose at year {t}, (No,Nb,Nn)=({No},{Nb},{Nn})')
                        count += 1
                    x_prev = x_curr
    print(f'{name} rose {count} times')
    return


def check_monotonicity_new(x, name=''):
    # Used to check for monotonocity in number of new-only firms.
    # Can be used for qn (quantity of new-only)
    # Takes input = x, which is qn 

    print(f'Checking {name} for monotonicity in number of new firms, Nn...')

    count = 0
    for t in range(18):
        for No in range(12):
            for Nb in range(12):
                Nn = 1
                x_prev = x[t, 2, No, Nb, Nn]
                for No in range(2, 12):
                    x_curr = x[t, 2, No, Nb, Nn]
                    if x_curr > x_prev:
                        #print(f'{x} rose at year {t}, (No,Nb,Nn)=({No},{Nb},{Nn})')
                        count += 1
                    x_prev = x_curr
    print(f'{name} rose {count} times')
    return