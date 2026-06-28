"""
Policy regime definitions and scenario runner for the base model.

Defines three regimes:
  1. Efficient: no distortions
  2. Untargeted: distortions uncorrelated with productivity
  3. Mistargeted: distortions negatively correlated with productivity
"""

import numpy as np
from .core import tauchen
from .model import solve_equilibrium


# Default calibration
CALIBRATION = {
    "N_Z": 25,
    "RHO": 0.90,
    "SIGMA": 0.20,
    "ALPHA": 0.65,
    "BETA": 0.85,
    "CF": 0.55,
    "CE": 1.10,
    "L_SUPPLY": 1.0,
    "TAU_VALS": np.array([-0.30, -0.15, 0.0, 0.15, 0.30]),
}


def create_regime_config(regime, s_grid, nu):
    """
    Create tau_vals and entry_weight for a given regime.

    Parameters
    ----------
    regime : str
        One of "efficient", "untargeted", "mistargeted"
    s_grid : ndarray
        Productivity grid
    nu : ndarray
        Entry distribution (over productivity)

    Returns
    -------
    tau_vals : ndarray
        Array of distortion wedges
    entry_weight : list of ndarray
        Entry distribution for each tau type
    """
    if regime == "efficient":
        tau_vals = np.array([0.0])
        entry_weight = [nu.copy()]

    elif regime == "untargeted":
        tau_vals = CALIBRATION["TAU_VALS"].copy()
        entry_weight = [0.2 * nu.copy() for _ in tau_vals]

    elif regime == "mistargeted":
        tau_vals = CALIBRATION["TAU_VALS"].copy()
        cdf = np.cumsum(nu)
        bin_idx = np.searchsorted(np.linspace(0, 1, 6)[1:-1], cdf)
        entry_weight = []
        for k in range(len(tau_vals)):
            w = np.where(bin_idx == k, nu, 0.0)
            entry_weight.append(w)
    else:
        raise ValueError(f"Unknown regime: {regime}")

    return tau_vals, entry_weight


def run_scenario(regime, calibration=None):
    """
    Run a scenario and return equilibrium results.

    Parameters
    ----------
    regime : str
        One of "efficient", "untargeted", "mistargeted"
    calibration : dict, optional
        Calibration parameters. If None, uses defaults.

    Returns
    -------
    results : dict
        Equilibrium results from solve_equilibrium
    """
    if calibration is None:
        calibration = CALIBRATION.copy()

    z_grid, Q = tauchen(calibration["N_Z"], calibration["RHO"], calibration["SIGMA"])
    s_grid = np.exp(z_grid)

    # Entry distribution: lower half of productivity grid
    entry_logits = -np.maximum(z_grid, 0) * 2.0 - 0.5 * z_grid**2
    nu = np.exp(entry_logits)
    nu = nu / nu.sum()

    tau_vals, entry_weight = create_regime_config(regime, s_grid, nu)

    results = solve_equilibrium(
        s_grid, Q,
        calibration["ALPHA"], calibration["BETA"],
        calibration["CF"], calibration["CE"],
        calibration["L_SUPPLY"],
        tau_vals, entry_weight
    )
    results["s_grid"] = s_grid
    results["regime"] = regime
    return results


# Export s_grid for use by analysis module (computed with default calibration)
z_grid, _ = tauchen(CALIBRATION["N_Z"], CALIBRATION["RHO"], CALIBRATION["SIGMA"])
s_grid = np.exp(z_grid)
