"""
Visualization functions for GE model results.
"""

import numpy as np
import matplotlib.pyplot as plt


def employment_by_decile(results, s_grid, n_bins=10):
    """
    Compute employment share by firm productivity decile.

    Parameters
    ----------
    results : dict
        Equilibrium results with 'types', 'M' keys
    s_grid : ndarray
        Productivity grid
    n_bins : int
        Number of bins (default 10 for deciles)

    Returns
    -------
    emp_by_bin : ndarray
        Employment share by bin (as percentage, sums to 100)
    """
    emp = np.zeros(len(s_grid))
    mass = np.zeros(len(s_grid))
    for t in results["types"]:
        emp += results["M"] * t["mu"] * t["n"]
        mass += results["M"] * t["mu"]

    order = np.argsort(s_grid)
    s_sorted = s_grid[order]
    emp_sorted = emp[order]
    mass_sorted = mass[order]

    cum_mass = np.cumsum(mass_sorted)
    total_mass = cum_mass[-1]
    bin_edges = np.linspace(0, total_mass, n_bins + 1)
    bin_id = np.searchsorted(bin_edges[1:-1], cum_mass)

    emp_by_bin = np.zeros(n_bins)
    for b in range(n_bins):
        emp_by_bin[b] = emp_sorted[bin_id == b].sum()

    return 100 * emp_by_bin / emp_by_bin.sum()


def plot_base_output_loss(results_dict, regimes, labels, save_path=None):
    """
    Plot aggregate output loss for base model regimes.

    Parameters
    ----------
    results_dict : dict
        Mapping regime -> results
    regimes : list
        List of regime names
    labels : dict
        Mapping regime -> plot label
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(8, 4.6))

    baseline_Y = results_dict["efficient"]["aggregate_output"]
    vals = [results_dict[r]["aggregate_output"] / baseline_Y * 100 for r in regimes]
    colors = ["#2E75B6", "#E69F00", "#C0392B"]

    bars = ax.bar(range(len(regimes)), vals, color=colors, width=0.55)
    ax.set_xticks(range(len(regimes)))
    ax.set_xticklabels([labels[r] for r in regimes], fontsize=9, linespacing=1.4)

    ax.set_ylabel("Aggregate output\n(efficient economy = 100)")
    ax.set_ylim(0, 110)
    ax.axhline(100, color="grey", linewidth=0.8, linestyle="--")

    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 2, f"{v:.1f}",
                ha="center", fontsize=9)

    ax.set_title("Aggregate output loss from idiosyncratic policy distortions\n"
                 "(Hopenhayn firm-dynamics model, labor supply held fixed)",
                 fontsize=10)
    fig.subplots_adjust(bottom=0.22)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)

    return fig, ax


def plot_base_employment_reallocation(results_dict, s_grid, save_path=None):
    """
    Plot employment reallocation for efficient vs mistargeted regimes.

    Parameters
    ----------
    results_dict : dict
        Mapping regime -> results
    s_grid : ndarray
        Productivity grid
    save_path : str, optional
        Path to save figure
    """
    eff_emp = employment_by_decile(results_dict["efficient"], s_grid)
    mis_emp = employment_by_decile(results_dict["mistargeted"], s_grid)

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    x = np.arange(1, 11)
    w = 0.38

    ax.bar(x - w/2, eff_emp, width=w, label="Efficient", color="#2E75B6")
    ax.bar(x + w/2, mis_emp, width=w, label="Mistargeted subsidy", color="#C0392B")

    ax.set_xlabel("Firm productivity decile (1 = least productive)")
    ax.set_ylabel("Share of aggregate employment (%)")
    ax.set_title("Employment reallocates toward low-productivity firms\n"
                 "under a mistargeted subsidy", fontsize=10)
    ax.set_xticks(x)
    ax.legend(frameon=False)

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)

    return fig, ax


def plot_credit_output(results_dict, regimes, labels, save_path=None):
    """
    Plot aggregate output for credit model regimes.

    Parameters
    ----------
    results_dict : dict
        Mapping regime -> results
    regimes : list
        List of regime names
    labels : dict
        Mapping regime -> plot label
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(10.5, 4.8))

    Y_frictionless = results_dict["frictionless"]["aggregate_output"]
    vals = [results_dict[r]["aggregate_output"] / Y_frictionless * 100 for r in regimes]
    colors = ["#2E75B6", "#8C8C8C", "#2E9E5B", "#C0392B"]

    bars = ax.bar(range(len(regimes)), vals, color=colors, width=0.55)
    ax.set_xticks(range(len(regimes)))
    ax.set_xticklabels([labels[r] for r in regimes], fontsize=8, linespacing=1.4)

    ax.set_ylabel("Aggregate output\n(frictionless economy = 100)")
    ax.set_ylim(0, 110)
    ax.axhline(100, color="grey", linewidth=0.8, linestyle="--")

    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 2, f"{v:.1f}",
                ha="center", fontsize=9)

    ax.set_title("A real friction means targeting can beat doing nothing\n"
                 "(credit-constrained firm-dynamics model, labor supply held fixed)",
                 fontsize=10)
    fig.subplots_adjust(bottom=0.22)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)

    return fig, ax


def plot_credit_constrained_share(results_dict, regimes, labels, save_path=None):
    """
    Plot share of capital-constrained firms by regime.

    Parameters
    ----------
    results_dict : dict
        Mapping regime -> results
    regimes : list
        List of regime names
    labels : dict
        Mapping regime -> plot label
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(10.5, 4.8))

    colors = ["#2E75B6", "#8C8C8C", "#2E9E5B", "#C0392B"]
    vals = [results_dict[r]["constrained_share"] * 100 for r in regimes]

    bars = ax.bar(range(len(regimes)), vals, color=colors, width=0.55)
    ax.set_xticks(range(len(regimes)))
    ax.set_xticklabels([labels[r] for r in regimes], fontsize=8, linespacing=1.4)

    ax.set_ylabel("Share of active firms\nthat are capital-constrained (%)")

    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}",
                ha="center", fontsize=9)

    ax.set_title("Targeting relaxes the constraint where it actually binds;\n"
                 "mistargeting just leaves it unchanged", fontsize=10)
    fig.subplots_adjust(bottom=0.22)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)

    return fig, ax
