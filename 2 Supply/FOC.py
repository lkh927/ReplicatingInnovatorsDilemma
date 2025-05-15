import numpy as np
import pandas as pd
import os

# Declare globals
alpha1 = alpha2 = alpha3 = None
Mkt = X_o = X_n = Xe_o = Xe_n = YearDummy = None
MC_o = MC_n = None
No = Nb = Nn = None

def load_globals(folder_path="."):
    global alpha1, alpha2, alpha3
    global Mkt, X_o, X_n, Xe_o, Xe_n, YearDummy
    global MC_o, MC_n
    global No, Nb, Nn

    def load_scalar(name):
        path = os.path.join(folder_path, f"{name}.csv")
        return pd.read_csv(path).iloc[0, 0]

    alpha1 = load_scalar("alpha1")
    alpha2 = load_scalar("alpha2")
    alpha3 = load_scalar("alpha3")
    Mkt = load_scalar("Mkt")
    X_o = load_scalar("X_o")
    X_n = load_scalar("X_n")
    Xe_o = load_scalar("Xe_o")
    Xe_n = load_scalar("Xe_n")
    YearDummy = load_scalar("YearDummy")
    MC_o = load_scalar("MC_o")
    MC_n = load_scalar("MC_n")
    No = load_scalar("No")
    Nb = load_scalar("Nb")
    Nn = load_scalar("Nn")

def foc(q):
    alpha1 = -3.28454
    alpha2 = 0.909773
    alpha3 = 1.204684
    Mkt = 56638.8
    X_o = 6.490788
    X_n = 6.240812
    Xe_o = -0.4157396
    Xe_n = 0.4135973
    YearDummy = -5.653561
    MC_o = 1.1213105727517398
    MC_n = -2.916521500397822
    No = 11
    Nb = 11
    Nn = 14
    #demand parameters

    Qo = No * q[0] + Nb * q[1] 
    # Aggregate quantity of 5.25 inch HDD's:
    # Number of "old_only" firms * quantity of 5.25 inch HDD's produced by "old_only" firms
    # + Number of "both" firms * quantity of 5.25 inch HDD's produced by "both" firms
    Qn = Nb * q[2] + Nn * q[3]
    # Aggregate quantity of 3.5 inch HDD's:
    # Number of "both" firms * quantity of 3.5 inch HDD's produced by "both" firms
    # + Number of "new_only" firms * quantity of 3.5 inch HDD's produced by "new_only" firms
    Q0 = Mkt - Qo - Qn
    # Aggregate quantity of other sizes?
    # Mkt must be aggregate of ALL types - so minus 5.25 inch and 3.5 inch,
    # We get the quantity of other sizes

    Po = np.real((-1 / alpha1) * (-np.log(Qo / Q0) + alpha2 * 0 + alpha3 * X_o + Xe_o + YearDummy))
    # See equation (8) on p. 819 - this is p isolated in that with j = old
    Pn = np.real((-1 / alpha1) * (-np.log(Qn / Q0) + alpha2 * 1 + alpha3 * X_n + Xe_n + YearDummy))
    # Same thing, but with j = new

    dPoQo = (Qo + Q0) / (alpha1 * Qo * Q0)
    # Analytical derivative of price of 5.25 inch HDD's wrt. the quantity of 5.25 inch HDD's
    dPnQo = 1 / (alpha1 * Q0)
    # Analytical derivative of price of 3.5 inch HDD's wrt. the quantity of 5.25 inch HDD's
    dPoQn = 1 / (alpha1 * Q0)
    # Analytical derivative of price of 5.25 inch HDD's wrt. the quantity of 3.5 inch HDD's
    dPnQn = (Qn + Q0) / (alpha1 * Qn * Q0)
    # Analytical derivative of price of 3.5 inch HDD's wrt. the quantity of 3.5 inch HDD's

    foc_o  = Po + dPoQo * q[0] - MC_o
    foc_bo = Po + dPoQo * q[1] + dPnQo * q[2] - MC_o
    foc_bn = Pn + dPnQn * q[2] + dPoQn * q[1] - MC_n
    foc_n  = Pn + dPnQn * q[3] - MC_n

    F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

    # Alternatively, you could return the vector like this:
    # return np.array([foc_o, foc_bo, foc_bn, foc_n])
    return F