'''
@author: Max Felius

Script for loading the data in seperate folders
'''

import numpy as np
import datetime
import re
import os, sys, time
import pandas as pd

def sinkhole_data_loader(folder_list):
    '''
    Creating a switch that loads and reads the data of the correct files
    '''
    #dict save
    dsinkhole = {}

    for folder in folder_list:
        if folder == 'Wink2016':
            dsinkhole[folder] = {}

            start_date = '20150421'
            start_date_datetime = datetime.datetime.strptime(start_date,'%Y%m%d')
            date_list = []
            delta_days = []
            data_list = []

            for date in sorted(os.listdir(folder)):
                if date.endswith('.csv'):
                    #get the date from the title
                    m = re.search(r'\d{8}',date)
                    date_conv = datetime.datetime.strptime(m.group(0),'%Y%m%d')
                    date_list.append(date_conv)

                    #Determine the number of days since the start date
                    delta_days.append((date_conv-start_date_datetime).days)

                    #Read the data from the files
                    data_list.append(pd.read_csv(os.path.join(folder,date),header=None))

            dsinkhole[folder]['date_list'] = date_list
            dsinkhole[folder]['delta_days'] = delta_days
            dsinkhole[folder]['data_list'] = data_list
            dsinkhole[folder]['Initial Values'] = {'R_init':470,'v_init':1000,'Expected_X0':480}

        elif folder == 'Wink2019':
            dsinkhole[folder] = {}

            start_date = '20151016'
            start_date_datetime = datetime.datetime.strptime(start_date,'%Y%m%d')
            date_list = []
            delta_days = []
            data_list = []

            for date in sorted(os.listdir(folder)):
                if date.endswith('.csv'):
                    #get the date from the title
                    m = re.search(r'\d{8}',date)
                    date_conv = datetime.datetime.strptime(m.group(0),'%Y%m%d')
                    date_list.append(date_conv)

                    #Determine the number of days since the start date
                    delta_days.append((date_conv-start_date_datetime).days)

                    #Read the data from the files
                    data_list.append(pd.read_csv(os.path.join(folder,date),header=None))

            dsinkhole[folder]['date_list'] = date_list
            dsinkhole[folder]['delta_days'] = delta_days
            dsinkhole[folder]['data_list'] = data_list
            dsinkhole[folder]['Initial Values'] = {'R_init':500,'v_init':1000,'Expected_X0':310}

        elif folder == 'Nof2019':
            dsinkhole[folder] = {}

            start_date = '111230'
            start_date_datetime = datetime.datetime.strptime(start_date,'%y%m%d')
            date_list = []
            delta_days = []
            data_list = []

            for date in sorted(os.listdir(folder)):
                if date.endswith('.csv'):
                    #get the date from the title
                    m = re.search(r'\d{6}',date)
                    date_conv = datetime.datetime.strptime(m.group(0),'%y%m%d')
                    date_list.append(date_conv)

                    #Determine the number of days since the start date
                    delta_days.append((date_conv-start_date_datetime).days)

                    #Read the data from the files
                    data_list.append(pd.read_csv(os.path.join(folder,date),header=None))

            dsinkhole[folder]['date_list'] = date_list
            dsinkhole[folder]['delta_days'] = delta_days
            dsinkhole[folder]['data_list'] = data_list
            dsinkhole[folder]['Initial Values'] = {'R_init':60,'v_init':100,'Expected_X0':35}

        elif folder == 'Nof2013':
            dsinkhole[folder] = {}

            start_date = '111230'
            start_date_datetime = datetime.datetime.strptime(start_date,'%y%m%d')
            date_list = []
            delta_days = []
            data_list = []

            for date in sorted(os.listdir(folder)):
                if date.endswith('.csv'):
                    #get the date from the title
                    m = re.search(r'\d{6}',date)
                    date_conv = datetime.datetime.strptime(m.group(0),'%y%m%d')
                    date_list.append(date_conv)

                    #Determine the number of days since the start date
                    delta_days.append((date_conv-start_date_datetime).days)

                    #Read the data from the files
                    data_list.append(pd.read_csv(os.path.join(folder,date),header=None))

            dsinkhole[folder]['date_list'] = date_list
            dsinkhole[folder]['delta_days'] = delta_days
            dsinkhole[folder]['data_list'] = data_list
            dsinkhole[folder]['Initial Values'] = {'R_init':60,'v_init':100,'Expected_X0':60}

        elif folder == 'Baer2018_1':
            dsinkhole[folder] = {}

            start_date = '20111230'
            start_date_datetime = datetime.datetime.strptime(start_date,'%Y%m%d')
            date_list = []
            delta_days = []
            data_list = []

            for date in sorted(os.listdir(folder)):
                if date.endswith('.csv'):
                    #get the date from the title
                    m = re.search(r'111214-\d{6}',date)
                    date_conv = datetime.datetime.strptime(m.group(0)[7:],'%y%m%d')
                    date_list.append(date_conv)

                    #Determine the number of days since the start date
                    delta_days.append((date_conv-start_date_datetime).days)

                    #Read the data from the files
                    data_list.append(pd.read_csv(os.path.join(folder,date),header=None))

            dsinkhole[folder]['date_list'] = date_list
            dsinkhole[folder]['delta_days'] = delta_days
            dsinkhole[folder]['data_list'] = data_list
            dsinkhole[folder]['Initial Values'] = {'R_init':30,'v_init':100,'Expected_X0':36}

        elif folder == 'Baer2018_2':
            dsinkhole[folder] = {}

            start_date = '140703'
            start_date_datetime = datetime.datetime.strptime(start_date,'%y%m%d')
            date_list = []
            delta_days = []
            data_list = []

            for date in sorted(os.listdir(folder)):
                if date.endswith('.csv'):
                    #get the date from the title
                    m = re.search(r'140617-\d{6}',date)
                    date_conv = datetime.datetime.strptime(m.group(0)[7:],'%y%m%d')
                    date_list.append(date_conv)

                    #Determine the number of days since the start date
                    delta_days.append((date_conv-start_date_datetime).days)

                    #Read the data from the files
                    data_list.append(pd.read_csv(os.path.join(folder,date),header=None))

            dsinkhole[folder]['date_list'] = date_list
            dsinkhole[folder]['delta_days'] = delta_days
            dsinkhole[folder]['data_list'] = data_list
            dsinkhole[folder]['Initial Values'] = {'R_init':40,'v_init':100,'Expected_X0':90}

        elif folder == 'Baer2018_3':
            dsinkhole[folder] = {}

            start_date = '150519'
            start_date_datetime = datetime.datetime.strptime(start_date,'%y%m%d')
            date_list = []
            delta_days = []
            data_list = []

            for date in sorted(os.listdir(folder)):
                if date.endswith('.csv'):
                    #get the date from the title

                    m = re.search(r'150519_\d{6}',date)
                    date_conv = datetime.datetime.strptime(m.group(0)[7:],'%y%m%d')
                    date_list.append(date_conv)

                    #Determine the number of days since the start date
                    delta_days.append((date_conv-start_date_datetime).days)

                    #Read the data from the files
                    data_list.append(pd.read_csv(os.path.join(folder,date),header=None))

            dsinkhole[folder]['date_list'] = date_list
            dsinkhole[folder]['delta_days'] = delta_days
            dsinkhole[folder]['data_list'] = data_list
            dsinkhole[folder]['Initial Values'] = {'R_init':60,'v_init':100,'Expected_X0':120}

        else:
            print(f'Unknown folder: {folder}.')

    return dsinkhole
