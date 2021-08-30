'''
Created: 26/01/2020
@author: Max Felius

Script with the different influence functions used. The default function is the Gaussian (stochastic) influence function.

## Note
- When using the bals function, make sure to use the cavity depth instead of the radius of influence (R)

## References:
- H. Kratzsch, Mining subsidence engineering.  SpringerScience & Business Media, 1983.
- G. Ren, D. Reddish, and B. Whittaker, “Mining subsi-dence and displacement prediction using influence func-tion methods,”Mining Science and Technology, vol. 5,pp. 89–104, may 1987.
'''

#imports
import numpy as np

#defining the different influence functions
def zg(R,r,itype='gaus'):
    '''
    Automatically uses the Gaussian Influence Function unless specified differently
    '''
    if itype == 'gaus':
        return -zg_gaus(R,r)
    elif itype == 'bals':
        return -zg_bals(R,r)
    elif itype == 'beyer':
        return -zg_beyer(R,r)
    else:
        print(f'Unknown itype: {itype}.')

def zg_gaus(R,r):
    return np.exp(-np.pi*(r**2/R**2))

def zg_bals(H,r):
#     r = np.sqrt((x-x0)**2 + (y-y0)**2)
    zone = np.arctan(r/H)
    return np.cos(zone)**2

def zg_beyer(R,r):
#     r = np.sqrt((x-x0)**2 + (y-y0)**2)
    kz = ((3)/(np.pi))*(1-(r/R)**2)**2
    kz[r>R] = 0
    return kz
