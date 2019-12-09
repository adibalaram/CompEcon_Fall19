import numpy as np
import scipy.optimize as opt
import households as hh
import firm
def solve_tp(r_path_init, params):
    '''
    Solves for the time path equilibrium using TPI
    '''
    beta, sigma, n, alpha, A, delta, T, xi, b_pre, r_ss = params
    tpi_dist = 7.0
    tpi_tol = 1e-8
    tpi_iter = 0
    tpi_max_iter = 300
    r_path = np.append(r_path_init, np.ones(2) * r_ss)
    while (tpi_dist > tpi_tol) & (tpi_iter < tpi_max_iter):
        w_path = firm.get_w(r_path, alpha, A, delta)
        # Solve HH problem
        # Solve upper right corner
        b_sp1_mat = np.zeros((T + 2, 2))
        foc_args = (beta, sigma, r_path[:2], w_path[:2], n[-2:], b_pre[0])
        b_sp1_guess = [0.05]
        result = opt.root(hh.FOCs, b_sp1_guess, args=foc_args)
        b_sp1_mat[0, -1] = result.x

        # Solve all full lifetimes
        DiagMaskb = np.eye(2, dtype = bool)
        for t in range (1, T):
            foc_args = (beta, sigma, r_path[t:t+2], w_path[t:t+2], n, b_pre[0])
            b_sp1_guess = [0.05, 0.05]
            result = opt.root(hh.FOCs, b_sp1_guess, args=foc_args)
            b_sp1_mat[t:t+2, :] = DiagMaskb * result.x + b_sp1_mat[t:t+2, :]
        # Use market clearing to find aggregates
        L_path = np.ones(T) * agg.get_L(n)
        K_path = agg.get_K(b_sp1_mat)
        # find implied r
        r_path_prime = firm.get_r(L_path, K_path, alpha, A, delta)
        # check distance
        tpi_dist = np.absolute(r_path[:T] - r_path_prime[:T]).max()
        print('Iteration = ', tpi_iter, ', Distance = ', tpi_dist,
              ', r = ', r)
        # update r
        r = xi * r_prime + (1 - xi) * r
        # update iteration counter
        ss_iter += 1

