# Likelihood function to evaluate choices

# Setup
import numpy as np
import pandas as pd
import scipy.optimize
import time
import glob
import os

# Import (policy and transition) functions 
from fun1 import fun1
from fun2 import fun2
from fun3 import fun3
from fun4 import fun4 
from fun5 import fun5
from fun6 import fun6
from fun7 import fun7
from fun8 import fun8
from fun9 import fun9
from fun10 import fun10
from fun11 import fun11
from fun12 import fun12
from fun13 import fun13


def Likelihood(Theta, beta, delta, Pi, V, EV, Policy, State, Exit, Adopt, T, iterMLE, output_type):
    """
    Takes inputs: Theta (3 x 1: phi, kappa_inc, kappa_ent), beta (discount factor), delta (rate of change in sunk cost), 
    Pi (Profits), V (value function), EV (expected value), Policy (policy choices), State (current state),
    Exit (exit decisions), Adopt (adoption decisions), T (number of periods), iterMLE (iteration number),
    and output_type (1 for log likelihood, 2 for total likelihood).
    """
    # Separate 
    phi, kappa_inc, kappa_ent = Theta

    print(f"\nMLE iter #{iterMLE:4.0f}: trying (phi, kappa_inc, kappa_ent) = ({phi:.8f}, {kappa_inc:.8f}, {kappa_ent:.8f})")

    start_time = time.time()
    #V = np.zeros((T, 3, 12, 12, 15))  # Value function initialized for T periods, 3 types, 12 no_prime, 12 nb_prime, 15 nn_prime
    
    for t in range(T-2,-1,-1):     # Using backwards induction, so starting for the last period and deducting until first period
        Vprime = np.zeros((6480,))      # 3*12*12*15 (type * no_prime * nb_prime * nn_prime)
        for type in range(3):           # Loop over types (0: no_prime, 1: nb_prime, 2: nn_prime)
            for no_prime in range(12):  # Loop over no_prime (0 to 11)
                for nb_prime in range(12): # Loop over nb_prime (0 to 11)
                    for nn_prime in range(15): # Loop over nn_prime (0 to 14)
                        Vprime[type + 2*no_prime + 2*11*nb_prime + 2*11*11*nn_prime] \
                         = V[t+1, type, no_prime, nb_prime, nn_prime]
                        # This line fills the Vprime array with the values from the next period's value function
                        # The first time iteration (in the terminal period), this will be filled with the infinite sum of future discounted profits
                        #  - the next time, it will be filled with the values that were calculated in the previous iteration

        # Loading observed states in the given year
        Npe = State[t, 3]
        Npe_prime = State[t+1, 3]
        # Starting state identification counter
        statenum = 1

        # Looping over all possible states (no, nb, nn) for the current period
        for no in range(12):
            for nb in range(12):
                for nn in range(15):
                    # Now, wolve for the Nash equilibrium
                    # gap is the sum of differences between z6 and z6old, z7 and z7old, ... , and z10 and z10old.
                    gap = 666
                    # inner loop iteration counter
                    iterNE = 1
                    
                    # Initialize expected value of choosing each option in tomorrow's actual state
                    if no > 0: # Old firms
                        z1 = V[t+1, 0, State[t+1,0], State[t+1,1], State[t+1,2]] # EV of staying -> type is old next period
                        z2 = V[t+1, 1, State[t+1,0], State[t+1,1], State[t+1,2]] # EV of adopting -> type is both next period
                    else:
                        z1 = z2 = 0
                    if nb > 0: # Both firms
                        z3 = V[t+1, 1, State[t+1,0], State[t+1,1], State[t+1,2]] # EV of staying -> type is both next period
                    else:
                        z3 = 0
                    if nn > 0: # New firms
                        z4 = V[t+1, 2, State[t+1,0], State[t+1,1], State[t+1,2]] # EV of staying -> type is new next period
                    else:
                        z4 = 0
                    if Npe > 0: # Potential entrants
                        z5 = V[t+1, 2, State[t+1,0], State[t+1,1], State[t+1,2]] # EV of entering -> type is new next period
                    else:
                        z5 = 0

                    # Initialize choice probabilities based on the initial expected values tomorrow
                    if no > 0:
                        z6old = fun6(z1, z2, beta, phi, kappa_inc, delta, t) # Pr[stay|old], given EVs of next period
                        z7old = fun7(z1, z2, beta, phi, kappa_inc, delta, t) # Pr[adopt|old], given EVs of next period
                    else:
                        z6old = z7old = 0 # Pr[stay|old] and Pr[adopt|old] if there are no old firms

                    if nb > 0:
                        z8old = fun8(z3, beta, phi) # Pr[stay|both], given EVs of next period
                    else:
                        z8old = 0 # Pr[stay|both] if there are no both firms

                    if nn > 0:
                        z9old = fun9(z4, beta, phi) # Pr[stay|new], given EVs of next period
                    else:
                        z9old = 0 # Pr[stay|new] if there are no new firms

                    if Npe > 0:
                        z10old = fun10(z5, beta, kappa_ent, delta, t) # Pr[enter|PE], given EVs of next period
                    else:
                        z10old = 0 # Pr[enter|PE] if there are no potential entrants

                    # Succesive approximations: Beliefs --> Policies --> Beliefs --> Policies...
                    while gap > 0.01 and iterNE < 10: # run 10 iterations or until convergence per state
                        if no > 0:
                            z1 = fun1(z6old, z7old, z8old, z9old, z10old, no, nb, nn, Npe, Npe_prime, Vprime) # Expected value of staying old, given choice prob of self and others
                            z2 = fun2(z6old, z7old, z8old, z9old, z10old, no, nb, nn, Npe, Npe_prime, Vprime) # Expected value of adopting, given choice prob of self and others
                            z6 = (fun6(z1, z2, beta, phi, kappa_inc, delta, t) + z6old) /2 # Pr[stay|old], given values and previous expectations
                            z7 = (fun7(z1, z2, beta, phi, kappa_inc, delta, t) + z7old) /2 # Pr[adopt|old], given values and previous expectations
                        else:
                            z1 = z2 = z6 = z7 = 0 # If no old firms, then values and probabilities are 0

                        if nb > 0:
                            z3 = fun3(z6, z7, z8old, z9old, z10old, no, nb, nn, Npe, Npe_prime, Vprime) # Value of staying both, given choice prob of self and others
                            z8 = (fun8(z3, beta, phi) + z8old) / 2 # Pr[stay|both], given values and previous expectations
                        else:
                            z3 = z8 = 0 # If no both firms, then values and probabilities are 0

                        if nn > 0:
                            z4 = fun4(z6, z7, z8, z9old, z10old, no, nb, nn, Npe, Npe_prime, Vprime) # Value of staying new, given choice prob of self and others
                            z9 = (fun9(z4, beta, phi) + z9old) / 2 # Pr[stay|new], given values and previous expectations
                        else:
                            z4 = z9 = 0 # If no new firms, then values and probabilities are 0

                        if Npe > 0:
                            z5 = fun5(z6, z7, z8, z9, z10old, no, nb, nn, Npe, Npe_prime, Vprime) # Value of entering, given choice prob of self and others
                            z10 = (fun10(z5, beta, kappa_ent, delta, t) + z10old) / 2 # Pr[enter|PE], given values and previous expectations
                        else:
                            z5 = z10 = 0 # If no potential entrants, then values and probabilities are 0

                        gap = abs(z6 - z6old) + abs(z7 - z7old) + abs(z8 - z8old) + abs(z9 - z9old) + abs(z10 - z10old) # Calculate the gap between old and new probabilities
                        
                        # Update values and interation counter
                        z6old, z7old, z8old, z9old, z10old = z6, z7, z8, z9, z10
                        iterNE += 1

                    # Update expected values and policies    
                    EV[t+1, :, no, nb, nn] = np.array([z1, z2, z3, z4, z5])
                    Policy[t, :, no, nb, nn] = np.array([z6, z7, z8, z9, z10])
                    # Calculate the Closed form expression for the expected value before observing epsilon.
                    if no > 0:
                        V[t, 0, no, nb, nn] = Pi[t, 0, no, nb, nn] + 0.57722 + fun11(z1, z2, beta, phi, kappa_inc, delta, t)
                    else:
                        V[t, 0, no, nb, nn] = 0
                    if nb > 0:
                        V[t, 1, no, nb, nn] = Pi[t, 1, no, nb, nn] + 0.57722 + fun12(z3, beta, phi)
                    else:
                        V[t, 1, no, nb, nn] = 0
                    if nn > 0:
                        V[t, 2, no, nb, nn] = Pi[t, 2, no, nb, nn] + 0.57722 + fun13(z4, beta, phi)
                    else:
                        V[t, 2, no, nb, nn] = 0
                    
                    # Print progress
                    #print(f"Year: {t}, State {statenum:4d}: (no, nb, nn) = ({no:2d}, {nb:2d}, {nn:2d})")
                    #print(f'Expected Value (z1, z2, z3, z4, z5) = ({z1:.2f}, {z2:.2f}, {z3:.2f}, {z4:.2f}, {z5:.2f})')
                    #print(f'Choice Probabilities (z6, z7, z8, z9, z10) = ({z6:.4f}, {z7:.4f}, {z8:.4f}, {z9:.4f}, {z10:.4f})')
                    #print(f'Value today (Vo, Vb, Vn) = ({V[t, 0, no, nb, nn]:.2f}, {V[t, 1, no, nb, nn]:.2f}, {V[t, 2, no, nb, nn]:.2f})')

                    statenum += 1

    # Joint choice probabilities (LL of observing choices in actual data over period and type)
    LL = np.zeros((T - 1, 4))
    
    for t in range(T - 2):
        No = State[t, 0]
        Nb = State[t, 1]
        Nn = State[t, 2]
        Npe = State[t, 3]
        Npe_prime = State[t+1, 3]
        print(f"Actual state in year {t}: (No, Nb, Nn, Npe, Npe_prime) = ({No},{Nb},{Nn},{Npe},{Npe_prime})")

        a6 = Policy[t, 0, No, Nb, Nn]
        a7 = Policy[t, 1, No, Nb, Nn]
        a8 = Policy[t, 2, No, Nb, Nn]
        a9 = Policy[t, 3, No, Nb, Nn]
        a10 = Policy[t, 4, No, Nb, Nn]
        print(f"Policies: Prob(Xo, Eo, Xb, Xn, En) = ({a6:.4f},{a7:.4f},{a8:.4f},{a9:.4f},{a10:.4f})")

        # Ensure probabilities are not zero for no log(0)
        if a6 < 0.0001:
            a6 = 0.0001
        if a7 < 0.0001:
            a7 = 0.0001
        if a8 < 0.0001:
            a8 = 0.0001
        if a9 < 0.0001:
            a9 = 0.0001
        if a10 < 0.0001:
            a10 = 0.0001

        # Log likelihood
        LL[t, 0] = Exit[t, 0] * np.log(a6) + Adopt[t, 0] * np.log(a7) + (State[t, 0] - Exit[t, 0] - Adopt[t, 0]) * np.log(1 - a6 - a7)
        # Exit|Old * ln(Pr[Exit|Old]) + Adopt * ln(Pr[Adopt|Old]) + (State - Exit - Adopt) * ln(1 - Pr[Exit|Old] - Pr[Adopt|Old])
        LL[t, 1] = Exit[t, 1] * np.log(a8) + (State[t, 1] - Exit[t, 1]) * np.log(1 - a8)
        # Exit|Both * ln(Pr[Exit|Both]) + (State - Exit) * ln(1 - Pr[Exit|Both])
        LL[t, 2] = Exit[t, 2] * np.log(a9) + (State[t, 2] - Exit[t, 2]) * np.log(1 - a9)
        # Exit|New * ln(Pr[Exit|New]) + (State - Exit) * ln(1 - Pr[Exit|New])
        LL[t, 3] = Adopt[t, 1] * np.log(a10) + (State[t, 3] - Adopt[t, 1]) * np.log(1 - a10)
        # Adopt|PE * ln(Pr[Adopt|PE]) + (State - Adopt) * ln(1 - Pr[Adopt|PE])
        print(f'Log likelihood = {np.sum(LL[t, :]):10.4f}')

    total_LL = np.sum(LL)
    print(f"Finished iteration {iterMLE} with phi, kappa_inc, kappa_ent = ({phi:.8f}, {kappa_inc:.8f}, {kappa_ent:.8f})")
    print(f'Log Likelihood = {-total_LL:10.10f}')
    print(f"Elapsed time = {time.time() - start_time:.2f} seconds")

    iterMLE += 1

    if output_type == 1:
        return -total_LL
    else:
        return total_LL
