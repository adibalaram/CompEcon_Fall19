# This script contains all the files needed to solve the dynamic program
import numpy as np
import scipy.optimize as opt
from math import exp
import random
import matplotlib.pyplot as plt


def prob(p, A, B, epsilon):
    '''
    Computes the probability of sale
    
    Agrs:
    p - price at which the probability is computed
    A, B - parameters of the logistic function
    epsilon - parameter that depends on the state of the system (x)
    
    Returns:
    Probability of sale for a given p, x
    '''
    q = (exp(A - B * p) / (1 + exp(A - B *p))) * epsilon
    return q

def prob_der(p, A, B, epsilon):
    '''
    Computes the derivative of the probability of sale
    
    Agrs: 
    p - price at which the derivative is computed
    A, B - parameters of the logistic function
    epsilon - parameter that depends on the state of the system (x)
    
    Returns:
    Probability of sale for a given p, x
    '''
    
    del_prob = -((B * exp(A - B * p)) / ((1 + exp(A - B *p) ** 2))) * epsilon
    return del_prob

def boundary_con(p, A, B, epsilon):
    '''
    Returns the boundary condition
    '''
    
    bound_con = prob(p, A, B, epsilon) + p * prob_der(p, A, B, epsilon)
    return bound_con

def FOC(p, A, B, epsilon, piD, piU, val_D, val_U):
    '''
    Returns the first order condition
    
    Also pass the relevant row of the transition probability matrix (pi)
    and the value computed for both states from the future period
    '''
    
    FOC_comp = prob(p, A, B, epsilon) + (p * prob_der(p, A, B, epsilon)) 
    - (prob_der(p, A, B, epsilon) * ((piD * val_D) + (piU * val_U)))
    
    return FOC_comp

def recursion(A, B, epsilon, pi, T, init_state):
    '''
    Computes the optimum price and value functions for each time period
    '''
    
    price_list = []
    value_func_U = []
    value_func_D = []
    pi_0 = pi[0]
    pi_1 = pi[1]
    curr_state = init_state
    random.seed(100)
    
    # Find optimal price for the last time period
    init_p = opt.root(boundary_con, 0, args = (A, B, epsilon))
    p = init_p.x[0]
    price_list.append(p)

    # Find value functions for the last time period
    val_D = p * (exp(A - B * p) / (1 + exp(A - B *p))) * epsilon
    val_U = p * (exp(A - B * p) / (1 + exp(A - B *p))) * (1 - epsilon)
    value_func_D.append(val_D)
    value_func_U.append(val_U)
    
    for i in range(T-1):
        rand = random.random()
        if(curr_state == 0):
            # Use appropriate row of transition probability matrix
            piD = pi_0[0]
            piU = pi_0[1]

            # Compute optimal price for period i
            root_result = opt.root(FOC, p, args = (A, B, epsilon, piD, piU, val_D, val_U))
            p = root_result.x[0]
            
            # Compute value functions for period i
            val_D = (p * (exp(A - B * p) / (1 + exp(A - B *p))) * epsilon) 
            + ((1 - (exp(A - B * p) / (1 + exp(A - B * p)))) * epsilon) * ((piD * val_D) + (piU * val_U))
            
            val_U = (p * (exp(A - B * p) / (1 + exp(A - B *p))) * (1 - epsilon)) 
            + ((1 - (exp(A - B * p) / (1 + exp(A - B *p))) * (1 - epsilon)) * ((piD * val_D) + (piU * val_U)))
            
            # generate next state
            if (rand <= piD):
                curr_state = 0
            else:
                curr_state = 1
        
        if(curr_state == 1):
            piD = pi_1[0]
            piU = pi_1[1]
            # Compute optimal price for period i
            root_result = opt.root(FOC, p, args = (A, B, epsilon, piD, piU, val_D, val_U))
            p = root_result.x[0]

            # Compute value functions for period i
            val_D = (p * (exp(A - B * p) / (1 + exp(A - B *p))) * epsilon) 
            + ((1 - (exp(A - B * p) / (1 + exp(A - B *p)))) * epsilon * ((piD * val_D) + (piU * val_U)))
            
            val_U = (p * (exp(A - B * p) / (1 + exp(A - B *p))) * (1 - epsilon)) 
            + ((1 - (exp(A - B * p) / (1 + exp(A - B *p)))) * (1 - epsilon) * ((piD * val_D) + (piU * val_U)))
            
            # generate next state
            if (rand <= piD):
                curr_state = 0
            else:
                curr_state = 1
        value_func_D.append(val_D)
        value_func_U.append(val_U)
        price_list.append(p)
        
    return price_list, value_func_D, value_func_U
        

