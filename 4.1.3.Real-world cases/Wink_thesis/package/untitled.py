'''
@author: Max Felius

The inverse kinematic model script

This script runs a non-linear lsq to estimate v and R

This script is specifically created for the balls influence function
'''
import numpy as np
# from package.geometric_models import gaussian as zg
# from package.geometric_models import dkzdR_gaussian as dkz
import time, os, sys

def dkzdR(R,theta,r):
    return (2*R*r**2 * np.tan(theta)**2)/((R**2 + r**2 * np.tan(theta)**2)**2)

def dkzdtheta(R,theta,r):
    return (2*R**2 * r**2 * np.tan(theta) * (1/np.cos(theta))**2)/((R**2 +r**2 * np.tan(theta)**2)**2)

def inverse_kinematic_model(v,t,R,r,y,verbose='on'):
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
    #differential equations
    # dkzdR = (2*R*r**2 * np.tan(theta)**2)/((R**2 + r**2 * np.tan(theta)**2)**2)
    # dkzdtheta = (2*R**2 * r**2 * np.tan(theta) * (1/np.cos(theta))**2)/((R**2 +r**2 * np.tan(theta)**2)**2)

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
        # A2 = ((2*v*t*np.pi*r**2)/(R**3))*zg(R,r)
        A2 = v*t*dkzdR(R,r)

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