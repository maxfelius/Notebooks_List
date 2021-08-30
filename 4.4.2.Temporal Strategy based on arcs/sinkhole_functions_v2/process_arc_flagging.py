'''
@author: Max Felius

In this module the flagging procedure is setup in a class
'''

#imports
import numpy as np
import pandas as pd
import datetime
import tqdm

class process_arc_flagging:
    def __init__(self):
        '''
        Initialize object
        '''
        #data
        self.flagged_data = pd.DataFrame()
        
        #settings
        self.r_alpha_2 = 1.96

    def get_delta_day(self,epochs):
        dates = list(map(lambda x: datetime.datetime.strptime(x,'d_%Y%m%d'),epochs))
        start_date = dates[0]
        dates_days = np.array(list(map(lambda x: (x-start_date).days,dates)))

        return dates_days, start_date

    def check_earlier_flags(self,processed_data,row,latest_epoch):
        '''
        Method to check if the point at the new epoch was flagged before

        Checking the row in self.flagged_data

        row: int
        latest_epoch: string
        '''
        if self.processed_data[latest_epoch].iloc[row] != 0:
            return 1 + self.processed_data[latest_epoch].iloc[row]
        else:
            return 0

    def flagging(self,a,b,y,sigma_ehat,delta_day):
        '''
        Method for the flagging of an incoming observation

        a: float
        b: float
        y: float
        delta_days: float
        '''
        
        # get the trend value
        delta_d = a * delta_day + b

        #95% confidence interval
        #self.r_alpha_2 = 1.96
        conf_int = self.r_alpha_2*sigma_ehat

        if y + conf_int > delta_d and y - conf_int < delta_d:
            return 0
        else:
            return 1



