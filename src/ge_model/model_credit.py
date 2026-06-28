"""
Credit-constrained firm dynamics model (Buera, Kaboski & Shin, 2011 style).

Extends the base model with capital as a second input and a collateral constraint:
k <= lambda * a, where a is net worth. This creates a genuine friction: talented
firms may be stuck below efficient scale if poor, enabling targeted policy to help.
"""

import numpy as np
from scipy.optimize import brentq
from .core import stationary_dist


def static_choice_credit(p, s_grid, k_max, theta_k, theta_n, r, w=1.0):
    """
    Static choice with capital and labor inputs, collateral constraint.

    Solves two-input Cobb-Douglas problem; if unconstrained capital exceeds k_max,
    re-solves labor given k pinned at k_max.

    Parameters
    ----------
    p : float
        Output price
    s_grid : ndarray
        Productivity grid
    k_max : float
        Capital collateral limit (= lambda * a)
    theta_k : float
        Capital share
    theta_n : float
        Labor share
    r : float
        Capital rental rate (interest + depreciation)
    w : float
        Wage

    Returns
    -------
    k : ndarray
        Capital choice
    n : ndarray
        Labor choice
    profit : ndarray
        Operating profit
    output : ndarray
        Output (s * k^theta_k * n^theta_n)
    constrained : ndarray
        Boolean; True if firm hits capital constraint
    """
    nu_rts = theta_k + theta_n  # returns to scale

    gamma = (r * theta_n) / (w * theta_k)  # unconstrained k/n ratio
    base = np.maximum(p * s_grid * theta_k * gamma ** theta_n, 1e-12) / r
    k_u = base ** (1.0 / (1.0 - nu_rts))
    n_u = k_u * gamma

    constrained = k_u > k_max
    k = np.where(constrained, k_max, k_u)

    # If constrained, re-solve labor given k = k_max
    n_c = np.maximum(p * s_grid * theta_n * np.maximum(k, 1e-12) ** theta_k / w,
                      1e-12) ** (1.0 / (1.0 - theta_n))
    n = np.where(constrained, n_c, n_u)

    output = s_grid * np.maximum(k, 1e-12) ** theta_k * np.maximum(n, 1e-12) ** theta_n
    revenue = p * output
    profit = revenue - r * k - w * n
    return k, n, profit, output, constrained


def solve_value_credit(p, s_grid, Q, beta, cf, k_max, theta_k, theta_n, r,
                       w=1.0, tol=1e-9, maxit=3000):
    """
    Value function iteration for credit-constrained firm.

    Parameters
    ----------
    p : float
        Output price
    s_grid : ndarray
        Productivity grid
    Q : ndarray
        Transition matrix
    beta : float
        Discount factor
    cf : float
        Fixed operating cost
    k_max : float
        Capital collateral limit
    theta_k : float
        Capital share
    theta_n : float
        Labor share
    r : float
        Capital rental rate
    w : float
        Wage
    tol : float
        Convergence tolerance
    maxit : int
        Maximum iterations

    Returns
    -------
    V : ndarray
        Value function
    exit_policy : ndarray
        Exit rule
    k_arr : ndarray
        Capital schedule
    n_arr : ndarray
        Labor schedule
    profit_arr : ndarray
        Profit schedule
    out_arr : ndarray
        Output schedule
    constrained : ndarray
        Constraint indicator
    """
    k_arr, n_arr, profit_arr, out_arr, constrained = static_choice_credit(
        p, s_grid, k_max, theta_k, theta_n, r, w)
    V = np.zeros(len(s_grid))
    for _ in range(maxit):
        EV = Q @ np.maximum(V, 0.0)
        V_new = profit_arr - cf + beta * EV
        if np.max(np.abs(V_new - V)) < tol:
            V = V_new
            break
        V = V_new
    exit_policy = V < 0
    return V, exit_policy, k_arr, n_arr, profit_arr, out_arr, constrained


def solve_equilibrium_credit(s_grid, Q, beta, cf, ce, L_supply,
                             theta_k, theta_n, r, k_max_vals, entry_weight,
                             p_bracket=(0.05, 80.0)):
    """
    Full equilibrium solver for credit-constrained model.

    Parameters
    ----------
    s_grid : ndarray
        Productivity grid
    Q : ndarray
        Transition matrix
    beta : float
        Discount factor
    cf : float
        Fixed operating cost
    ce : float
        Entry cost
    L_supply : float
        Aggregate labor supply
    theta_k : float
        Capital share
    theta_n : float
        Labor share
    r : float
        Capital rental rate
    k_max_vals : list or ndarray
        Capital limits for each firm type
    entry_weight : list of ndarray
        Entry distribution for each firm type
    p_bracket : tuple
        Bracket for root-finding

    Returns
    -------
    results : dict
        Dictionary with keys:
        - 'p': equilibrium price
        - 'aggregate_output': aggregate output Y
        - 'aggregate_mass_firms': total mass of active firms
        - 'exit_rate': exit rate
        - 'constrained_share': fraction of firms at capital limit
        - 'types': list of dicts with per-type details
    """
    def free_entry_gap(p):
        total = 0.0
        for k, k_max in enumerate(k_max_vals):
            V, *_ = solve_value_credit(p, s_grid, Q, beta, cf, k_max,
                                        theta_k, theta_n, r)
            total += np.sum(entry_weight[k] * V)
        return total - ce

    p_star = brentq(free_entry_gap, *p_bracket, xtol=1e-10)

    results = {"p": p_star, "types": []}
    labor_demand_per_M = 0.0
    output_per_M = 0.0
    mass_per_M = 0.0
    exits_per_M = 0.0
    constrained_mass_per_M = 0.0

    for k, k_max in enumerate(k_max_vals):
        V, exit_policy, k_arr, n_arr, profit_arr, out_arr, constrained = \
            solve_value_credit(p_star, s_grid, Q, beta, cf, k_max,
                                theta_k, theta_n, r)
        mu = stationary_dist(exit_policy, Q, entry_weight[k])

        labor_demand_per_M += np.sum(mu * n_arr)
        output_per_M += np.sum(mu * out_arr)
        mass_per_M += np.sum(mu)
        exits_per_M += np.sum(mu * exit_policy)
        constrained_mass_per_M += np.sum(mu * constrained)

        results["types"].append(dict(k_max=k_max, V=V, exit_policy=exit_policy,
                                      k=k_arr, n=n_arr, profit=profit_arr,
                                      output=out_arr, mu=mu, constrained=constrained))

    M = L_supply / labor_demand_per_M
    results["M"] = M
    results["aggregate_output"] = M * output_per_M
    results["aggregate_mass_firms"] = M * mass_per_M
    results["exit_rate"] = exits_per_M / mass_per_M
    results["constrained_share"] = constrained_mass_per_M / mass_per_M
    return results
