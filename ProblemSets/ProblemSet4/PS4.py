'''
Solution for Problem Set 4
This script reads in the data and computes the maximum score estimator for two models
The first model doesn't include price
The second includes price and a target level characteristic
'''

# Import necessary packages
import pandas as pd
import numpy as np
import scipy.optimize as opt
from scipy.optimize import differential_evolution

# Read in data and convert price and population variables to millions
ACH_data = pd.read_excel('radio_merger_data.xlsx',header = 0)
ACH_data['price_mil'] = ACH_data['price']/1000000
ACH_data['population_target_mil'] = ACH_data['population_target']/1000000
ACH_data.describe()

# Split data by year - this makes it easier to compute the score function by year and then
# sum across years. I also had some difficulty passing the data as is to the differential evolution
# routine. It works fine if I pass yearly data as a tuple.
temp07 = ACH_data[ACH_data['year'] == 2007]
temp08 = ACH_data[ACH_data['year'] == 2008]

# Call the differential evolution optimizer on the objective function
# First, this is done on the objective function without price

from Obj_func import obj_func_no_price

# I tried many different bounds on the parameters and these bounds provided the best results

bnds = [(0, 4000), (-10, 10)]
args = (temp07, temp08)
obj_min = 1e+100

# I run the optimization routine three times to see if the stochastic nature of differential evolution
# leads to different results. This wasn't the case when I tried it earlier.

for i in range(3):
    max_score = differential_evolution(obj_func_no_price, bnds, args = args, tol = 1e-15)
    print('Iteration ', i + 1, ' is complete')  # This is just a check to see how many iterations have been completed
    if(max_score['fun'] < obj_min):
        obj_min = max_score['fun']
        alpha_min = max_score['x'][0]
        beta_min = max_score['x'][1]

print('Estimates for the model without price')

print("Minimum function value = ", obj_min)
print("Optimum alpha = ", alpha_min)
print("Optimum beta = ", beta_min) 

# Then, estimate the second model that accounts for price
# This segment takes a long time to run (about 40 minutes) so I do not run the optimization routine multiple times

from Obj_func import obj_func_with_price

bnds = [(-1e+9,1e+9), (-1e+9,1e+9), (-1e+9,1e+9), (-1e+9,1e+9)]
args = (temp07, temp08)
DE_result = differential_evolution(obj_func_with_price, bnds, args = args, tol = 1e-15)

print('Estimates for the model with price')

print("Minimum function value = ", DE_result['fun'])
print("Optimum delta = ", DE_result['x'][0])
print("Optimum alpha = ", DE_result['x'][1])
print("Optimum gamma = ", DE_result['x'][2]) 
print("Optimum beta = ", DE_result['x'][3]) 