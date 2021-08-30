'''
@author: Max Felius

Function that creates all combination possible given the number or rows
'''

# imports
import numpy as np

def create_tuple_pairs(n):
    '''
    :type n: int
    :rtype: list
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
