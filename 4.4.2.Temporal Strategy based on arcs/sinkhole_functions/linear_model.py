'''
@author: Max Felius

'''

#import 
import numpy as np
import datetime

class linear_model:
    def __init__(self):
        pass

    def get_delta_day(self,epochs):
        dates = list(map(lambda x: datetime.datetime.strptime(x,'d_%Y%m%d'),epochs))
        start_date = dates[0]
        dates_days = np.array(list(map(lambda x: (x-start_date).days,dates)))

        return dates_days, start_date

    def linear_model(self,epochs,data):
        '''
        Function creating the linear model for detect arcs behaving anomalous
        '''
        
        #creating time vector
        delta_days, start_day = self.get_delta_day(epochs)
        
        #pre-allocate space for the output variables
        a = []
        b = []
        sigma_ehat = []
        
        for i in range(len(data)):
            '''
            Loop creating a linear model per row
            '''
            
            #setting up the system of equations
            y = np.array(data[epochs].iloc[i])
            A = np.array((delta_days,np.ones([len(delta_days)])))
            
            #stochastic matrix
            W = np.eye((len(y)))
            
            #compute solutions
            invW = np.linalg.inv(W)
            Qxhat = np.linalg.inv(A @ invW @ A.T)
            xhat = Qxhat @ A @ invW @ y
            
            yhat = A.T @ xhat
            ehat = y - yhat
            
            #compute the standard deviation of the noise of an arc
            sigma_ehat_out = np.sqrt((np.sum((ehat - np.mean(ehat))**2))/len(y))
            
            #saving the data
            a.append(xhat[0])
            b.append(xhat[1])
            sigma_ehat.append(sigma_ehat_out)
        
        return a, b, sigma_ehat

    def linear_model_epochs_selected(self,epochs_list,data):
        '''
        Function creating the linear model for detect arcs behaving anomalous
        
        This particular function uses a specific set of epochs per observation.
        '''
        #pre-allocate space for the output variables
        a = []
        b = []
        sigma_ehat = []
        
        for i in range(len(data)):
            '''
            Loop creating a linear model per row
            '''
            epochs = epochs_list[i,:]

            #creating time vector
            delta_days, start_day = self.get_delta_day(epochs)

            #setting up the system of equations
            y = np.array(data[epochs].iloc[i])
            A = np.array((delta_days,np.ones([len(delta_days)])))
            
            #stochastic matrix
            W = np.eye((len(y)))
            
            #compute solutions
            invW = np.linalg.inv(W)
            Qxhat = np.linalg.inv(A @ invW @ A.T)
            xhat = Qxhat @ A @ invW @ y
            
            yhat = A.T @ xhat
            ehat = y - yhat
            
            #compute the standard deviation of the noise of an arc
            sigma_ehat_out = np.sqrt((np.sum((ehat - np.mean(ehat))**2))/len(y))
            
            #saving the data
            a.append(xhat[0])
            b.append(xhat[1])
            sigma_ehat.append(sigma_ehat_out)
        
        return a, b, sigma_ehat
