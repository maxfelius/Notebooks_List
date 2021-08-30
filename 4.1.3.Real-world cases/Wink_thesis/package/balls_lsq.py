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
from tqdm import tqdm

def dkzdR(R,theta,r):
    return (2*R*r**2 * np.tan(theta)**2)/((R**2 + r**2 * np.tan(theta)**2)**2)

def dkzdtheta(R,theta,r):
    return (2*R**2 * r**2 * np.tan(theta) * (1/np.cos(theta))**2)/((R**2 +r**2 * np.tan(theta)**2)**2)

def zg(R,r,theta):
    H = R/np.tan(theta)
    return np.cos(np.arctan(r/H))**2

def inverse_kinematic_model(v,t,R,r,y,theta,verbose='on'):
    '''
    Non-Linear Least Squares for determining kinematic model parameters

    Input:
    :type v: float
    :type t: np.array(float)
    :type R: float
    :type r: np.array(float)
    :type y: np.array(float)
    :type theta: float

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
        yhat = v*t*zg(R,r,theta)

        #compute the difference in measured and computed subsidence
        dy = y - yhat

        #defining the jacobian matrix
        A1 = t*zg(R,r,theta)
        # A2 = ((2*v*t*np.pi*r**2)/(R**3))*zg(R,r)
        A2 = v*t*dkzdR(R,theta,r) #R
        A3 = v*t*dkzdtheta(R,theta,r) #theta

        J = np.array([A1,A2,A3]).T

        Qxhat = np.linalg.inv(J.T @ invQyy @ J)
        dx = Qxhat @ J.T @ invQyy @ dy

        v_old = v
        R_old = R
        theta_old = theta
        v = v + dx[0]
        R = R + dx[1]
        theta = theta + dx[2]

        dx_hat = np.array([v_old-v,R_old-R,theta_old-theta]).T

        if dx_hat.T @ Qxhat @ dx_hat < sys.float_info.epsilon:
            if verbose.lower() == 'on':
                print(f'Stopped at iteration {i+1}.\nThe computed values are v={v} and R={R}.')
            break

    if i == n-1:
        print(f'Ended using the maximum number of iterations: {n}.\nThe computed values are v={v} and R={R}.')

    if verbose.lower() == 'on':
        print(f'The total runtime was: {time.time()-start} seconds.')

    return v, R, theta

def center_determination(t,x,y,x0_array,data_list,delta_days,nitems,v_in,R_in,theta,verbose='on'):
    '''
    Function to determine the center of the sinkhole based on the RMSE
    '''
    # v_in = 1
    # R_in = np.max(x)/2

    RMSE_out = []

    if verbose.lower() == 'off':
        for x0 in x0_array:
            r = np.sqrt((x-x0)**2)

            try:
                gv, gR, gTheta = inverse_kinematic_model(v_in,t,R_in,r,y,theta,verbose='off')
            except:
                gv = 0
                gR = 1

        #     fit_list = np.zeros((3,nitems))
            RMSE_list = np.zeros((1,nitems))

            for i in range(nitems):
                #compute some parameters
                y_data = data_list[i][1].values/100 #from cm to meter
                x1 = data_list[i][0].values
                r1 = np.sqrt((x1-x0)**2)

                #computing the gaussian model and fit
                y1 = gv*delta_days[i]*zg(gR,r1,gTheta)
                ehat = y_data - y1
                gfit = 100*(1-(np.nansum(abs(ehat))/np.nansum(abs(y_data))))
    #             fit_list[0,i] = gfit
                gaus_RMSE = np.sqrt((ehat @ ehat.T)/len(ehat))*1000
                RMSE_list[0,i] = gaus_RMSE

            avg_gRMSE = np.nansum(RMSE_list[0,:])/(nitems)

            RMSE_out.append(avg_gRMSE)

    elif verbose.lower() == 'on':
        for x0 in tqdm(x0_array,'Determining Center Position'):
            r = np.sqrt((x-x0)**2)

            try:
                gv, gR, gTheta = inverse_kinematic_model(v_in,t,R_in,r,y,theta,verbose='off')
            except:
                gv = 0
                gR = 1
                gTheta = 0

        #     fit_list = np.zeros((3,nitems))
            RMSE_list = np.zeros((1,nitems))

            for i in range(nitems):
                #compute some parameters
                y_data = data_list[i][1].values/100 #from cm to meter
                x1 = data_list[i][0].values
                r1 = np.sqrt((x1-x0)**2)

                #computing the gaussian model and fit
                y1 = gv*delta_days[i]*zg(gR,r1,gTheta)
                ehat = y_data - y1
                gfit = 100*(1-(np.nansum(abs(ehat))/np.nansum(abs(y_data))))
    #             fit_list[0,i] = gfit
                gaus_RMSE = np.sqrt((ehat @ ehat.T)/len(ehat))*1000
                RMSE_list[0,i] = gaus_RMSE

            avg_gRMSE = np.nansum(RMSE_list[0,:])/(nitems)

            RMSE_out.append(avg_gRMSE)
    else:
        print(f'{verbose} input unknown.')

    return np.array(RMSE_out)