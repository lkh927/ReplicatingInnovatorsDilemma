# Likelihood function to evaluate choices

# Setup
import numpy as np
import pandas as pd
import scipy.optimize
import time
import glob
import os

# Import (policy and transition) functions 
import fun1, fun2, fun3, fun4, fun5, fun6, fun7, fun8, fun9, fun10, fun11, fun12, fun13

# Import data 
data_folder = '/Users/annaabildskov/Desktop/Documents/Polit/3. sem KA/Dyn. Prog/TP_local/Translated/1 Summary Statistics/Data'  # Change this to the actual path
csv_files = glob.glob(os.path.join(data_folder, '*.csv'))
# Read all CSVs into a list of DataFrames
data = {}
for file in csv_files:
    name = [pd.read_csv(file) for file in csv_files]
    data[name] = pd.read_csv(file)

# Pi = data['Pi']
State = data['State']
Exit = data['Exit']
Adopt = data['Adopt']
beta = delta = V = EV = Policy = Pi = None
T = len(State)      # Number of periods (years)

iterMLE = 1         # Iteration counter for MLE


def Likelihood(Theta, output_type):
    global beta, delta, Pi, V, EV, Policy, State, Exit, Adopt, T, iterMLE

    phi, kappa_inc, kappa_ent = Theta
    print(f"\nMLE iter #{iterMLE:4.0f}: trying (phi, kappa_inc, kappa_ent) = ({phi:.8f}, {kappa_inc:.8f}, {kappa_ent:.8f})")

    start_time = time.time()

    for t in reversed(range(0, T)):     # Using backwards induction, so starting for the last period and deducting until first period
        Vprime = np.zeros((6480,))      # 3*12*12*15 (type, no_prime, nb_prime, nn_prime)
        for type in range(3):
            for no_prime in range(12):
                for nb_prime in range(12):
                    for nn_prime in range(15):
                        idx = type + 3*no_prime + 3*12*nb_prime + 3*12*12*nn_prime
                        Vprime[idx] = V[t, type, no_prime, nb_prime, nn_prime]

        No = State[t, 0]
        Nb = State[t, 1]
        Nn = State[t, 2]
        Npe = State[t, 3]
        Npe_prime = State[t+1, 3]
        statenum = 0

        for no in range(12):
            for nb in range(12):
                for nn in range(15):
                    gap = 666
                    iterNE = 0
                    
                    # EV1 - EV5 for tomorrows state
                    if no > 0:
                        z1 = V[t+1, 0, State[t+1,0]+1, State[t+1,1]+1, State[t+1,2]+1]
                        z2 = V[t+1, 1, State[t+1,0]+1, State[t+1,1]+1, State[t+1,2]+1]
                    else:
                        z1 = z2 = 0
                    if nb > 0:
                        z3 = V[t+1, 1, State[t+1,0]+1, State[t+1,1]+1, State[t+1,2]+1]
                    else:
                        z3 = 0
                    if nn > 0:
                        z4 = V[t+1, 2, State[t+1,0]+1, State[t+1,1]+1, State[t+1,2]+1]
                    else:
                        z4 = 0
                    if Npe > 0:
                        z5 = V[t+1, 2, State[t+1,0]+1, State[t+1,1]+1, State[t+1,2]+1]
                    else:
                        z5 = 0

                    # Policies from initial EV1 - EV5
                    if no > 0:
                        z6old = fun6(z1, z2, beta, phi, kappa_inc, delta, t)
                        z7old = fun7(z1, z2, beta, phi, kappa_inc, delta, t)
                    else:
                        z6old = z7old = 0

                    if nb > 0:
                        z8old = fun8(z3, beta, phi)
                    else:
                        z8old = 0

                    if nn > 0:
                        z9old = fun9(z4, beta, phi)
                    else:
                        z9old = 0

                    if Npe > 0:
                        z10old = fun10(z5, beta, kappa_ent, delta, t)
                    else:
                        z10old = 0

                    # Initialize iteration over beliefs and policies
                    while gap > 0.01 and iterNE < 10:
                        if no > 0:
                            z1 = fun1(z6old, z7old, z8old, z9old, z10old, no, nb, nn, Npe, Npe_prime, Vprime)
                            z2 = fun2(z6old, z7old, z8old, z9old, z10old, no, nb, nn, Npe, Npe_prime, Vprime)
                            z6 = (fun6(z1, z2, beta, phi, kappa_inc, delta, t) + z6old) /2
                            z7 = (fun7(z1, z2, beta, phi, kappa_inc, delta, t) + z7old) /2
                        else:
                            z1 = z2 = z6 = z7 = 0

                        if nb > 0:
                            z3 = fun3(z6, z7, z8old, z9old, z10old, no, nb, nn, Npe, Npe_prime, Vprime)
                            z8 = (fun8(z3, beta, phi) + z8old) / 2
                        else:
                            z3 = z8 = 0

                        if nn > 0:
                            z4 = fun4(z6, z7, z8, z9old, z10old, no, nb, nn, Npe, Npe_prime, Vprime)
                            z9 = (fun9(z4, beta, phi) + z9old) / 2
                        else:
                            z4 = z9 = 0

                        if Npe > 0:
                            z5 = fun5(z6, z7, z8, z9, z10old, no, nb, nn, Npe, Npe_prime, Vprime)
                            z10 = (fun10(z5, beta, kappa_ent, delta, t) + z10old) / 2
                        else:
                            z5 = z10 = 0

                        gap = abs(z6 - z6old) + abs(z7 - z7old) + abs(z8 - z8old) + abs(z9 - z9old) + abs(z10 - z10old)
                        
                        # Update values and interation counter
                        z6old, z7old, z8old, z9old, z10old = z6, z7, z8, z9, z10
                        iterNE += 1

                    # Update expected values and policies    
                    EV[t+1, :, no+1, nb+1, nn+1] = [z1, z2, z3, z4, z5]
                    Policy[t, :, no+1, nb+1, nn+1] = [z6, z7, z8, z9, z10]

                    if no > 0:
                        V[t, 0, no+1, nb+1, nn+1] = Pi[t, 0, no+1, nb+1, nn+1] + 0.57722 + fun11(z1, z2, beta, phi, kappa_inc, delta, t)
                    else:
                        V[t, 0, no+1, nb+1, nn+1] = 0
                    if nb > 0:
                        V[t, 1, no+1, nb+1, nn+1] = Pi[t, 1, no+1, nb+1, nn+1] + 0.57722 + fun12(z3, beta, phi)
                    else:
                        V[t, 1, no+1, nb+1, nn+1] = 0
                    if nn > 0:
                        V[t, 2, no+1, nb+1, nn+1] = Pi[t, 2, no+1, nb+1, nn+1] + 0.57722 + fun13(z4, beta, phi)
                    else:
                        V[t, 2, no+1, nb+1, nn+1] = 0
                    
                    # Print progress
                    print(f'Expected Value (z1, z2, z3, z4, z5) = ({z1:.2f}, {z2:.2f}, {z3:.2f}, {z4:.2f}, {z5:.2f})')
                    print(f'Choice Probabilities (z6, z7, z8, z9, z10) = ({z6:.4f}, {z7:.4f}, {z8:.4f}, {z9:.4f}, {z10:.4f})')
                    print(f'Value today (Vo, Vb, Vn) = ({V[t-1, 0, no, nb, nn]:.2f}, {V[t-1, 1, no, nb, nn]:.2f}, {V[t-1, 2, no, nb, nn]:.2f})')

                statenum += 1
            print(f'First iteration finished on state = {statenum}. Time = {time.time() - start_time:.2f} seconds')


    # Joint choice probabilities (LL of observing choices in actual data over period and type)
    LL = np.zeros((T - 1, 4))
    for t in range(T - 1):
        No = State[t, 0]
        Nb = State[t, 1]
        Nn = State[t, 2]
        Npe = State[t, 3]
        Npe_prime = State[t+1, 3]
        print(f"Actual state in year {t}: (No, Nb, Nn, Npe, Npe_prime) = ({No},{Nb},{Nn},{Npe},{Npe_prime})")

        a6 = Policy[t, 0, No+1, Nb+1, Nn+1]
        a7 = Policy[t, 1, No+1, Nb+1, Nn+1]
        a8 = Policy[t, 2, No+1, Nb+1, Nn+1]
        a9 = Policy[t, 3, No+1, Nb+1, Nn+1]
        a10 = Policy[t, 4, No+1, Nb+1, Nn+1]
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
        LL[t-1, 0] = Exit[t, 0] * np.log(a6) + Adopt[t-1, 0] * np.log(a7) + (State[t, 0] - Exit[t, 0] - Adopt[t, 0]) * np.log(1 - a6 - a7)
        LL[t-1, 1] = Exit[t, 1] * np.log(a8) + (State[t, 1] - Exit[t, 1]) * np.log(1 - a8)
        LL[t-1, 2] = Exit[t, 2] * np.log(a9) + (State[t, 2] - Exit[t, 2]) * np.log(1 - a9)
        LL[t-1, 3] = Adopt[t, 1] * np.log(a10) + (State[t, 3] - Adopt[t, 1]) * np.log(1 - a10)
        print(f'Log likelihood = {np.sum(LL[t-1, :]):10.4f}')

    total_LL = np.sum(LL)
    print(f"Finished iteration {iterMLE} with phi, kappa_inc, kappa_ent = ({phi:.8f}, {kappa_inc:.8f}, {kappa_ent:.8f})")
    print(f'Log Likelihood = {-total_LL:10.10f}')
    print(f"Elapsed time = {time.time() - start_time:.2f} seconds")

    iterMLE += 1

    return -total_LL if output_type == 1 else total_LL
