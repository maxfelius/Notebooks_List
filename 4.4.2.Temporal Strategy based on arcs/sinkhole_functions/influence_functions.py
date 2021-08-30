'''
#Influence Functions
@author: Max Felius
@date: 05/05/2021

This is a file containing all the influence functions used for this thesis
'''

#imports 
import numpy as np

def Gaussian_Influence_Function(R,r):
    '''
    :type R: int
    :type r: np.array([float])
    :rtype: np.array([float])
    '''
    return np.exp(-np.pi*(r**2/R**2))

