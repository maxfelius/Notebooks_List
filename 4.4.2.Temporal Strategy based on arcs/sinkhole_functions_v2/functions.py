'''
# Function Repository
@author: Max Felius
@date 04/05/2021
@version: 0.0.0

This is a repository file with small but usefull functions
'''

#imports
import numpy as np
import datetime
import os, sys, re, time
import pandas as pd

def get_delta_days(epochs):
    '''
    :type epochs: list
    :rtype: np.array[float]

    Function that uses a list of epochs and transforms is relative days w.r.t. the first epoch in the list. The first epoch is return separately.
    '''

    dates = get_sentinel_datetime(epochs)
    start_date = dates[0]
    dates_days = np.array(list(map(lambda x: (x-start_date).days,dates)))

    return dates_days, start_date



def create_tuple_pairs(n):
    '''
    :type n: int
    :rtype: list
    
    Function returning a list with tuples of all the unique combinations possible.
    '''
    tuple_list = []

    print('Creating tuple list.')

    #create matrix of ones with the locations of connections
    combination_matrix = np.ones((n,n))
    lower = combination_matrix[np.tril_indices(n, k = -1)]

    combination_matrix2 = np.zeros((n,n))
    combination_matrix2[np.tril_indices(n, k = -1)] = lower

    for x in range(combination_matrix2.shape[0]):
        for y in range(combination_matrix2.shape[1]):
            if combination_matrix2[x,y] == 1:
                tuple_list.append((x,y))

    return tuple_list

def get_sentinel_days(headers):
    '''
    :type headers: list
    :rtype list

    Function returning a list with only Sentinel 1 epochs (removes non epoch headers).
    '''
    return list(filter(lambda x: re.compile(r'd_\d{8}').match(x) != None, headers))

def get_sentinel_datetime(epochs):
    '''
    :type epochs: list[string]
    :rtype: list[datetime]
    '''
    return list(map(lambda x: datetime.datetime.strptime(x,'d_%Y%m%d'),epochs))


def linear_model(epochs,data):
        '''
        Function creating the linear model for detect arcs behaving anomalous
        '''

        #creating time vector
        delta_days, start_day = get_delta_days(epochs)
        
        #pre-allocate space for the output variables
        a = []
        b = []
        sigma_ehat = []
        
        for i in range(len(data)):
            '''
            Loop creating a linear model per row
            '''
            
            #setting up the system of equations
            y = np.array(data[epochs].iloc[i])
            A = np.array((delta_days,np.ones([len(delta_days)])))
            
            #stochastic matrix
            W = np.eye((len(y)))
            
            #compute solutions
            invW = np.linalg.inv(W)
            Qxhat = np.linalg.inv(A @ invW @ A.T)
            xhat = Qxhat @ A @ invW @ y
            
            yhat = A.T @ xhat
            ehat = y - yhat
            
            #compute the standard deviation of the noise of an arc
            sigma_ehat_out = np.sqrt((np.sum((ehat - np.mean(ehat))**2))/len(y))
            
            #saving the data
            a.append(xhat[0])
            b.append(xhat[1])
            sigma_ehat.append(sigma_ehat_out)
        
        return a, b, sigma_ehat