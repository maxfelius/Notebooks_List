'''
@author: Max Felius

'''
#imports
import numpy as np

def arc_flagging(data_processed,epochs,start_epoch):
    '''
    The algortihm checks whether a point falls inside or outside the a particular confidence region

    Platform is needed to get the delta days. 

    Data of the subset used is defined in self.data

    :type data_processed: pandas DataFrame
    :type epochs: list[]
    :type start_epoch: int
    :rtype: pandas DataFrame
    '''
    
    print('Starting with arc flagging')
    
    #number of rows in the dataset
    n = len(data_processed)
    n_days = len(epochs)
    
    #pre-allocate space for variable to be exported
    temp = {}
    temp['SUMMED'] = [0 for _ in range(n)]
    
    '''
    compute the linear model for the training data
    take 50 epochs for training the model
    The first epoch is the reference epoch and is not taken
    into the model
    '''
    data_in = data_processed[epochs[1:start_epoch+1]]
    data_in = data_in.join(data_processed['Arc'])
    
    a, b, sigma_ehat = linear_model(epochs[1:start_epoch+1],data_in)
    
    #Create the delta days vector
    delta_days, start_day = get_delta_day(epochs)
    
    for idx in progressbar.progressbar(range(start_epoch,n_days-1)):
        '''
        Starting the arc flagging procedure
        '''
        
        #add new epoch to test
        date = epochs[idx+1]
        temp[date] = []  
        
        #start flagging epochs outside the predefined confidence interval
        for row in range(n):
            xhat1 = a[row]
            xhat2 = b[row]
            
            #Measured deformation
            y_under = data_processed[date].iloc[row]
            
            #predicted deformation
            delta_d = xhat1 * delta_days[idx+1] + xhat2
            
            #95% confidence interval
            r_alpha_2 = 1.96
            conf_int = r_alpha_2*sigma_ehat[row]
            
            if y_under + conf_int > delta_d and y_under - conf_int < delta_d:
                temp[date].append(0)
            else:
                temp[date].append(1)
                temp['SUMMED'][row] += 1
    
    print('Finished checking arc for potential flag.')
    
    return data_processed[['Arc','geometry (wgs)','point','geometry (rd)']].join(pd.DataFrame.from_dict(temp)), epochs[1:start_epoch+1]
