"""
GE Modelling package: Firm dynamics and misallocation from policy distortions.

Main modules:
  - core: Shared utilities (Tauchen, stationary distribution)
  - model: Base Hopenhayn model
  - model_credit: Credit-constrained extension
  - scenarios: Regime definitions for base model
  - scenarios_credit: Regime definitions for credit model
  - plotting: Visualization functions
"""

from .core import tauchen, stationary_dist
from .model import static_choice, solve_value, solve_equilibrium
from .model_credit import static_choice_credit, solve_value_credit, solve_equilibrium_credit
from .scenarios import run_scenario as run_base_scenario, CALIBRATION, s_grid
from .scenarios_credit import run_scenario as run_credit_scenario, CALIBRATION as CALIBRATION_CREDIT, s_grid as s_grid_credit
from .plotting import (
    employment_by_decile,
    plot_base_output_loss,
    plot_base_employment_reallocation,
    plot_credit_output,
    plot_credit_constrained_share,
)

__all__ = [
    "tauchen",
    "stationary_dist",
    "static_choice",
    "solve_value",
    "solve_equilibrium",
    "static_choice_credit",
    "solve_value_credit",
    "solve_equilibrium_credit",
    "run_base_scenario",
    "run_credit_scenario",
    "CALIBRATION",
    "CALIBRATION_CREDIT",
    "s_grid",
    "s_grid_credit",
    "employment_by_decile",
    "plot_base_output_loss",
    "plot_base_employment_reallocation",
    "plot_credit_output",
    "plot_credit_constrained_share",
]
