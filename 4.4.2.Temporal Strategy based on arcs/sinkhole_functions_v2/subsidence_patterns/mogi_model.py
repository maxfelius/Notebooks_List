'''
@created: 26/01/2021
@author: Max Felius

Script to apply the mogi model on the dataset
'''

#imports
import numpy as np

def mogi(v,x,z,x0,z0):
    r = np.sqrt((x-x0)**2 + (z-z0)**2)
    return ((1-v)/np.pi) * np.array([(z-z0)/r**3])

def least_squares_mogi(t,v,x,z,x0,z0,y_measurements):
    '''
    Linear Least Squares
    '''
    #initial values
    Qyy = np.eye(len(x))
    invQyy = np.linalg.inv(Qyy)

    A = t * mogi(v,x,z,x0,z0)
    A = A.T #743x2

    Qxhat = np.linalg.inv(A.T @ invQyy @ A)

    xhat = Qxhat @ A.T @ invQyy @ y_measurements

    return xhat
