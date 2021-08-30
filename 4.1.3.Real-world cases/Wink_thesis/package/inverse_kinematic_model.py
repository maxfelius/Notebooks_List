'''
@author: Max Felius

The inverse kinematic model script
'''

import numpy as np
# from package.zg import zg
import time, os, sys

def check_itype(itype):
    '''
    Checking which influence function to import
    '''
    if itype.lower() == 'gauss':
        from package.stochastic_inverse_lsq import inverse_kinematic_model
        return inverse_kinematic_model
    else:
        print(f'Type: {itype} is unknown')
        return 0

def inverse_kinematic_model(v,t,R,r,y,itype='gauss',verbose='on'):
    '''
    Non-Linear Least Squares for determining kinematic model parameters

    Input:
    :type v: float
    :type t: np.array(float)
    :type R: float
    :type r: np.array(float)
    :type y: np.array(float)

    Output
    :rtype R: float
    :rtype v: float
    '''

    inv_kin_model = check_itype(itype)

    if inv_kin_model != 0:
        return inv_kin_model(v,t,R,r,t,verbose)
    else:
        return 0

    #maximum number of runs
    n = 100

    #initial values
    Qyy = np.eye(len(r))
    invQyy = np.linalg.inv(Qyy)

    #start the timer
    start = time.time()

    for i in range(n):
        #expected deformation
        yhat = v*t*zg(R,r)

        #compute the difference in measured and computed subsidence
        dy = y - yhat

        #defining the jacobian matrix
        A1 = t*zg(R,r)
        A2 = ((2*v*t*np.pi*r**2)/(R**3))*zg(R,r)

        J = np.array([A1,A2]).T

        Qxhat = np.linalg.inv(J.T @ invQyy @ J)
        dx = Qxhat @ J.T @ invQyy @ dy

        v_old = v
        R_old = R
        v = v + dx[0]
        R = R + dx[1]

        dx_hat = np.array([v_old-v,R_old-R]).T

        if dx_hat.T @ Qxhat @ dx_hat < sys.float_info.epsilon:
            if verbose.lower() == 'on':
                print(f'Stopped at iteration {i+1}.\nThe computed values are v={v} and R={R}.')
            break

    if i == n-1:
        print(f'Ended using the maximum number of iterations: {n}.\nThe computed values are v={v} and R={R}.')

    if verbose.lower() == 'on':
        print(f'The total runtime was: {time.time()-start} seconds.')

    return v, R
