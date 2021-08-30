'''
@author: Max Felius

This python file contains the functions for computing the minimal detectable deformation and the detectability power.
'''

#imports
import scipy.stats as st

#functions created by Wietske Brouwer
def dp_f(alpha, sigma, mdd):
    k = st.norm.ppf(1-alpha/2, loc=0, scale=sigma)
    dp = 1-st.norm.cdf(k, loc=mdd, scale=sigma )
    return dp

def mdd_f(alpha, sigma, dp):
    x_temp = norm.ppf(1-dp, loc = 0, scale = sigma)
    K = norm.ppf(1-alpha/2, loc=0, scale = sigma)
    mdd = K - x_temp
    return mdd

#functions received from Skygeo which contain an error
def compute_mdd(dp, std, z_crit):
    # Find the critical value of the sample distribution
    z_a = st.norm.ppf(dp, loc=0, scale=std)
    return (abs(z_a) + z_crit) * std

def compute_dp(mdd, std, z_crit):
    # Convert mdd from mm to in terms of the factor of the std
    mdd = mdd / std
    # Find the critical value of the sample distribution
    z_a = mdd - z_crit
    # Find the DP (confidence interval) of the sample
    dp = st.norm.cdf(z_a, loc=0, scale=std)
    return dp * 100
