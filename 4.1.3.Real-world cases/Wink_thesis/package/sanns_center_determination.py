'''
@author: Max Felius

Script to determine the center of the subsidence trough
'''
# from package.inverse_kinematic_model import inverse_kinematic_model
from package.sanns_inverse_lsq import inverse_kinematic_model
import numpy as np
from package.geometric_models import sann as zg
from tqdm import tqdm

def center_determination(t,x,y,x0_array,data_list,delta_days,nitems,v_in,R_in,verbose='on'):
    '''
    Function to determine the center of the sinkhole based on the RMSE
    '''
    # v_in = 1
    # R_in = np.max(x)/2

    RMSE_out = []

    if verbose.lower() == 'off':
        for x0 in x0_array:
            r = np.sqrt((x-x0)**2)

            try:
                gv, gR = inverse_kinematic_model(v_in,t,R_in,r,y,verbose='off')
            except:
                gv = 0
                gR = 1

        #     fit_list = np.zeros((3,nitems))
            RMSE_list = np.zeros((1,nitems))

            for i in range(nitems):
                #compute some parameters
                y_data = data_list[i][1].values/100 #from cm to meter
                x1 = data_list[i][0].values
                r1 = np.sqrt((x1-x0)**2)

                #computing the gaussian model and fit
                y1 = gv*delta_days[i]*zg(gR,r1)
                ehat = y_data - y1
                gfit = 100*(1-(np.sum(abs(ehat))/np.sum(abs(y_data))))
    #             fit_list[0,i] = gfit
                gaus_RMSE = np.sqrt((ehat @ ehat.T)/len(ehat))*1000
                RMSE_list[0,i] = gaus_RMSE

            avg_gRMSE = np.sum(RMSE_list[0,:])/(nitems)

            RMSE_out.append(avg_gRMSE)

    elif verbose.lower() == 'on':
        for x0 in tqdm(x0_array,'Determining Center Position'):
            r = np.sqrt((x-x0)**2)

            try:
                gv, gR = inverse_kinematic_model(v_in,t,R_in,r,y,verbose='off')
            except:
                gv = 0
                gR = 1

        #     fit_list = np.zeros((3,nitems))
            RMSE_list = np.zeros((1,nitems))

            for i in range(nitems):
                #compute some parameters
                y_data = data_list[i][1].values/100 #from cm to meter
                x1 = data_list[i][0].values
                r1 = np.sqrt((x1-x0)**2)

                #computing the gaussian model and fit
                y1 = gv*delta_days[i]*zg(gR,r1)
                ehat = y_data - y1
                gfit = 100*(1-(np.sum(abs(ehat))/np.sum(abs(y_data))))
    #             fit_list[0,i] = gfit
                gaus_RMSE = np.sqrt((ehat @ ehat.T)/len(ehat))*1000
                RMSE_list[0,i] = gaus_RMSE

            avg_gRMSE = np.sum(RMSE_list[0,:])/(nitems)

            RMSE_out.append(avg_gRMSE)
    else:
        print(f'{verbose} input unknown.')

    return np.array(RMSE_out)
