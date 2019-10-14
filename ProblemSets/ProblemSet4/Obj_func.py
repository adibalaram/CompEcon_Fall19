from geopy.distance import vincenty
import numpy as np

def obj_func_no_price(Beta, *comp_data):
    '''
    Compute the objective function for the maximum score estimator.
    This model doesn't account for price.
    
    Args:
    comp_data: The entire dataset that is to be used
    Beta: A length 2 tuple that contains the parameters to be estimated
    
    Returns:
    ms_obj_fun: Negative of the value of the objective function for the maximum score estimator.
                We return the negative since we use a minimization routine
                This is a function of the parameters alpha and beta
    '''

    alpha, beta = Beta
    
    # Start by creating the f(b,t) matrices
    # I populate the matrices with zeros since pre-allocating memory usually results
    # in faster running times (at least in MATLAB and is necessary in Java)
    
    comp_data_07 = comp_data[0]
    f_07 = np.zeros((comp_data_07.shape[0],comp_data_07.shape[0]))
    
    comp_data_08 = comp_data[1]
    f_08 = np.zeros((comp_data_08.shape[0],comp_data_08.shape[0]))
    
    # Each of the loops below is used to actually populate the value of a merger for each
    # buyer-target pair. Entry (i,j) in either matrix corresponds to the value of the 
    # merger between i and j in a particular market (year)
    # Geographical distances are computed for each pair

    for i in range(comp_data_07.shape[0]):
        for j in range(comp_data_07.shape[0]):
            dist = vincenty((comp_data_07.loc[i,'buyer_lat'],comp_data_07.loc[i,'buyer_long']),
                                (comp_data_07.loc[j,'target_lat'],comp_data_07.loc[j,'target_long'])).miles
            f_07[i,j] = ((comp_data_07.loc[i,'num_stations_buyer'] * comp_data_07.loc[j,'population_target_mil'])
                         + (alpha * comp_data_07.loc[i,'corp_owner_buyer'] * 
                            comp_data_07.loc[j,'population_target_mil']) + (beta * dist))
    
    for i in range(comp_data_08.shape[0]):
        for j in range(comp_data_08.shape[0]):
            dist = vincenty((comp_data_08.iloc[0,3], comp_data_08.iloc[0,4]),
                                (comp_data_08.iloc[0,5], comp_data_08.iloc[0,6])).miles
            f_08[i,j] = ((comp_data_08.iloc[i,9] * comp_data_08.iloc[j,13])
                         + (alpha * comp_data_08.iloc[i,11] * 
                            comp_data_08.iloc[j,13]) + (beta * dist))

    
    # I now compute the objective function (as a function of the parameters)
    # Start by computing the sum of the indicator functions by year
    
    obj_func_07 = 0
    for i in range(f_07.shape[0] - 1):
        for j in range(i + 1, f_07.shape[0]):
            actual = f_07[i,i] + f_07[j,j]  # This is the value of two actual mergers
            counterfactual = f_07[i,j] + f_07[j,i]  # This is the value of the counterfactuals
            if(actual >= counterfactual):   # This statement is essentially the indicator function
                obj_func_07 += 1
    
    
    # The segment below does the same thing but for the year 2008

    obj_func_08 = 0
    for i in range(f_08.shape[0] - 1):
        for j in range(i + 1, f_08.shape[0]):
            actual = f_08[i,i] + f_08[j,j]
            counterfactual = f_08[i,j] + f_08[j,i]
            if(actual >= counterfactual):
                obj_func_08 += 1
                
    ms_obj_func = obj_func_07 + obj_func_08
    return -ms_obj_func

def obj_func_with_price(Beta, *comp_data):
    '''
    Compute the objective function for the maximum score estimator.
    This model does account for price.
    
    Args:
    comp_data: The entire dataset that is to be used
    Beta: A length 4 tuple that contains the parameters to be estimated
    
    Returns:
    ms_obj_fun: Negative of the value of the objective function for the maximum score estimator.
                We return the negative since we use a minimization routine
                This is a function of the parameters alpha and beta
    '''
    
    delta, alpha, gamma, beta = Beta
    
    # Start by creating the f(b,t) matrices
    # I include the additional target level characteristic (market concentration)
    
    comp_data_07 = comp_data[0]
    f_07 = np.zeros((comp_data_07.shape[0],comp_data_07.shape[0]))
    
    comp_data_08 = comp_data[1]
    f_08 = np.zeros((comp_data_08.shape[0],comp_data_08.shape[0]))
    
    for i in range(comp_data_07.shape[0]):
        for j in range(comp_data_07.shape[0]):
            dist = vincenty((comp_data_07.loc[i,'buyer_lat'],comp_data_07.loc[i,'buyer_long']),
                                (comp_data_07.loc[j,'target_lat'],comp_data_07.loc[j,'target_long'])).miles
            f_07[i,j] = ((delta * comp_data_07.loc[i,'num_stations_buyer'] * comp_data_07.loc[j,'population_target_mil'])
                         + (alpha * comp_data_07.loc[i,'corp_owner_buyer'] * 
                            comp_data_07.loc[j,'population_target_mil']) + 
                         (gamma * comp_data_07.loc[j,'hhi_target']) + (beta * dist))
    
    for i in range(comp_data_08.shape[0]):
        for j in range(comp_data_08.shape[0]):
            dist = vincenty((comp_data_08.iloc[0,3], comp_data_08.iloc[0,4]),
                                (comp_data_08.iloc[0,5], comp_data_08.iloc[0,6])).miles
            f_08[i,j] = ((delta * comp_data_08.iloc[i,9] * comp_data_08.iloc[j,13])
                         + (alpha * comp_data_08.iloc[i,11] * 
                            comp_data_08.iloc[j,13]) + (gamma * comp_data_08.iloc[j,8]) + 
                         (beta * dist))

    
    # I now compute the objective function
    
    # Start by computing the sum of the indicator functions by year
    
    obj_func_07 = 0
    for i in range(f_07.shape[0] - 1):
        for j in range(i + 1, f_07.shape[0]):
            LHS_1 = f_07[i,i] - f_07[i,j]   # This term is the LHS of the first condition to be evaluated in the indicator function
            RHS_1 = comp_data_07.loc[i,'price_mil'] - comp_data_07.loc[j,'price_mil'] # This term is the RHS of the first condition
            # to be evaluated in the indicator function
            LHS_2 = f_07[j,j] - f_07[j,i]   # This term is the LHS of the second condition to be evaluated in the indicator function
            RHS_2 = comp_data_07.loc[j,'price_mil'] - comp_data_07.loc[i,'price_mil']# This term is the RHS of the second condition
            # to be evaluated in the indicator function
            if((LHS_1 >= RHS_1) & (LHS_2 >= RHS_2)):    # In this model I ensure that both conditions are satisfied
                obj_func_07 += 1
    
    
    
    obj_func_08 = 0
    for i in range(f_08.shape[0] - 1):
        for j in range(i + 1, f_08.shape[0]):
            LHS_1 = f_08[i,i] - f_08[i,j]
            RHS_1 = comp_data_08.iloc[i,12] - comp_data_08.iloc[j,12]
            LHS_2 = f_08[j,j] - f_08[j,i]
            RHS_2 = comp_data_08.iloc[j,12] - comp_data_08.iloc[i,12]
            if((LHS_1 >= RHS_1) & (LHS_2 >= RHS_2)):
                obj_func_08 += 1
                
    ms_obj_func = obj_func_07 + obj_func_08
    return -ms_obj_func