# GE Modelling: Refactored for Interactive Academic Workflow

A professional, modular implementation of firm-dynamics GE models with policy applications. Structured for interactive Jupyter-based exploration in the style of World Bank, IMF, and research labs.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch Jupyter
jupyter lab

# 3. Open notebooks/ and run:
#    01_base_model.ipynb → 02_credit_model.ipynb → 03_comparison.ipynb
```

**Running the full workflow takes ~2 minutes and produces publication-quality charts.**

---

## Project Structure

```
GE Modelling/
│
├── notebooks/                      # Interactive workflow (START HERE)
│   ├── 01_base_model.ipynb        # Build, calibrate, solve, visualize base model
│   ├── 02_credit_model.ipynb      # Same for credit-constrained model
│   ├── 03_comparison.ipynb        # Side-by-side comparison & policy insights
│   └── README.md                  # Detailed notebook guide
│
├── src/ge_model/                  # Core library (professional structure)
│   ├── __init__.py               # Clean API exports
│   ├── core.py                   # Shared utilities (Tauchen, stationary_dist)
│   ├── model.py                  # Base Hopenhayn model
│   ├── model_credit.py           # Credit-constrained extension
│   ├── scenarios.py              # Regime definitions (base model)
│   ├── scenarios_credit.py       # Regime definitions (credit model)
│   └── plotting.py               # All visualization functions
│
├── results/                       # Outputs (organized by model)
│   ├── base/
│   │   ├── results_table.csv
│   │   ├── output_loss.png
│   │   └── employment_reallocation.png
│   └── credit/
│       ├── results_table.csv
│       ├── output.png
│       └── constrained_share.png
│
├── requirements.txt               # Dependencies
├── README.md                      # This file
└── kilic_cv.pdf                  # (original project info)
```

---

## The Academic Workflow

This project implements the standard workflow in economics research, especially at international organizations:

### 1. **Build** — Define the model
- Notebook: markdown cells explaining equations
- Code: Functions for static choice, value function iteration, equilibrium

### 2. **Calibrate** — Set parameters
- Notebook: Calibration table (editable if you want to experiment)
- Code: Defaults in `scenarios.py` and `scenarios_credit.py`

### 3. **Solve** — Run equilibrium solver
- Notebook: Call `run_base_scenario()` or `run_credit_scenario()`
- Code: Free-entry condition + labor-market clearing solved simultaneously

### 4. **Visualize** — Generate charts
- Notebook: Inline plots (PNG exports to `results/` folder)
- Code: Plotting functions return both figure handle and saved file

### 5. **Compare & Present** — Extract policy insights
- Notebook: Side-by-side regimes, tables, key findings
- Natural format for presentations, papers, seminars

---

## Key Features of the Refactored Structure

### ✅ Modularity
- **Before**: 6 separate scripts with tight coupling (analysis.py auto-executes)
- **After**: Clean Python package where functions are imported and called explicitly

### ✅ Interactivity
- **Before**: Run `python analysis.py` → output to files
- **After**: Run cells in Jupyter, see plots inline, modify parameters and re-run

### ✅ Reproducibility
- **Before**: Hard-coded parameters in scenarios.py; must re-edit to experiment
- **After**: Calibration as a dict; easy to override and compare

### ✅ Professional Structure
- **Before**: Flat directory with model.py, model_credit.py, analysis.py, etc.
- **After**: `src/ge_model/` package with `__init__.py` and semantic module names

### ✅ Separation of Concerns
- **core.py**: Utilities (Tauchen, stationary distribution) — *shared by both models*
- **model.py, model_credit.py**: Solution algorithms — *domain logic*
- **scenarios.py, scenarios_credit.py**: Regime definitions — *configuration data*
- **plotting.py**: Visualization — *presentation layer*
- **Notebooks**: User interaction and narrative — *the workflow*

---

## What's Inside Each Module

### `src/ge_model/core.py`
**Shared utilities:**
- `tauchen(n, rho, sigma, m=3.0)` — Discretize AR(1) process
- `stationary_dist(exit_policy, Q, entry_dist)` — Firm population dynamics

### `src/ge_model/model.py`
**Base Hopenhayn model (single input, labor only):**
- `static_choice(p, s_grid, tau, alpha, w=1.0)` — Labor demand & profit
- `solve_value(p, s_grid, Q, alpha, beta, cf, tau)` — Value function iteration
- `solve_equilibrium(s_grid, Q, alpha, beta, cf, ce, L_supply, tau_vals, entry_weight)` — Full solver

### `src/ge_model/model_credit.py`
**Credit-constrained model (two inputs: capital + labor):**
- `static_choice_credit(p, s_grid, k_max, theta_k, theta_n, r, w=1.0)` — Two-input choice with collateral constraint
- `solve_value_credit(...)` — VFI for constrained firm
- `solve_equilibrium_credit(...)` — Full solver with constraint tracking

### `src/ge_model/scenarios.py`
**Policy regimes for base model:**
- `CALIBRATION` — Default parameters
- `create_regime_config(regime, s_grid, nu)` — Define entry distribution for regime
- `run_scenario(regime, calibration=None)` — Run a single regime

### `src/ge_model/scenarios_credit.py`
**Policy regimes for credit model:**
- Same structure as scenarios.py, but for four regimes (frictionless, constrained, targeted, mistargeted)

### `src/ge_model/plotting.py`
**Visualization functions:**
- `plot_base_output_loss()` — Output loss chart
- `plot_base_employment_reallocation()` — Employment distribution shift
- `plot_credit_output()` — Credit model output by regime
- `plot_credit_constrained_share()` — Constraint intensity chart

### `src/ge_model/__init__.py`
**Clean public API:**
```python
from ge_model import (
    run_base_scenario, run_credit_scenario,
    plot_base_output_loss, plot_credit_output,
    ...
)
```

---

## The Three Models

### Model 1: Base Model (Hopenhayn 1992 + Restuccia & Rogerson 2008)

**Question:** How much output is lost to idiosyncratic policy distortions?

**Key assumptions:**
- Single input (labor); no capital
- Productivity: AR(1) in logs, persistent
- Distortion: time-invariant wedge τ (tax or subsidy), assigned at entry
- Exogenous aggregate labor supply

**Three regimes:**
1. **Efficient** (τ=0): Benchmark
2. **Untargeted** (τ random): Even uncorrelated misallocation costs output
3. **Mistargeted** (τ against productivity): Misallocation concentrated on weak firms

**Results:**
- Untargeted: 11% output loss
- Mistargeted: 31% output loss
- **Lesson:** Targeting productive firms *still hurts* in a frictionless model

---

### Model 2: Credit-Constrained Model (Buera, Kaboski & Shin 2011)

**Question:** When can targeted credit policy actually improve output?

**Key change:** Add collateral constraint k ≤ λ·a, where a is net worth drawn *independently* of productivity.

**Key assumptions:**
- Two inputs (capital + labor)
- Wealth and talent uncorrelated → talented but poor firms are constrained
- This is a *real* friction, not just a wedge

**Four regimes:**
1. **Frictionless** (λ = ∞): Upper-bound benchmark
2. **Constrained** (λ = 1.5): Baseline with real friction, no policy
3. **Targeted** (λ_boost = 5.0 for top-quintile entrants): Policy helps where friction binds
4. **Mistargeted** (λ_boost for bottom-quintile): Policy wasted but not harmful

**Results:**
- Constrained economy: 20.4% below frictionless
- Targeted policy: closes ~50% of friction gap (89.4 vs 79.6)
- Mistargeted policy: no effect (firms don't want credit they can't use)
- **Lesson:** Targeting *works* when there's a real friction to correct

---

### Model 3: Comparison

**Central insight:**
Whether "pick the winners" is good policy depends entirely on whether there's a **real, independent market failure**.

- **No friction (base model)**: Targeting misallocates an efficient equilibrium → always bad
- **Real friction (credit model)**: Targeting relaxes a genuine constraint → can be good

---

## Running the Notebooks

### Interactive Mode (Recommended)

```bash
jupyter lab
# Open 01_base_model.ipynb
# Run all cells (Kernel → Restart & Run All)
# Observe results table and charts render inline
# Edit calibration parameters and re-run to experiment
```

### Batch Mode (For CI/CD, reproducibility checks)

```bash
# Convert notebook to Python and run
jupyter nbconvert --to script notebooks/01_base_model.ipynb
python notebooks/01_base_model.py
```

---

## Customization & Extensions

### Easy: Change a parameter
1. Open `01_base_model.ipynb`
2. Edit `CALIBRATION` dict in cell 2
3. Re-run from that point

### Medium: Add a new regime
1. Edit `scenarios.py` → add a case in `create_regime_config()`
2. Add a label in the notebook
3. Call `run_scenario("new_regime")`

### Advanced: Add a new model variant
1. Create `src/ge_model/model_variant.py`
2. Follow the same structure: `static_choice`, `solve_value`, `solve_equilibrium`
3. Create `scenarios_variant.py` and a new notebook
4. Export from `__init__.py`

---

## Performance

**Expected runtime:**
- Base model: 30–60 seconds (solve 3 regimes)
- Credit model: 60–90 seconds (solve 4 regimes)
- Comparison: ~10 seconds (load and chart)
- **Total:** ~2 minutes for the full workflow

**Bottleneck:** Value function iteration converges to < 1e-9 tolerance. If faster prototyping is needed:
- Reduce `N_Z` (productivity grid points) from 25 to 15
- Reduce tolerance from 1e-9 to 1e-6

---

## Testing Your Setup

To verify everything is installed and configured correctly:

```python
# In a Python shell or notebook:
import sys
sys.path.insert(0, 'src')

from ge_model import run_base_scenario
res = run_base_scenario("efficient")
print(f"Base model equilibrium price: {res['p']:.4f}")
print(f"Aggregate output: {res['aggregate_output']:.4f}")
```

If this runs without errors and prints reasonable values (p ≈ 1-2, Y ≈ 10-20), you're good to go!

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'ge_model'"
- Ensure `sys.path.insert(0, 'src')` is in the first cell of the notebook
- Or run from the project root: `cd "GE Modelling"` before launching Jupyter

### "FileNotFoundError: results/base/ does not exist"
- Folders are created automatically on first notebook run
- If not, manually create: `mkdir -p results/base results/credit`

### Slow performance
- VFI iterations can take time. This is normal.
- Use a faster computer or reduce grid size for prototyping

### Plots not displaying in Jupyter Lab
- Try Jupyter Notebook (classic) as a fallback
- Or: `jupyter lab --NotebookApp.open_browser=false` and open manually

---

## References & Citations

The models in this project are based on:

1. **Hopenhayn, H. (1992).** Entry, exit, and firm dynamics in long-run equilibrium. *Econometrica*, 60(5), 1127–1150.

2. **Restuccia, D., & Rogerson, R. (2008).** Policy distortions and aggregate productivity with heterogeneous establishments. *International Economic Review*, 49(4), 1437–1466.

3. **Buera, F. J., Kaboski, J. P., & Shin, Y. (2011).** Finance and development: A tale of two sectors. *American Economic Review*, 101(5), 1964–2002.

4. **Hsieh, C.-T., & Klenow, P. J. (2009).** Misallocation and manufacturing TFP in China and India. *Quarterly Journal of Economics*, 124(4), 1403–1448.

---

## Author's Note

This is a self-directed replication/extension project demonstrating the ability to:
- Solve a structural firm-dynamics GE model
- Calibrate and simulate across policy scenarios
- Use policy counterfactuals to quantify misallocation costs
- Present results in a reproducible, academic workflow

Parameters are stylized and chosen for internal consistency and pedagogical clarity, not to match specific microdata. As a real extension, you would discipline the productivity process and entry distribution against World Bank Enterprise Survey firm-size data.

---

## Questions & Feedback

For questions about the code, models, or workflow:
- Check the notebooks/README.md for detailed guidance
- Review docstrings in src/ge_model/*.py for function signatures
- Examine the references above for the underlying economics
