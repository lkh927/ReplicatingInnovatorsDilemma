import numpy as np
import pandas as pd
import os
from types import SimpleNamespace
import matplotlib.pyplot as plt
from scipy.optimize import minimize



class Supply():
    def __init__(self):
        self.par = SimpleNamespace()


    def load_csv(self, filename, folder):
        return pd.read_csv(os.path.join(folder, f"{filename}.csv"), header=0).values


    def setup(self, data_folder):
        par = self.par

        par.alpha1 = self.load_csv("alpha1", data_folder)[0, 0]
        par.alpha2 = self.load_csv("alpha2", data_folder)[0, 0]
        par.alpha3 = self.load_csv("alpha3", data_folder)[0, 0]
        par.M = self.load_csv("M", data_folder).flatten()
        par.P = self.load_csv("P", data_folder)
        par.Q = self.load_csv("Q", data_folder)
        par.State = self.load_csv("State", data_folder)
        par.X = self.load_csv("X", data_folder)
        par.Xe = self.load_csv("Xe", data_folder)
        par.Yd = self.load_csv("Yd", data_folder)

        par.T = 18  # Number of periods
  
    
    def MC(self):
        par = self.par

        #Initialize solution containers
        dPdQ = np.zeros((par.T, 4))
        ePQ = np.zeros((par.T, 4))
        ABCDEFGH = np.zeros((par.T, 8))
        q = np.zeros((par.T, 4))
        MC = np.zeros((par.T, 4))

        # Special case for t=0 (1981) - only old_only firms
        t = 0
        No, Nb, Nn = par.State[t, 0], par.State[t, 1], par.State[t, 2]
        m = par.M[t]
        Qo, Qn, Q0 = par.Q[t, 0], par.Q[t, 1], par.Q[t, 2]
        Po, Pn = par.P[t, 0], par.P[t, 1]
        so, sn, s0 = Qo/m, Qn/m, Q0/m

        # Calculate and store derivatives
        dPoQo = 1 / (par.alpha1 * Qo)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPdQ[t, :] = [dPoQo, 0, dPnQo, dPoQn]

        # Calculate and store elasticities
        ePoQo = -dPoQo * (Qo / Po)
        ePQ[t, :] = [ePoQo, 0, 0, 0]

        # Calculate and store quantities of 5.25 inch HDD's produced at t = 0
        # by each "old_only" firm
        qo = Qo / No
        q[t, :] = [qo, 0, 0, 0]

        # Calculate and store marginal cost of producing 5.25 inch HDD's at t = 0
        MCo = Po + dPoQo * qo
        MC[t, :] = [MCo, 0, 0, 0]

        # Special case for t=1 (1982) - "old_only" and "new_only" firms - still 0 "both" firms
        t = 1
        No, Nb, Nn = par.State[t, 0], par.State[t, 1], par.State[t, 2]
        m = par.M[t]
        Qo, Qn, Q0 = par.Q[t, 0], par.Q[t, 1], par.Q[t, 2]
        Po, Pn = par.P[t, 0], par.P[t, 1]
        so, sn, s0 = Qo/m, Qn/m, Q0/m

        # Calculate and store derivatives
        dPoQo = 1 / (par.alpha1 * Qo)
        dPnQn = 1 / (par.alpha1 * Qn)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPdQ[t, :] = [dPoQo, dPnQn, dPnQo, dPoQn]

        # Calculate and store elasticities
        ePoQo = -dPoQo * (Qo / Po)
        ePQ[t, :] = [ePoQo, 0, 0, 0]

        # Calculate and store quantities of 5.25 inch and 3.5 inch HDD's produced at t = 1
        # by each "old_only" and "new_only" firm
        qo = Qo / No
        qn = Qn / Nn
        q[t, :] = [qo, 0, 0, qn]

        # Calculate and store marginal cost of producing 5.25 inch and 3.5 inch HDD's t = 1
        MCo = Po + dPoQo * qo
        MCn = Pn + dPnQn * qn
        MC[t, :] = [MCo, 0, 0, MCn]

        # Loop through periods 2 to T-1 where there are "old_only", "both" AND "new_only" firms
        for t in range(2, par.T):
            No, Nb, Nn = par.State[t, 0], par.State[t, 1], par.State[t, 2]
            m = par.M[t]
            Qo, Qn, Q0 = par.Q[t, 0], par.Q[t, 1], par.Q[t, 2]
            Po, Pn = par.P[t, 0], par.P[t, 1]
            so, sn, s0 = Qo/m, Qn/m, Q0/m

            # Calculate and store derivatives
            dPoQo = 1 / (par.alpha1 * Qo)
            dPnQn = 1 / (par.alpha1 * Qn)
            dPnQo = 1 / (par.alpha1 * Q0)
            dPoQn = 1 / (par.alpha1 * Q0)
            dPdQ[t, :] = [dPoQo, dPnQn, dPnQo, dPoQn]

            # Calculate and store elasticities
            ePoQo = -dPoQo * (Qo / Po)
            ePnQn = -dPnQn * (Qn / Pn)
            ePnQo = -dPnQo * (Qo / Pn)
            ePoQn = -dPoQn * (Qn / Po)
            ePQ[t, :] = [ePoQo, ePnQn, ePnQo, ePoQn]

            # Calculate and store ABCDEFGH, still to be found out what is
            A = dPnQn * (Qn / Nb)
            B = dPoQn * (Qo / Nb)
            C = dPoQn * (No / Nb)
            D = dPnQn * (1 + Nn / Nb)
            E = dPoQn * (Qo / Nb)
            F = dPnQo * (Qn / Nb)
            G = dPnQo * (Nn / Nb)
            H = dPoQo * (1 + No / Nb)
            ABCDEFGH[t, :] = [A, B, C, D, E, F, G, H]        

            # Calculate and store quantities of 5.25 and 3.5 inch HDD's produced at t by each
            # "old_only", "new_only" and "both" firm
            qo = Qo / (No + Nb)
            qn = Qn / (Nn + Nb)
            qbo = Qo / Nb - (No / Nb) * qo
            qbn = Qn / Nb - (Nn / Nb) * qn
            q[t, :] = [qo, qbo, qbn, qn]

            # Calculate and store marginal cost of producing 5.25 and 3.5 incg HDD's at t
            # for "old_only", "new_only" and "both" firms
            MCo = Po + dPoQo * qo
            MCn = Pn + dPnQn * qn
            MCbo = Po + dPoQo * qbo + dPnQo * qbn
            MCbn = Pn + dPnQn * qbn + dPoQn * qbo
            MC[t, :] = [MCo, MCbo, MCbn, MCn]

        return {
            'dPdQ': dPdQ,
            'ePQ': ePQ,
            'ABCDEFGH': ABCDEFGH,
            'q': q,
            'MC': MC
        }
        

    def foc(self, q, MC, t, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par
        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * q[t,0] + Nb * q[t,1]
        Qn = Nb * q[t,2] + Nn * q[t,3]
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = Po + dPoQo * q[t,0] - MC[t, 0]
        foc_bo = Po + dPoQo * q[t,1] + dPnQo * q[t,2] - MC[t, 0]
        foc_bn = Pn + dPnQn * q[t,2] + dPoQn * q[t,1] - MC[t, 1]
        foc_n  = Pn + dPnQn * q[t,3] - MC[t, 1]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F
    
    
    def nonlcon(self, q, t, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * q[t, 0] + Nb * q[t, 1]
        Qn = Nb * q[t, 2] + Nn * q[t, 3]
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        MC_o = self.MC()['MC'][t, 0]
        MC_n = self.MC()['MC'][t, 3]

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([-(Po - MC_o), -(Pn - MC_n)])

        # Constraint group (ii): qo > qbo, qn > qbn
        c2 = np.array([q[t, 1] - q[t,0], q[t,2] - q[t,3]])

        # Constraint group (iii): Q0 > 0.0001
        c3 = -(Q0 - 0.0001)

        # Combine all inequality constraints
        c = np.concatenate([c1, c2, [c3]])

        # No equality constraints
        ceq = np.array([])

        return c, ceq


    def find_pi(self):
        par = self.par
        q = self.MC()['q']
        #MC = self.MC()['MC']

        # Initialize q with no zeros and only q_o and q_n (double column of q_o and double column of q_n)
        q_actual = q.copy()
        q_actual[:, 1] = q[:, 0]     # Avoid 0's (use column 1 instead of 2)
        q_actual[0, 3] = q[1, 3]     # Set the first row, 4th column to second row, 4th column of q
        q_actual[:, 2] = q_actual[:, 3]  # Set entire 3rd column equal to 4th column

        # Initialize solution containers
        q = np.zeros(1, 4)
        qo = qbo = qbn = qn = 0
        Qo = Qn = Q0 = 0
        Po = Pn = 0
        pi_o = pi_b = pi_n = 0
        Bigq = np.zeros((par.T, 4, 12, 12, 15))
        BigQ = np.zeros((par.T, 3, 12, 12, 15))
        BigP = np.zeros((par.T, 2, 12, 12, 15))
        BigPi = np.zeros((par.T, 3, 12, 12, 15))

        # Loop over time periods
        for t in range(par.T):
            Mkt = par.M[t]
            MC = self.MC()['MC']

            q0_base = q_actual[t, :].copy()
            q0 = np.full(4, 0.1)
            lb = np.full(4, 0.0001)
            ub = np.full(4, Mkt)
            bounds = [(lb[i], ub[i]) for i in range(4)]

            # Loop over all possible values of No, Nb, Nn
            for No in range(12):  # 0 to 11
                for Nb in range(12): # 0 to 11
                    for Nn in range(15): # 0 to 14
                        print(f'Year: {1981+t}, State (No, Nb, Nn): ({No},{Nb}{Nn})')
                        A = np.array([No, Nb, Nb, Nn])

                        if t >= 15:
                            q0 = q0_base / 2
                            while np.dot(A, q0) > Mkt:
                                q0 = q0 / 2
                            if No == 0:
                                q0[0] = 0.0001
                            if Nb == 0:
                                q0[1] = 0.0001
                                q0[2] = 0.0001
                            if Nn == 0:
                                q0[3] = 0.0001
                            if ((No >= 8 and Nn == 0) or
                                (No >= 11 and Nn == 1) or
                                (No == 0 and Nb == 10 and Nn == 8) or
                                (No == 10 and Nb == 4 and Nn == 2) or
                                (No == 11 and Nb == 2 and Nn == 2)):
                                q0 = np.array([0.0001, 0.0001, 0.0001, 0.0001])            



                        if No > 0 and Nb > 0 and Nn > 0:
                            q = None

        pass


    def foc_001(self, q, MC, t, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par
        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * 0 + Nb *0
        Qn = Nb * 0 + Nn * q[t,3]
        Q0 = par.M[t] - Qo - Qn

        Po = 0
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = 0
        dPnQo = 0
        dPoQn = 0
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = q[t,0]
        foc_bo = q[t,1]
        foc_bn = q[t,2]
        foc_n  = Pn + dPnQn * q[t,3] - MC[t, 1]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F


    def foc_010(self, q, MC, t, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par
        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * 0 + Nb * q[t,1]
        Qn = Nb * q[t,2] + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = q[t,0]
        foc_bo = Po + dPoQo * q[t,1] + dPnQo * q[t,2] - MC[t, 0]
        foc_bn = Pn + dPnQn * q[t,2] + dPoQn * q[t,1] - MC[t, 1]
        foc_n  = q[t,3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F


    def foc_100(self, q, MC, t, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par
        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * q[t,0] + Nb * 0
        Qn = Nb * 0 + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = 0

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 0
        dPoQn = 0
        dPnQn = 0

        foc_o  = Po + dPoQo * q[t,0] - MC[t, 0]
        foc_bo = q[t,1]
        foc_bn = q[t,2]
        foc_n  = q[t,3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F


    def foc_011(self, q, MC, t, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par
        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * 0 + Nb * q[t,1]
        Qn = Nb * q[t,2] + Nn * q[t,3]
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = q[t,0]
        foc_bo = Po + dPoQo * q[t,1] + dPnQo * q[t,2] - MC[t, 0]
        foc_bn = Pn + dPnQn * q[t,2] + dPoQn * q[t,1] - MC[t, 1]
        foc_n  = Pn + dPnQn * q[t,3] - MC[t, 1]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F



    def foc_101(self, q, MC, t, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par
        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * q[t,0] + Nb * 0
        Qn = Nb * 0 + Nn * q[t,3]
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = Po + dPoQo * q[t,0] - MC[t, 0]
        foc_bo = q[t,1]
        foc_bn = q[t,2]
        foc_n  = Pn + dPnQn * q[t,3] - MC[t, 1]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F



    def foc_110(self, q, MC, t, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par
        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * q[t,0] + Nb * q[t,1]
        Qn = Nb * q[t,2] + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = Po + dPoQo * q[t,0] - MC[t, 0]
        foc_bo = Po + dPoQo * q[t,1] + dPnQo * q[t,2] - MC[t, 0]
        foc_bn = Pn + dPnQn * q[t,2] + dPoQn * q[t,1] - MC[t, 1]
        foc_n  = q[t,3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F


    def nonlcon_001(self, q, t, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * 0 + Nb * 0
        Qn = Nb * 0 + Nn * q[t, 3]
        Q0 = par.M[t] - Qo - Qn

        # Compute price
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        MC_n = self.MC()['MC'][t, 3]

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = -(Pn - MC_n)

        # Constraint group (iii): Q0 > 0.0001
        c3 = -(Q0 - 0.0001)

        # Combine all inequality constraints
        c = np.concatenate([[c1], [c3]])

        # No equality constraints
        ceq = np.array([])

        return c, ceq
    

    def nonlcon_010(self, q, t, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * 0 + Nb * q[t, 1]
        Qn = Nb * q[t, 2] + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        MC_o = self.MC()['MC'][t, 0]
        MC_n = self.MC()['MC'][t, 3]

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([-(Po - MC_o), -(Pn - MC_n)])

        # Constraint group (iii): Q0 > 0.0001
        c3 = -(Q0 - 0.0001)

        # Combine all inequality constraints
        c = np.concatenate([c1, [c3]])

        # No equality constraints
        ceq = np.array([])

        return c, ceq
    

    def nonlcon_100(self, q, t, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * q[t, 0] + Nb * 0
        Qn = Nb * 0 + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        MC_o = self.MC()['MC'][t, 0]

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = -(Po - MC_o)

        # Constraint group (iii): Q0 > 0.0001
        c3 = -(Q0 - 0.0001)

        # Combine all inequality constraints
        c = np.concatenate([[c1], [c3]])

        # No equality constraints
        ceq = np.array([])

        return c, ceq
    

    def nonlcon_011(self, q, t, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * 0 + Nb * q[t, 1]
        Qn = Nb * q[t, 2] + Nn * q[t, 3]
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        MC_o = self.MC()['MC'][t, 0]
        MC_n = self.MC()['MC'][t, 3]

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([-(Po - MC_o), -(Pn - MC_n)])

        # Constraint group (ii): qo > qbo, qn > qbn
        c2 = q[t,2] - q[t,3]

        # Constraint group (iii): Q0 > 0.0001
        c3 = -(Q0 - 0.0001)

        # Combine all inequality constraints
        c = np.concatenate([c1, [c2], [c3]])

        # No equality constraints
        ceq = np.array([])

        return c, ceq
    

    def nonlcon_101(self, q, t, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * q[t, 0] + Nb * 0
        Qn = Nb * 0 + Nn * q[t, 3]
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        MC_o = self.MC()['MC'][t, 0]
        MC_n = self.MC()['MC'][t, 3]

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([-(Po - MC_o), -(Pn - MC_n)])

        # Constraint group (iii): Q0 > 0.0001
        c3 = -(Q0 - 0.0001)

        # Combine all inequality constraints
        c = np.concatenate([c1, [c3]])

        # No equality constraints
        ceq = np.array([])

        return c, ceq


    def nonlcon_110(self, q, t, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        #No = par.State[t, 0]
        #Nb = par.State[t, 1]
        #Nn = par.State[t, 2]

        Qo = No * q[t, 0] + Nb * q[t, 1]
        Qn = Nb * q[t, 2] + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        MC_o = self.MC()['MC'][t, 0]
        MC_n = self.MC()['MC'][t, 3]

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([-(Po - MC_o), -(Pn - MC_n)])

        # Constraint group (ii): qo > qbo, qn > qbn
        c2 = q[t, 1] - q[t,0]

        # Constraint group (iii): Q0 > 0.0001
        c3 = -(Q0 - 0.0001)

        # Combine all inequality constraints
        c = np.concatenate([c1, c2, [c3]])

        # No equality constraints
        ceq = np.array([])

        return c, ceq
