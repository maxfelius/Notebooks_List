'''
@author: Max Felius
'''

#imports
import datatime
import numpy as np

def get_delta_days(epochs):
    dates = list(map(lambda x: datetime.datetime.strptime(x,'d_%Y%m%d'),epochs))
    start_date = dates[0]
    dates_days = np.array(list(map(lambda x: (x-start_date).days,dates)))

    return dates_days, start_date
