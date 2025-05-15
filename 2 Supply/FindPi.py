# FindPi.py

import numpy as np
from scipy.optimize import minimize
from FOC import foc
from nonlcon import constraints  # assuming constraints() returns {'type': 'ineq', 'fun': ...}

# Assuming "MC" and "q" are imported or defined globally from previous module
# MC[:, 0] -> MC_o
# MC[:, 1] -> MC (not used)
# MC[:, 3] -> MC_n

def find_pi(q, MC):
    # Unpack data dictionary
    alpha1, alpha2, alpha3 = data['alpha1'], data['alpha2'], data['alpha3']
    M = data['M']
    X = data['X']
    Xe = data['Xe']
    Yd = data['Yd']
    MC = data['MC']
    q_input = data['q']
    
    # Result arrays
    Bigq = np.zeros((18, 4, 12, 12, 15))
    BigQ = np.zeros((18, 3, 12, 12, 15))
    BigP = np.zeros((18, 2, 12, 12, 15))
    BigPi = np.zeros((18, 3, 12, 12, 15))
    
    for t in range(18):
        globals().update({
            'alpha1': alpha1, 'alpha2': alpha2, 'alpha3': alpha3,
            'Mkt': M[t],
            'X_o': X[t, 0], 'X_n': X[t, 1],
            'Xe_o': Xe[t, 0], 'Xe_n': Xe[t, 1],
            'YearDummy': Yd[t],
            'MC_o': MC[t, 0], 'MC_n': MC[t, 3]
        })

        q0_base = q_input[t, :].copy()
        q0_base[1] = q_input[t, 0]  # avoid zeros
        q0_base[2] = q0_base[3] if t > 0 else q0_base[2]
        q0 = np.full(4, 0.1)
        lb = np.full(4, 0.0001)
        ub = np.full(4, M[t])

        for No in range(1, 12):  # 1 to 11
            for Nb in range(1, 12):
                for Nn in range(1, 15):  # 1 to 14
                    globals().update({'No': No, 'Nb': Nb, 'Nn': Nn})

                    A = np.array([No, Nb, Nb, Nn])
                    q0_trial = q0_base / 2
                    while np.dot(A, q0_trial) > M[t]:
                        q0_trial /= 2

                    result = minimize(
                        foc,
                        q0_trial,
                        method='SLSQP',
                        bounds=[(lb[i], ub[i]) for i in range(4)],
                        constraints=[constraints()],
                        options={'disp': False}
                    )

                    if not result.success:
                        q = np.zeros(4)
                    else:
                        q = result.x

                    qo, qbo, qbn, qn = q
                    Qo = No * qo + Nb * qbo
                    Qn = Nn * qn + Nb * qbn
                    Q0 = M[t] - Qo - Qn

                    if No == 0 and Nb == 0:
                        Po = 0
                    else:
                        Po = (-1 / alpha1) * (-np.log(Qo / Q0) + alpha3 * X[t, 0] + Xe[t, 0] + Yd[t])
                    
                    if Nn == 0 and Nb == 0:
                        Pn = 0
                    else:
                        Pn = (-1 / alpha1) * (-np.log(Qn / Q0) + alpha2 + alpha3 * X[t, 1] + Xe[t, 1] + Yd[t])

                    pi_o = (Po - MC[t, 0]) * qo
                    pi_b = (Po - MC[t, 0]) * qbo + (Pn - MC[t, 3]) * qbn
                    pi_n = (Pn - MC[t, 3]) * qn

                    Bigq[t, :, No, Nb, Nn] = [qo, qbo, qbn, qn]
                    BigQ[t, :, No, Nb, Nn] = [Qo, Qn, Q0]
                    BigP[t, :, No, Nb, Nn] = [Po, Pn]
                    BigPi[t, :, No, Nb, Nn] = [pi_o, pi_b, pi_n]

    return {
        'Bigq': Bigq,
        'BigQ': BigQ,
        'BigP': BigP,
        'BigPi': BigPi
    }
