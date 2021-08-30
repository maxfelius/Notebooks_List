'''
#
@author: Max Felius
@date: 05/05/2021


'''

#imports
import numpy as np
import sys, os, time

#import personal functions

from sinkhole_functions.influence_functions import *

#functions
def create_matching_len(t,y,r):
    '''
    The time vector has a fixed number of epochs
    The y and r vector length is based on the number of points selected.

    The same vectors are returned but all have the same length

    :type r: np.array([float]) mx1
    :type y: np.array([float]) mxn
    :type t: np.array([float]) nx1 

    :rtype: np.array([float]) (mxn)x1, np.array([float]) (mxn)x1, np.array([float]) (mxn)x1 
    '''
    t_length = len(t)
    r_length = len(r)

    #pre allocate space for the return vectors
    t_vector = np.array([])
    y_vector = y.T.ravel()
    r_vector = np.array([])

    #loop over each epoch
    for item in t:
        t_temp = np.array([item for _ in range(r_length)])

        t_vector = np.concatenate((t_vector,t_temp))
        r_vector = np.concatenate((r_vector,r))

    return t_vector, y_vector, r_vector

def kinematic_model(R,r,y,t):
    '''
    :type R: int
    :type r: list[float] (mxn)x1
    :type y: list[float] (mxn)x1
    :type t: list[float] (mxn)x1 

    :rtype: float, float, float
    '''

    #create design matrix
    A = t * Gaussian_Influence_Function(R,r) #shape=((mxn)x1)
    A = A.reshape(len(y),1)

    #stochastic matrix
    W = np.eye((len(y)))

    #compute solutions
    invW = np.linalg.inv(W)

    #make an exceotion for when a matrix is singular
    try:
        Qxhat = np.linalg.inv(A.T @ invW @ A)
    except:
        # print('Exception...')
        # return 0,0,0
        return np.nan, np.nan, np.nan
        # return 1, 1, 1
    
    #the subsidence velocity
    xhat = Qxhat @ A.T @ invW @ y

    yhat = A @ xhat
    ehat = y - yhat
    
    #calculate the fit of the equation
    fit = 100*(1-(np.sum(ehat @ ehat.T)/np.sum((y-np.mean(y))**2)))
    
    return xhat, Qxhat, fit


def kinematic_model_old(R,r,y_data):
    '''
    Function to determine the subsidence velocity
    
    linear least squares
    '''
    #creating the LSQ
    A = Gaussian_Influence_Function(R,r) #len(x_range) by 1 matrix
    y = y_data

    A = A.reshape((1,len(y)))

    #stochastic matrix
    W = np.eye((len(y)))

    #compute solutions
    invW = np.linalg.inv(W)
    try:
        Qxhat = np.linalg.inv(A @ invW @ A.T)
    except:
        print('Exception...')
        return 0,0,0
    
    #the subsidence velocity
    xhat = Qxhat @ A @ invW @ y

    yhat1 = A.T @ xhat
    ehat = y - yhat1
    
    fit = 100*(1-(np.sum(ehat @ ehat.T)/np.sum((y_data-np.mean(y_data))**2)))
    
    return xhat, fit, Qxhat

def filter_extremes(item,maxvalue=0.1,minvalue=0.0000001):
    if item == 0:
        return np.nan
    
    if item > maxvalue:
        return np.nan
#         return maxvalue
    if item < minvalue:
        return np.nan
#         return minvalue
    else:
        return item

def linear_model(x_vector,y_vector):
    A = x_vector
    y = y_vector
    
    A = A.reshape((1,len(y)))
    
    #stochastic matrix
    W = np.eye((len(y)))
    
    #compute solutions
    invW = np.linalg.inv(W)
    try:
        Qxhat = np.linalg.inv(A @ invW @ A.T)
    except:
        print('Exception...')
        return np.nan,np.nan,np.nan
    
    #the subsidence velocity
    xhat = Qxhat @ A @ invW @ y

    yhat1 = A.T @ xhat
    ehat = y - yhat1
    
#     fit = 100*(1-(np.sum(ehat @ ehat.T)/np.sum((y_data-np.mean(y_data))**2)))
    
    return xhat, Qxhat

#filter for extreme values
def filter_extremes(item,maxvalue=0.1,minvalue=0.0000001):
    if item == 0:
        return np.nan
    
    if item > maxvalue:
        return np.nan
#         return maxvalue
    if item < minvalue:
        return np.nan
#         return minvalue
    else:
        return item
    
def filter_extremes2(item,maxvalue=0.1,minvalue=0.0000001):
    if item == 0:
        return np.nan
    
    if item > maxvalue:
        return np.nan
#         return maxvalue
    if item < minvalue:
        return np.nan
#         return minvalue
    else:
        return 1/item