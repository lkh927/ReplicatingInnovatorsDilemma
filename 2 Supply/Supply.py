import numpy as np
import pandas as pd
import os
from types import SimpleNamespace
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from functools import partial



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
        par.Yd = self.load_csv("Yd", data_folder).flatten()

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

            # Calculate and store ABCDEFGH
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
        

    def foc(self, q, t, MC, No, Nb, Nn):
        """Takes following inputs for a GIVEN time period:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        No: number of "old_only" firms
        Nb: number of "both" firms
        Nn: number of "new_only" firms
        """
        par = self.par

        Qo = No * q[0] + Nb * q[1]
        Qn = Nb * q[2] + Nn * q[3]
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))
        
        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = Po + dPoQo * q[0] - MC[0]
        foc_bo = Po + dPoQo * q[1] + dPnQo * q[2] - MC[0]
        foc_bn = Pn + dPnQn * q[2] + dPoQn * q[1] - MC[3]
        foc_n  = Pn + dPnQn * q[3] - MC[3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F
    
    
    def nonlcon(self, q, t, MC, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        Qo = No * q[0] + Nb * q[1]
        Qn = Nb * q[2] + Nn * q[3]
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([Po - MC[0], Pn - MC[3]]).flatten()

        # Constraint group (ii): qo ≥ qbo, qn ≥ qbn
        c2 = np.array([q[0] - q[1], q[3] - q[2]])

        # Constraint group (iii): Q0 ≥ 0.0001
        c3 = np.array([Q0 - 0.0001])

        # Combine all inequality constraints
        c = np.concatenate([c1, c2, c3])

        return c


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
        Bigq = np.zeros((par.T, 4, 12, 12, 15))
        BigQ = np.zeros((par.T, 3, 12, 12, 15))
        BigP = np.zeros((par.T, 2, 12, 12, 15))
        BigPi = np.zeros((par.T, 3, 12, 12, 15))

        # Loop over time periods
        for t in range(par.T):
            Mkt = par.M[t]
            MC = self.MC()['MC']

            q0_base = q_actual[t, :].copy()
            q0 = np.array([0.1, 0.1, 0.1, 0.1])
            lb = np.full(4, 0.0001)
            ub = np.full(4, Mkt)
            bounds = [(lb[i], ub[i]) for i in range(4)]

            # Loop over all possible values of No, Nb, Nn
            for No in range(0,5):  # 0 to 11
                for Nb in range(0,5): # 0 to 11
                    for Nn in range(0,5): # 0 to 14
                        print(f'\nYear: {t+1}, State: ({No}, {Nb}, {Nn})')

                        A = np.array([No, Nb, Nb, Nn])

                        if t >= 14:
                        #    q0 = q0_base / 2
                        #    while np.dot(A, q0) > Mkt:
                        #        q0 = q0 / 2
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
                                q0 = [0.0001, 0.0001, 0.0001, 0.0001]      

                        # Skip the case where all are zero
                        if No == 0 and Nb == 0 and Nn == 0:
                            q = np.zeros(4)
                            qo = qbo = qbn = qn = 0
                        # Choose the appropriate objective and constraint functions
                        else: 
                            if No > 0 and Nb > 0 and Nn > 0:
                                obj_func = partial(self.foc, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                                constraint_func = partial(self.nonlcon, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                            elif No > 0 and Nb > 0 and Nn == 0:
                                obj_func = partial(self.foc_110, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                                constraint_func = partial(self.nonlcon_110, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                            elif No > 0 and Nb == 0 and Nn > 0:
                                obj_func = partial(self.foc_101, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                                constraint_func = partial(self.nonlcon_101, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                            elif No > 0 and Nb == 0 and Nn == 0:
                                obj_func = partial(self.foc_100, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                                constraint_func = partial(self.nonlcon_100, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                            elif No == 0 and Nb > 0 and Nn > 0:
                                obj_func = partial(self.foc_011, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                                constraint_func = partial(self.nonlcon_011, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                            elif No == 0 and Nb > 0 and Nn == 0:
                                obj_func = partial(self.foc_010, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                                constraint_func = partial(self.nonlcon_010, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                            elif No == 0 and Nb == 0 and Nn > 0:
                                obj_func = partial(self.foc_001, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)
                                constraint_func = partial(self.nonlcon_001, MC=MC[t], t=t, No=No, Nb=Nb, Nn=Nn)

                            A_local = A.copy()
                            Mkt_local = Mkt
                            # Set up constraints
                            constraints = [
                                {'type': 'ineq', 'fun': lambda q: Mkt_local - np.dot(A_local, q)},
                                {'type': 'ineq', 'fun': constraint_func}
                                ]
                            
                            # Run optimization
                            res = minimize(
                                obj_func, q0, method='SLSQP', bounds=bounds,
                                constraints=constraints, options={'disp': False, 'maxiter': 1000})
                        
                            q = res.x
                            qo = q[0]
                            qbo = q[1]
                            qbn = q[2]
                            qn = q[3]
                        
                        #Derive aggregate variables
                        Qo = No * qo + Nb * qbo
                        Qn = Nn * qn + Nb * qbn
                        Q0 = Mkt - Qo - Qn

                        if No == 0 and Nb == 0:
                            Po = 0
                        else:
                            Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])

                        if Nn == 0 and Nb == 0:
                            Pn = 0
                        else: 
                            Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])
                        
                        # Calculate profits
                        pi_o = (Po - MC[t,0]) * qo
                        pi_b = (Po - MC[t,0]) * qbo + (Pn - MC[t,3]) * qbn
                        pi_n = (Pn - MC[t,3]) * qn

                        Bigq[t,0,No+1,Nb+1,Nn+1] = qo
                        Bigq[t,1,No+1,Nb+1,Nn+1] = qbo
                        Bigq[t,2,No+1,Nb+1,Nn+1] = qbn
                        Bigq[t,3,No+1,Nb+1,Nn+1] = qn

                        BigQ[t,0,No+1,Nb+1,Nn+1] = Qo
                        BigQ[t,1,No+1,Nb+1,Nn+1] = Qn
                        BigQ[t,2,No+1,Nb+1,Nn+1] = Q0

                        BigP[t,0,No+1,Nb+1,Nn+1] = Po
                        BigP[t,1,No+1,Nb+1,Nn+1] = Pn

                        BigPi[t,0,No+1,Nb+1,Nn+1] = pi_o
                        BigPi[t,1,No+1,Nb+1,Nn+1] = pi_b
                        BigPi[t,2,No+1,Nb+1,Nn+1] = pi_n

                        print(f'(qo, qbo, qbn, qn): {qo:.2f}, {qbo:.2f}, {qbn:.2f}, {qn:.2f}')
                        print(f'(Qo, Qn, Q0): {Qo:.2f}, {Qn:.2f}, {Q0:.2f}')
                        print(f'(Po, Pn): {Po:.2f}, {Pn:.2f}')
                        print(f'(pi_o, pi_b, pi_n): {pi_o:.2f}, {pi_b:.2f}, {pi_n:.2f}')

        return Bigq, BigQ, BigP, BigPi


    def foc_001(self, q, t, MC, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par
        
        Qo = No * 0 + Nb * 0
        Qn = Nb * 0 + Nn * q[3]
        Q0 = par.M[t] - Qo - Qn

        Po = 0
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = 0
        dPnQo = 0
        dPoQn = 0
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = q[0]
        foc_bo = q[1]
        foc_bn = q[2]
        foc_n  = Pn + dPnQn * q[3] - MC[3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F


    def foc_010(self, q, t, MC, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par

        Qo = No * 0 + Nb * q[1]
        Qn = Nb * q[2] + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = q[0]
        foc_bo = Po + dPoQo * q[1] + dPnQo * q[2] - MC[0]
        foc_bn = Pn + dPnQn * q[2] + dPoQn * q[1] - MC[3]
        foc_n  = q[3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F


    def foc_100(self, q, t, MC, No, Nb, Nn):
        """Takes following inputs for a GIVEN time period:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        No: number of "old_only" firms
        Nb: number of "both" firms
        Nn: number of "new_only" firms
        """
        par = self.par

        Qo = No * q[0] + Nb * 0
        Qn = Nb * 0 + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = 0

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 0
        dPoQn = 0
        dPnQn = 0

        foc_o  = Po + dPoQo * q[0] - MC[0]
        foc_bo = q[1]
        foc_bn = q[2]
        foc_n  = q[3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F


    def foc_011(self, q, t, MC, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par

        Qo = No * 0 + Nb * q[1]
        Qn = Nb * q[2] + Nn * q[3]
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = q[0]
        foc_bo = Po + dPoQo * q[1] + dPnQo * q[2] - MC[0]
        foc_bn = Pn + dPnQn * q[2] + dPoQn * q[1] - MC[3]
        foc_n  = Pn + dPnQn * q[3] - MC[3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F



    def foc_101(self, q, t, MC, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par

        Qo = No * q[0] + Nb * 0
        Qn = Nb * 0 + Nn * q[3]
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = Po + dPoQo * q[0] - MC[0]
        foc_bo = q[1]
        foc_bn = q[2]
        foc_n  = Pn + dPnQn * q[3] - MC[3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F



    def foc_110(self, q, t, MC, No, Nb, Nn):
        """Takes following inputs:
        q: a vector of quantities produced by each type of firm, [qo, qbo, qbn, qn]
        MC: marginal cost of prodducing 5.25 and 3.5 inch HDD's
        t: time period (0 to T-1)
        """
        par = self.par

        Qo = No * q[0] + Nb * q[1]
        Qn = Nb * q[2] + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        Po = np.real((-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t]))
        Pn = np.real((-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t]))

        dPoQo = (Qo + Q0) / (par.alpha1 * Qo * Q0)
        dPnQo = 1 / (par.alpha1 * Q0)
        dPoQn = 1 / (par.alpha1 * Q0)
        dPnQn = (Qn + Q0) / (par.alpha1 * Qn * Q0)

        foc_o  = Po + dPoQo * q[0] - MC[0]
        foc_bo = Po + dPoQo * q[1] + dPnQo * q[2] - MC[0]
        foc_bn = Pn + dPnQn * q[2] + dPoQn * q[1] - MC[3]
        foc_n  = q[3]

        F = foc_o**2 + foc_bo**2 + foc_bn**2 + foc_n**2

        # Alternatively, you could return the vector like this:
        # return np.array([foc_o, foc_bo, foc_bn, foc_n])
        return F


    def nonlcon_001(self, q, t, MC, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        Qo = No * 0 + Nb * 0
        Qn = Nb * 0 + Nn * q[3]
        Q0 = par.M[t] - Qo - Qn

        # Compute price
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([Pn - MC[3]])

        # Constraint group (iii): Q0 > 0.0001
        c3 = np.array([Q0 - 0.0001])

        # Combine all inequality constraints
        c = np.concatenate([c1, c3])

        return c
    

    def nonlcon_010(self, q, t, MC, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        Qo = No * 0 + Nb * q[1]
        Qn = Nb * q[2] + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([Po - MC[0], Pn - MC[3]]).flatten()

        # Constraint group (iii): Q0 > 0.0001
        c3 = np.array([Q0 - 0.0001])

        # Combine all inequality constraints
        c = np.concatenate([c1, c3])

        return c
    

    def nonlcon_100(self, q, t, MC, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        Qo = No * q[0] + Nb * 0
        Qn = Nb * 0 + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([Po - MC[0]])

        # Constraint group (iii): Q0 > 0.0001
        c3 = np.array([Q0 - 0.0001])

        # Combine all inequality constraints
        c = np.concatenate([c1, c3])

        return c
    

    def nonlcon_011(self, q, t, MC, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        Qo = No * 0 + Nb * q[1]
        Qn = Nb * q[2] + Nn * q[3]
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([Po - MC[0], Pn - MC[3]]).flatten()

        # Constraint group (ii): qo > qbo, qn > qbn
        c2 = np.array([q[3] - q[2]])

        # Constraint group (iii): Q0 > 0.0001
        c3 = np.array([Q0 - 0.0001])

        # Combine all inequality constraints
        c = np.concatenate([c1, c2, c3])

        return c
    

    def nonlcon_101(self, q, t, MC, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        Qo = No * q[0] + Nb * 0
        Qn = Nb * 0 + Nn * q[3]
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([Po - MC[0], Pn - MC[3]]).flatten()

        # Constraint group (iii): Q0 > 0.0001
        c3 =np.array([Q0 - 0.0001])

        # Combine all inequality constraints
        c = np.concatenate([c1, c3])

        return c


    def nonlcon_110(self, q, t, MC, No, Nb, Nn):
        """
        Nonlinear constraints used in optimization:
        - Ensures non-negative markups (Po >= MC_o and Pn >= MC_n)
        - Ensures firm-specific production ordering (qo > qbo, qn > qbn)
        - Ensures the outside good market share Q0 > 0
        """
        par = self.par

        Qo = No * q[0] + Nb * q[1]
        Qn = Nb * q[2] + Nn * 0
        Q0 = par.M[t] - Qo - Qn

        # Compute prices
        Po = (-1 / par.alpha1) * (-np.log(Qo / Q0) + par.alpha2 * 0 + par.alpha3 * par.X[t, 0] + par.Xe[t, 0] + par.Yd[t])
        Pn = (-1 / par.alpha1) * (-np.log(Qn / Q0) + par.alpha2 * 1 + par.alpha3 * par.X[t, 1] + par.Xe[t, 1] + par.Yd[t])

        # Constraint group (i): Prices - Marginal Costs ≥ 0
        c1 = np.array([Po - MC[0], Pn - MC[3]]).flatten()

        # Constraint group (ii): qo > qbo, qn > qbn
        c2 = np.array([q[0] - q[1]])

        # Constraint group (iii): Q0 > 0.0001
        c3 = np.array([Q0 - 0.0001])

        # Combine all inequality constraints
        c = np.concatenate([c1, c2, c3])

        return c
