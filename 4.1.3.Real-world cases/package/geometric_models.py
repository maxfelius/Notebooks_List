'''
@author: Max Felius

Script for the influence function

Script containing all the different geometric models

The contains the following influence functions:
- Gaussian (stochastic)
- Bals' 
- Scanns'
- Ehrhardt and Sauer
- Beyer
- Sanns

'''

import numpy as np

def gaussian(R,r):
    return np.exp(-np.pi * (r**2/R**2))

def bals(zeta):
	return np.cos(zeta)**2

def scanns(r):
	return 2.256*(1/r)*np.exp(-4*r**2)

def ehrhardt(r):
	return 0.1392*np.exp(-0.5*r**2)

def beyer(R,r):
	return (3/(np.pi*R**2))*(1-(r/R)**2)**2

def sann(R,r):
	return (2/(np.pi*np.sqrt(np.pi)*R))*(1/r)*np.exp(-4*(r/R)**2)