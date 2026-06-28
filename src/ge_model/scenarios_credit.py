"""
Policy regime definitions and scenario runner for the credit-constrained model.

Defines four regimes:
  1. Frictionless: no capital constraint
  2. Constrained: finite collateral multiplier, no policy
  3. Targeted: credit access favors top-quintile entrants
  4. Mistargeted: credit access favors bottom-quintile entrants
"""

import numpy as np
from .core import tauchen
from .model_credit import solve_equilibrium_credit


# Default calibration for credit model
CALIBRATION = {
    "N_Z": 25,
    "RHO": 0.90,
    "SIGMA": 0.20,
    "THETA_K": 0.30,
    "THETA_N": 0.35,
    "R_RATE": 0.10,
    "BETA": 0.85,
    "CF": 0.55,
    "CE": 1.10,
    "L_SUPPLY": 1.0,
    "LAMBDA_BASE": 1.5,
    "LAMBDA_BOOST": 5.0,
    "A_VALS": np.array([0.4, 0.8, 1.5, 3.0, 6.0]),
}


def create_regime_config_credit(regime, s_grid, nu, calibration):
    """
    Create k_max_vals and entry_weight for a given credit regime.

    Parameters
    ----------
    regime : str
        One of "frictionless", "constrained", "targeted", "mistargeted"
    s_grid : ndarray
        Productivity grid
    nu : ndarray
        Entry distribution (over productivity)
    calibration : dict
        Calibration parameters

    Returns
    -------
    k_max_vals : list
        Capital collateral limits for each firm type
    entry_weight : list of ndarray
        Entry distribution for each firm type
    """
    if regime == "frictionless":
        k_max_vals = [1e6]
        entry_weight = [nu.copy()]

    else:
        A_VALS = calibration["A_VALS"]
        n_a = len(A_VALS)

        if regime == "constrained":
            k_max_vals = list(calibration["LAMBDA_BASE"] * A_VALS)
            entry_weight = [(1.0 / n_a) * nu.copy() for _ in range(n_a)]

        elif regime in ("targeted", "mistargeted"):
            cdf = np.cumsum(nu)
            if regime == "targeted":
                favored_mask = cdf > 0.80
            else:
                favored_mask = cdf <= 0.20

            k_max_vals = []
            entry_weight = []
            for a in A_VALS:
                k_max_vals.append(calibration["LAMBDA_BASE"] * a)
                w_normal = np.where(~favored_mask, nu, 0.0) / n_a
                entry_weight.append(w_normal)

                k_max_vals.append(calibration["LAMBDA_BOOST"] * a)
                w_favored = np.where(favored_mask, nu, 0.0) / n_a
                entry_weight.append(w_favored)

        else:
            raise ValueError(f"Unknown regime: {regime}")

    return k_max_vals, entry_weight


def run_scenario(regime, calibration=None):
    """
    Run a credit regime scenario and return equilibrium results.

    Parameters
    ----------
    regime : str
        One of "frictionless", "constrained", "targeted", "mistargeted"
    calibration : dict, optional
        Calibration parameters. If None, uses defaults.

    Returns
    -------
    results : dict
        Equilibrium results from solve_equilibrium_credit
    """
    if calibration is None:
        calibration = CALIBRATION.copy()

    z_grid, Q = tauchen(calibration["N_Z"], calibration["RHO"], calibration["SIGMA"])
    s_grid = np.exp(z_grid)

    # Entry distribution
    entry_logits = -np.maximum(z_grid, 0) * 2.0 - 0.5 * z_grid**2
    nu = np.exp(entry_logits)
    nu = nu / nu.sum()

    k_max_vals, entry_weight = create_regime_config_credit(regime, s_grid, nu, calibration)

    results = solve_equilibrium_credit(
        s_grid, Q,
        calibration["BETA"], calibration["CF"], calibration["CE"],
        calibration["L_SUPPLY"],
        calibration["THETA_K"], calibration["THETA_N"],
        calibration["R_RATE"],
        k_max_vals, entry_weight
    )
    results["s_grid"] = s_grid
    results["regime"] = regime
    return results


# Export s_grid for use by analysis module
z_grid, _ = tauchen(CALIBRATION["N_Z"], CALIBRATION["RHO"], CALIBRATION["SIGMA"])
s_grid = np.exp(z_grid)
