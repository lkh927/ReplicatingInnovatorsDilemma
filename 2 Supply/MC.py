import numpy as np
import pandas as pd
import os

def load_csv(filename, folder):
    return pd.read_csv(os.path.join(folder, f"{filename}.csv"), header=0).values

def find_MC(data_folder):
    # Load data
    alpha1 = load_csv("alpha1", data_folder)[0, 0]
    M = load_csv("M", data_folder).flatten()
    P = load_csv("P", data_folder)
    Q = load_csv("Q", data_folder)
    State = load_csv("State", data_folder)

    T = 18  # Number of periods

    # Initialize result containers
    dPdQ = np.zeros((T, 4))
    ePQ = np.zeros((T, 4))
    ABCDEFGH = np.zeros((T, 8))
    q = np.zeros((T, 4))
    MC = np.zeros((T, 4))

    # Special case for t=0 (1981)
    t = 0
    No, Nb, Nn = State[t, 0], State[t, 1], State[t, 2]
    m = M[t]
    Qo, Qn, Q0 = Q[t, 0], Q[t, 1], Q[t, 2]
    Po, Pn = P[t, 0], P[t, 1]
    so, sn, s0 = Qo/m, Qn/m, Q0/m

    dPoQo = 1 / (alpha1 * Qo)
    dPnQo = 1 / (alpha1 * Q0)
    dPoQn = 1 / (alpha1 * Q0)

    dPdQ[t, :] = [dPoQo, 0, dPnQo, dPoQn]
    ePoQo = -dPoQo * (Qo / Po)
    ePQ[t, :] = [ePoQo, 0, 0, 0]
    qo = Qo / No
    q[t, :] = [qo, 0, 0, 0]
    MCo = Po + dPoQo * qo
    MC[t, :] = [MCo, 0, 0, 0]

    # Special case for t=1 (1982)
    t = 1
    No, Nb, Nn = State[t, 0], State[t, 1], State[t, 2]
    m = M[t]
    Qo, Qn, Q0 = Q[t, 0], Q[t, 1], Q[t, 2]
    Po, Pn = P[t, 0], P[t, 1]
    so, sn, s0 = Qo/m, Qn/m, Q0/m

    dPoQo = 1 / (alpha1 * Qo)
    dPnQn = 1 / (alpha1 * Qn)
    dPnQo = 1 / (alpha1 * Q0)
    dPoQn = 1 / (alpha1 * Q0)

    dPdQ[t, :] = [dPoQo, dPnQn, dPnQo, dPoQn]
    ePoQo = -dPoQo * (Qo / Po)
    ePQ[t, :] = [ePoQo, 0, 0, 0]
    qo = Qo / No
    qn = Qn / Nn
    q[t, :] = [qo, 0, 0, qn]
    MCo = Po + dPoQo * qo
    MCn = Pn + dPnQn * qn
    MC[t, :] = [MCo, 0, 0, MCn]

    for t in range(2, T):  # Corresponds to MATLAB t = 3:18    
        No, Nb, Nn = State[t, 0], State[t, 1], State[t, 2]
        m = M[t]
        Qo, Qn, Q0 = Q[t, 0], Q[t, 1], Q[t, 2]
        Po, Pn = P[t, 0], P[t, 1]

        so, sn, s0 = Qo/m, Qn/m, Q0/m

        dPoQo = 1 / (alpha1 * Qo)
        dPnQn = 1 / (alpha1 * Qn)
        dPnQo = 1 / (alpha1 * Q0)
        dPoQn = 1 / (alpha1 * Q0)

        dPdQ[t, :] = [dPoQo, dPnQn, dPnQo, dPoQn]

        ePoQo = -dPoQo * (Qo / Po)
        ePnQn = -dPnQn * (Qn / Pn)
        ePnQo = -dPnQo * (Qo / Pn)
        ePoQn = -dPoQn * (Qn / Po)
        ePQ[t, :] = [ePoQo, ePnQn, ePnQo, ePoQn]

        A = dPnQn * (Qn / Nb)
        B = dPoQn * (Qo / Nb)
        C = dPoQn * (No / Nb)
        D = dPnQn * (1 + Nn / Nb)
        E = dPoQn * (Qo / Nb)
        F = dPnQo * (Qn / Nb)
        G = dPnQo * (Nn / Nb)
        H = dPoQo * (1 + No / Nb)
        ABCDEFGH[t, :] = [A, B, C, D, E, F, G, H]

        qo = Qo / (No + Nb)
        qn = Qn / (Nn + Nb)
        qbo = Qo / Nb - (No / Nb) * qo
        qbn = Qn / Nb - (Nn / Nb) * qn
        q[t, :] = [qo, qbo, qbn, qn]

        MCo = Po + dPoQo * qo
        MCn = Pn + dPnQn * qn
        MCbo = Po + dPoQo * qbo + dPnQo * qbn
        MCbn = Pn + dPnQn * qbn + dPoQn * qbo
        MC[t, :] = [MCo, MCbo, MCbn, MCn]

    return {
        "dPdQ": dPdQ,
        "ePQ": ePQ,
        "ABCDEFGH": ABCDEFGH,
        "q": q,
        "MC": MC
    }
