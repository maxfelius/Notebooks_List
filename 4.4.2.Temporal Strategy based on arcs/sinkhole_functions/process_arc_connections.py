'''
@author: Max Felius

# Function to get the epochs:
filter_string = re.compile(r'd_\d{8}')
epochs = list(filter(lambda x: filter_string.match(x) != None, list(data)))
'''

#imports
import numpy as np
import pandas as pd
import sys, os, time
from tqdm import tqdm
import re

class process_arc_connections:
    def __init__(self,data):
        #dataset characteristics
        self.data = data
        self.all_headers = list(data)
        self.epoch_headers = self.filter_sentinel_epochs(self.all_headers)
        
        #saved variables
        self.tuple_list = None
        self.processed_data = None

    def get_processed_data(self):
        '''
        method to return the processed data
        '''
        return self.processed_data

    def save_processed_data(self,filename):
        '''
        Method to save the processed data

        filename: string
        '''
        self.processed_data.to_csv(filename)

        print(f'The processed data is saved at: {filename}')

    def filter_sentinel_epochs(self,headers):
        '''
        Simple function to filter out Sentinel epochs form the header list
        '''
        filter_string = re.compile(r'd_\d{8}')
        return list(filter(lambda x: filter_string.match(x) != None, headers))
    
    def create_tuple_pairs(self,n):
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

    def process_arc_connections(self):
        '''
        Computes the difference between two points for all epochs. Processes the arcs provided by the create_tuple_pairs method.

        Outputs WKT format for arcs and arc differences

        :type data: pandas dataframe
        :type epochs: list[]
        :rtype: pandas dataframe
        '''
        #self.data is the dataset that is loaded in with the initialization
        n = len(self.data)
        self.tuple_list = self.create_tuple_pairs(n)
        
        #headers containing the coordinates of the points
        coordinates = ['pnt_lon','pnt_lat','pnt_rdx','pnt_rdy']

        #creating the dataset
        arc_dataset = {}

        #creating lists for location parameters
        arc_dataset['Arc'] = self.tuple_list
        arc_dataset['geometry (rd)'] = []
        arc_dataset['geometry (wgs)'] = []
        arc_dataset['Distance (m)'] = []
        arc_dataset['point'] = [] #midpoint of the line
        arc_dataset['lon'] = []
        arc_dataset['lat'] = []
        arc_dataset['rdx'] = []
        arc_dataset['rdy'] = []

        #start with the arc processing procedure
        for i in tqdm(range(len(self.epoch_headers)),'Processing Arc Connections...'):
            epoch = self.epoch_headers[i]
            arc_dataset[epoch] = []

            for pair in self.tuple_list:
                #taking the difference between 1 pair of two points (i.e. arc)
                # print(epoch,pair[0],pair[1])
                # test_b = self.data[epoch].iloc[pair[0]]
                # test_c = self.data[epoch].iloc[pair[1]]
                # test_a = test_b-test_c
                # arc_dataset[epoch].append(test_a)
                arc_dataset[epoch].append(self.data[epoch].iloc[pair[0]]-self.data[epoch].iloc[pair[1]])

                #use the first epoch to create the location parameters
                if i == 0:
                    #points lat/lon
                    point_lon = [self.data[coordinates[0]].iloc[pair[0]],self.data[coordinates[0]].iloc[pair[1]]]
                    point_lat = [self.data[coordinates[1]].iloc[pair[0]],self.data[coordinates[1]].iloc[pair[1]]]

                    arc_dataset['lon'].append(point_lon)
                    arc_dataset['lat'].append(point_lat)

                    point_rdx = [self.data[coordinates[2]].iloc[pair[0]],self.data[coordinates[2]].iloc[pair[1]]]
                    point_rdy = [self.data[coordinates[3]].iloc[pair[0]],self.data[coordinates[3]].iloc[pair[1]]]

                    arc_dataset['rdx'].append(point_rdx)
                    arc_dataset['rdy'].append(point_rdy)

                    # wgs coordinates
                    point1 = f'{self.data[coordinates[0]].iloc[pair[0]]} {self.data[coordinates[1]].iloc[pair[0]]}'
                    point2 = f'{self.data[coordinates[0]].iloc[pair[1]]} {self.data[coordinates[1]].iloc[pair[1]]}'

                    arc_dataset['geometry (wgs)'].append(f'LINESTRING ({point1},{point2})')
                    
                    x_new = (self.data[coordinates[0]].iloc[pair[1]] + self.data[coordinates[0]].iloc[pair[0]])/2
                    y_new = (self.data[coordinates[1]].iloc[pair[1]] + self.data[coordinates[1]].iloc[pair[0]])/2                    

                    arc_dataset['point'].append(f'POINT ({x_new},{y_new})')

                    point3 = f'{self.data[coordinates[2]].iloc[pair[0]]} {self.data[coordinates[3]].iloc[pair[0]]}'
                    point4 = f'{self.data[coordinates[2]].iloc[pair[1]]} {self.data[coordinates[3]].iloc[pair[1]]}'

                    arc_dataset['geometry (rd)'].append(f'LINESTRING ({point3},{point4})')

                    p1 = [self.data[coordinates[2]].iloc[pair[0]],self.data[coordinates[3]].iloc[pair[0]]]
                    p2 = [self.data[coordinates[2]].iloc[pair[1]],self.data[coordinates[3]].iloc[pair[1]]]
                    
                    arc_dataset['Distance (m)'].append(f'{np.round(np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))}')
                    
        print('Finished processing arc connections.')
        self.processed_data = pd.DataFrame.from_dict(arc_dataset)
        
        # return self.processed_data
