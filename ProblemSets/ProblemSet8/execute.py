import numpy as np
import scipy.optimize as opt
from math import exp
import random
import matplotlib.pyplot as plt
from functions import recursion

# Set parameter values
A = 3.0
B = 1.0
epsilon = 0.4
T = 10
init_state = 1
pi = np.array([[0.1, 0.9],[0.4,0.6]])

# Store optimal prices and corresponding value functions 
Opt_prices, value_D, value_U = recursion(A, B, epsilon, pi, T, init_state)

time = list(range(1,11))

# Plot the optimal prices - note that the optimal price list needs to be reversed while plotting
plt.figure()
plt.scatter(time[0:], Opt_prices[::-1])
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Optimal prices for the finite horizon dynamic programming problem')
plt.savefig('Prices.png')

# Plot the value functions - note that both value functions need to be reversed while plotting
plt.figure()
fig, ax = plt.subplots()
ax.scatter(time[0:], value_D[::-1], label = "Down state")
ax.scatter(time[0:], value_U[::-1], label = "Up state")
legend = ax.legend(loc = "upper left", shadow = False)
plt.ylim([1e-127,1e-121])
plt.xlabel('Time')
plt.ylabel('Value function')
plt.title('Value functions for the finite horizon dynamic programming problem')
plt.savefig('VFs.png')