# Jupyter Notebooks: GE Modelling Workflow

This directory contains three interactive notebooks that implement the professional academic workflow for solving, calibrating, and presenting GE models.

## Notebook Structure

### `01_base_model.ipynb` — Base Model: Firm Dynamics & Misallocation
**Interactive exploration of the Hopenhayn (1992) model with policy distortions**

**Sections:**
1. Setup & imports
2. Calibration parameters (editable table)
3. Discretization (AR(1) Tauchen visualization)
4. Model specification (equations and intuition)
5. Solve three regimes (efficient, untargeted, mistargeted)
6. Results table with key metrics
7. Visualizations (output loss, employment reallocation charts)
8. Key findings discussion

**Outputs:**
- `results/base/results_table.csv` — Equilibrium metrics for all three regimes
- `results/base/output_loss.png` — Bar chart of aggregate output by regime
- `results/base/employment_reallocation.png` — Employment distribution shift from mistargeting

**Run time:** ~30-60 seconds

---

### `02_credit_model.ipynb` — Credit Extension: When Targeting Can Help
**Interactive exploration of the credit-constrained model (Buera, Kaboski & Shin, 2011)**

**Sections:**
1. Setup & imports
2. Calibration parameters (credit model specifics)
3. Model specification (two inputs + collateral constraint)
4. Solve four regimes (frictionless, constrained, targeted, mistargeted)
5. Results table with gap-closing metrics
6. Visualizations (output levels, constrained share charts)
7. Key findings discussion

**Outputs:**
- `results/credit/results_table.csv` — Equilibrium metrics for all four regimes
- `results/credit/output.png` — Bar chart of aggregate output by regime
- `results/credit/constrained_share.png` — Capital constraint intensity

**Run time:** ~60-90 seconds

---

### `03_comparison.ipynb` — Synthesis: When Does Targeting Work?
**Side-by-side comparison of both models to extract policy lessons**

**Sections:**
1. Load results from both models
2. Base model output summary
3. Credit model policy effectiveness
4. Side-by-side comparison chart
5. The central insight (policy implication)
6. Extension exercises (sensitivity analysis ideas)

**Outputs:**
- `results/comparison.png` — Side-by-side bar chart highlighting the role of frictions

**Run time:** ~10 seconds

---

## How to Use

### Quick Start (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter lab

# Open notebooks in order:
# 1. 01_base_model.ipynb
# 2. 02_credit_model.ipynb
# 3. 03_comparison.ipynb
```

### Recommended Workflow

1. **Open `01_base_model.ipynb` in Jupyter Lab**
   - Read the markdown cells to understand the model
   - Look at calibration (editable if you want to experiment)
   - Run all cells (`Kernel → Restart & Run All`)
   - Observe results table and charts render inline
   - Note the key finding: mistargeting costs ~31% output

2. **Open `02_credit_model.ipynb`**
   - Repeat: read, run all cells
   - Compare constrained share metrics
   - Note: targeted policy closes ~50% of friction gap

3. **Open `03_comparison.ipynb`**
   - Load both results
   - See side-by-side comparison
   - Read the policy lesson

### Customization

Each notebook is designed for **interactive iteration**. You can:

- **Modify calibration parameters** in the calibration cells and re-run
- **Adjust visualization labels** and chart aesthetics
- **Add new analysis** (e.g., welfare decomposition, sensitivity sweeps)
- **Extend with ipywidgets** for interactive parameter sliders (optional advanced extension)

Example: To experiment with different discount factors, edit the calibration dict in cell 2 of `01_base_model.ipynb`, then re-run from there.

---

## File Organization

```
GE Modelling/
├── notebooks/
│   ├── 01_base_model.ipynb          ← Start here
│   ├── 02_credit_model.ipynb        ← Run second
│   ├── 03_comparison.ipynb          ← Run third
│   └── README.md                    ← This file
├── src/
│   └── ge_model/
│       ├── __init__.py
│       ├── core.py
│       ├── model.py
│       ├── model_credit.py
│       ├── scenarios.py
│       ├── scenarios_credit.py
│       └── plotting.py
├── results/
│   ├── base/
│   │   ├── results_table.csv
│   │   ├── output_loss.png
│   │   └── employment_reallocation.png
│   └── credit/
│       ├── results_table.csv
│       ├── output.png
│       └── constrained_share.png
├── requirements.txt
└── README.md
```

---

## The Academic Workflow

This structure mirrors how researchers at institutions like the World Bank, IMF, and NBER organize computational GE models:

1. **Build** → Define model equations, parameters, numerical solution methods
2. **Calibrate** → Display and (optionally) adjust parameters
3. **Solve** → Run equilibrium solver for all policy scenarios
4. **Visualize** → Generate publication-quality charts inline
5. **Compare** → Contrast regimes to extract policy insights
6. **Present** → Notebooks are self-contained narratives for seminars/papers

This is preferable to shell scripts because:
- ✅ **Interactive**: Cell-by-cell execution allows exploration
- ✅ **Transparent**: Equations and intuition live in markdown
- ✅ **Reproducible**: Same notebook, same outputs every time
- ✅ **Shareable**: Notebooks are native to Jupyter; no extra tooling needed
- ✅ **Scalable**: Easy to add new scenarios, sensitivity analysis, or extensions

---

## Troubleshooting

**Import errors?**
- Ensure you've run `pip install -r requirements.txt` from the project root
- Verify `src/` is on the Python path (first cell handles this)

**Plots not rendering?**
- If using Jupyter Lab, you might need: `jupyter labextension install @jupyterlab/mathjax3`
- Or use JupyterNotebook (not Lab) as a fallback

**Slow performance?**
- The VFI (value function iteration) can take 20-30 seconds per regime
- This is normal; the numerical solver is converging to < 1e-9 tolerance
- Consider reducing maxit in scenarios.py if needed (not recommended for publication)

**Results not saving?**
- Check that `results/base/` and `results/credit/` folders exist
- Ensure write permissions in the project directory

---

## Next Steps & Extensions

### Easy Extensions
- Add a fourth notebook (`04_sensitivity_analysis.ipynb`) with parameter sweeps
- Create a `05_replication_guide.ipynb` walking through the math
- Add welfare decomposition (consumer surplus, producer surplus, deadweight loss)

### Advanced Extensions
- Interactive parameter sliders using `ipywidgets`
- Add a comparison to empirical World Bank Enterprise Survey data
- Extend to multiple industries with inter-industry linkages
- Add a nominal rigidity friction alongside credit constraints

### Paper Writing
- Export notebook as PDF for appendix
- Use `nbconvert` to convert to .tex for LaTeX integration
- Reference cells as "see Notebook 1, Cell X" in main paper

---

## Reference

**Economic models implemented:**
- Hopenhayn (1992): "Entry, exit, and firm dynamics in long-run equilibrium"
- Restuccia & Rogerson (2008): "Policy distortions and aggregate productivity"
- Buera, Kaboski & Shin (2011): "Finance and development: A tale of two sectors"

**Key results:**
- Untargeted misallocation → 11% output loss (R&R baseline)
- Mistargeted misallocation → 31% output loss (amplified by endogenous exit)
- Targeted credit policy → closes ~50% of friction gap when real friction exists
