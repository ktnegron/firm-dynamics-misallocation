"""
Shared utilities for firm-dynamics general equilibrium models.

Includes Tauchen discretization, stationary distribution computation,
and shared numerical routines.
"""

import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq


def tauchen(n, rho, sigma, m=3.0):
    """
    Discretize AR(1) process z' = rho*z + eps, eps ~ N(0, sigma^2).

    Parameters
    ----------
    n : int
        Number of grid points
    rho : float
        Persistence parameter
    sigma : float
        Standard deviation of innovation
    m : float
        Grid span (in std devs of stationary distribution)

    Returns
    -------
    z_grid : ndarray, shape (n,)
        Grid points
    Q : ndarray, shape (n, n)
        Transition matrix Q[i, j] = Pr(z_t+1 = z_j | z_t = z_i)
    """
    sd_z = sigma / np.sqrt(1 - rho ** 2)
    z_max = m * sd_z
    z_min = -z_max
    z_grid = np.linspace(z_min, z_max, n)
    step = (z_max - z_min) / (n - 1)

    Q = np.zeros((n, n))
    for i in range(n):
        mu = rho * z_grid[i]
        for j in range(n):
            if j == 0:
                Q[i, j] = norm.cdf((z_grid[0] - mu + step / 2) / sigma)
            elif j == n - 1:
                Q[i, j] = 1 - norm.cdf((z_grid[-1] - mu - step / 2) / sigma)
            else:
                Q[i, j] = (norm.cdf((z_grid[j] - mu + step / 2) / sigma)
                           - norm.cdf((z_grid[j] - mu - step / 2) / sigma))
    Q = Q / Q.sum(axis=1, keepdims=True)  # numerical safety
    return z_grid, Q


def stationary_dist(exit_policy, Q, entry_dist, tol=1e-12, maxit=20000):
    """
    Compute stationary firm distribution.

    Parameters
    ----------
    exit_policy : ndarray, shape (n_s,)
        Boolean array; True if firm exits
    Q : ndarray, shape (n_s, n_s)
        Transition matrix for productivity
    entry_dist : ndarray, shape (n_s,)
        Mass of entrants at each productivity level
    tol : float
        Convergence tolerance
    maxit : int
        Maximum iterations

    Returns
    -------
    mu : ndarray, shape (n_s,)
        Stationary distribution of active firms
    """
    stay = (~exit_policy).astype(float)
    mu = entry_dist.copy()
    for _ in range(maxit):
        mu_new = Q.T @ (stay * mu) + entry_dist
        if np.max(np.abs(mu_new - mu)) < tol:
            mu = mu_new
            break
        mu = mu_new
    return mu
