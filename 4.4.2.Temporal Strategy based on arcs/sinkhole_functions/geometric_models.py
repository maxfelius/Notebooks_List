'''
# Geometric Models
@author: Max Felius
@date: 05/05/2021

Script for the influence function

Script containing all the different geometric models

The contains the following influence functions:
- Gaussian (stochastic)
- Bals' 
- Scanns'
- Ehrhardt and Sauer
- Beyer
- Sanns
- bals

'''
import numpy as np

#function to select one of the functions below
def kinematic_model(R,r,name,theta=35):
	'''
	:type name: string
	:type R: int
	:type r: np.array([float])
	'''
	if name.lower() == 'gaussian':
		return gaussian(R,r)
	elif name.lower() == 'scanns':
		return scanns(r)
	elif name.lower() == 'beyer':
		return beyer(R,r)
	elif name.lower() == 'sann':
		return sann(R,r)
	elif name.lower() == 'bals':
		return bals(R,r,theta)
	else:
		print(f'Model: {name} is unknown. Please use another model.')
		return

def gaussian(R,r):
	'''
	:type R: int
	:type r: np.array([float])
	:rtype: np.array([float])
	'''
	return np.exp(-np.pi * (r**2/R**2))

def dkzdR_gaussian(R,r):
	'''
	:type R: int
	:type r: np.array([float])
	:rtype: np.array([float])
	'''
	return ((2*np.pi*r**2)/(R**3))*np.exp(-np.pi * (r**2/R**2))

def scanns(r):
	'''
	:type r: np.array([float])
	:rtype: np.array([float])
	'''
	return 2.256*(1/r)*np.exp(-4*r**2)

def ehrhardt(r):
	'''
	:type r: np.array([float])
	:rtype: np.array([float])
	'''
	return 0.1392*np.exp(-0.5*r**2)

def beyer(R,r):
	'''
	:type R: int
	:type r: np.array([float])
	:rtype: np.array([float])
	'''
	return (3/(np.pi*R**2))*(1-(r/R)**2)**2

def dkzdR_beyer(R,r):
	'''
	:type R: int
	:type r: np.array([float])
	:rtype: np.array([float])
	'''
	return (-6*(R**2 -3*r**2)*(R**2 - r**2))/(np.pi*R**7)

def sann(R,r):
	'''
	:type R: int
	:type r: np.array([float])
	:rtype: np.array([float])
	'''
	return (2/(np.pi*np.sqrt(np.pi)*R))*(1/r)*np.exp(-4*(r/R)**2)

def	dkzdR_sann(R,r):
	'''
	:type R: int
	:type r: np.array([float])
	:rtype: np.array([float])
	'''
	return (2*np.exp(-(4*r**2)/R**2)*(8*r**2 - R**2))/(np.pi**(3/2) * r * R**4)

def bals(R,r,theta):
	print(f'Bals geometric model selected. Using a theta of {theta} degrees.')
	theta = np.deg2rad(theta)
	H = R/np.tan(theta)
	return np.cos(np.arctan(r/H))**2