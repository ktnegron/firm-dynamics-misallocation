"""
Hopenhayn (1992)-style firm-dynamics model with idiosyncratic policy distortions
(Restuccia & Rogerson, 2008).

Firms differ in productivity s (AR(1) in logs). Each period a firm chooses labor n
to maximize static profit given the equilibrium price p. Firms exit endogenously
when their continuation value falls below zero. A free-entry condition pins down
the equilibrium price; labor-market clearing pins down the mass of entrants.
"""

import numpy as np
from scipy.optimize import brentq
from .core import stationary_dist


def static_choice(p, s_grid, tau, alpha, w=1.0):
    """
    Static firm decision: labor demand, profit, and output.

    The distortion tau affects revenue the firm acts on, not physical output,
    so it correctly drops out of TFP calculations.

    Parameters
    ----------
    p : float
        Output price
    s_grid : ndarray
        Productivity grid
    tau : float
        Idiosyncratic distortion (tax if >0, subsidy if <0)
    alpha : float
        Labor share of output
    w : float
        Wage (default 1.0)

    Returns
    -------
    n : ndarray
        Labor demand
    profit : ndarray
        Operating profit
    output : ndarray
        Physical output (s * n^alpha)
    """
    eff = np.maximum((1 - tau) * p * s_grid * alpha, 1e-12) / w
    n = eff ** (1 / (1 - alpha))
    revenue = (1 - tau) * p * s_grid * n ** alpha
    profit = revenue - w * n
    output = s_grid * n ** alpha
    return n, profit, output


def solve_value(p, s_grid, Q, alpha, beta, cf, tau, tol=1e-9, maxit=3000):
    """
    Value function iteration for a given distortion tau.

    Parameters
    ----------
    p : float
        Output price
    s_grid : ndarray
        Productivity grid
    Q : ndarray
        Transition matrix for log-productivity
    alpha : float
        Labor share
    beta : float
        Discount factor
    cf : float
        Per-period fixed operating cost
    tau : float
        Idiosyncratic distortion
    tol : float
        Convergence tolerance
    maxit : int
        Maximum iterations

    Returns
    -------
    V : ndarray
        Value function
    exit_policy : ndarray
        Boolean exit rule (True if exit)
    n_arr : ndarray
        Labor demand schedule
    profit_arr : ndarray
        Profit schedule
    out_arr : ndarray
        Output schedule
    """
    n_arr, profit_arr, out_arr = static_choice(p, s_grid, tau, alpha)
    V = np.zeros(len(s_grid))
    for _ in range(maxit):
        EV = Q @ np.maximum(V, 0.0)
        V_new = profit_arr - cf + beta * EV
        if np.max(np.abs(V_new - V)) < tol:
            V = V_new
            break
        V = V_new
    exit_policy = V < 0
    return V, exit_policy, n_arr, profit_arr, out_arr


def solve_equilibrium(s_grid, Q, alpha, beta, cf, ce, L_supply,
                      tau_vals, entry_weight, p_bracket=(0.05, 50.0)):
    """
    Full equilibrium solver for the base model.

    Parameters
    ----------
    s_grid : ndarray
        Productivity grid (exponentiated z_grid from Tauchen)
    Q : ndarray
        Transition matrix
    alpha : float
        Labor share
    beta : float
        Discount factor
    cf : float
        Fixed operating cost
    ce : float
        Entry cost
    L_supply : float
        Aggregate labor supply (exogenous)
    tau_vals : ndarray
        Array of distortion wedges
    entry_weight : list of ndarray
        entry_weight[k] is the distribution of entrants with distortion tau_vals[k]
    p_bracket : tuple
        Bracket for root-finding

    Returns
    -------
    results : dict
        Dictionary with keys:
        - 'p': equilibrium price
        - 'aggregate_output': aggregate output Y
        - 'aggregate_mass_firms': total mass of active firms
        - 'exit_rate': fraction of firms that exit per period
        - 'labor_demand_per_M': labor per unit of aggregate entrant mass M
        - 'types': list of dicts with per-type details
    """
    def free_entry_gap(p):
        total = 0.0
        for k, tau in enumerate(tau_vals):
            V, _, _, _, _ = solve_value(p, s_grid, Q, alpha, beta, cf, tau)
            total += np.sum(entry_weight[k] * V)
        return total - ce

    p_star = brentq(free_entry_gap, *p_bracket, xtol=1e-10)

    results = {"p": p_star, "types": []}
    labor_demand_per_M = 0.0
    output_per_M = 0.0
    mass_per_M = 0.0
    exits_per_M = 0.0

    for k, tau in enumerate(tau_vals):
        V, exit_policy, n_arr, profit_arr, out_arr = solve_value(
            p_star, s_grid, Q, alpha, beta, cf, tau)
        mu = stationary_dist(exit_policy, Q, entry_weight[k])

        labor_demand_per_M += np.sum(mu * n_arr)
        output_per_M += np.sum(mu * out_arr)
        mass_per_M += np.sum(mu)
        exits_per_M += np.sum(mu * exit_policy)

        results["types"].append(dict(tau=tau, V=V, exit_policy=exit_policy,
                                      n=n_arr, profit=profit_arr,
                                      output=out_arr, mu=mu))

    M = L_supply / labor_demand_per_M
    results["M"] = M
    results["aggregate_output"] = M * output_per_M
    results["aggregate_mass_firms"] = M * mass_per_M
    results["exit_rate"] = exits_per_M / mass_per_M
    results["labor_demand_per_M"] = labor_demand_per_M
    return results
