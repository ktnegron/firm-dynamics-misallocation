# Getting Started: Complete Workflow Guide

## Step 0: One-Time Setup

### 0a. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs: numpy, scipy, pandas, matplotlib, jupyter, ipywidgets

**Time:** ~2 minutes  
**Do this once.** You don't need to repeat it.

### 0b. Verify Installation
```bash
python -c "import numpy, scipy, pandas, matplotlib, jupyter; print('All dependencies installed OK')"
```

---

## Step 1: Launch Jupyter Lab

```bash
jupyter lab
```

This opens Jupyter in your default browser (usually `http://localhost:8888`).

**What you'll see:** File browser on the left, main editor panel on the right.

---

## Step 2: Open Notebook #1 — Base Model

1. In the left file panel, navigate to `notebooks/`
2. Double-click `01_base_model.ipynb`

The notebook opens with a title and several cells (code blocks and text).

---

## Step 3: Run the Base Model Workflow (5-7 minutes)

**Follow the notebook cells in order. Read the markdown (text) cells first, then run code cells.**

### Cell 1: Setup
- **What it does:** Import libraries, add src/ to Python path
- **Your action:** Click the cell, then press `Shift+Enter` (or click the play button)
- **Result:** You'll see `✓ Imports successful`

### Cell 2: Calibration
- **What it does:** Display calibration parameters as a table
- **Your action:** Run it (`Shift+Enter`)
- **Result:** Pretty table showing α=0.65, β=0.85, etc.
- **Optional:** Edit numbers here and re-run if you want to experiment

### Cell 3: Discretization
- **What it does:** Creates AR(1) productivity grid, plots it
- **Your action:** Run it
- **Result:** Two scatter plots showing the discretized productivity process

### Cell 4: Model Specification
- **What it does:** Prints the model equations
- **Your action:** Run it
- **Result:** Text describing the firm problem and value function

### Cell 5: Solve Three Regimes
- **What it does:** Solves base model for (efficient, untargeted, mistargeted)
- **Your action:** Run it
- **Result:** Output like `[efficient] ✓ p*=1.2897, Y=1.1929`
- **Time:** ~30-60 seconds (this is where the computation happens)

### Cell 6: Results Table
- **What it does:** Creates pandas DataFrame with results
- **Your action:** Run it
- **Result:** Table with 3 rows (one per regime) and columns like "Aggregate Output", "Output Loss (%)"
- **Saved:** `results/base/results_table.csv`

### Cell 7: Chart 1 - Output Loss
- **What it does:** Bar chart comparing output across regimes
- **Your action:** Run it
- **Result:** Blue, orange, and red bars; chart saved as `results/base/output_loss.png`

### Cell 8: Chart 2 - Employment Reallocation
- **What it does:** Shows how mistargeting shifts jobs toward weak firms
- **Your action:** Run it
- **Result:** Side-by-side bars comparing efficient vs. mistargeted; saved as `results/base/employment_reallocation.png`

### Cell 9: Key Findings
- **What it does:** Summarizes the main insights
- **Your action:** Run it (mostly text output)
- **Result:** Discussion of why mistargeting costs 31% output

---

## Step 4: Open Notebook #2 — Credit Model

1. Open a new tab in Jupyter Lab (File → New Notebook, but actually open `notebooks/02_credit_model.ipynb`)
2. Follow the same pattern as Notebook 1

**Same 9-cell structure:**
- Setup
- Calibration
- Model specification (now with two inputs: capital + labor, plus collateral constraint)
- Solve four regimes (frictionless, constrained, targeted, mistargeted)
- Results table
- Chart 1: Output levels
- Chart 2: Constrained share
- Key findings

**Key difference:** 
- This model takes ~60-90 seconds (four regimes instead of three)
- Results saved to `results/credit/`

---

## Step 5: Open Notebook #3 — Comparison

1. Open `notebooks/03_comparison.ipynb`

**Structure (4 cells):**
1. **Load results** — Reads both CSV files from `results/base/` and `results/credit/`
2. **Base model summary** — Prints base model results
3. **Credit model summary** — Prints credit model results
4. **Side-by-side comparison** — Creates one chart showing both models
5. **Policy implication** — Explains the central lesson

**Key insight:** This notebook shows *why* targeting fails in the base model but works in the credit model.

---

## The Complete Workflow at a Glance

```
1. Install dependencies (pip install -r requirements.txt)
                ↓
2. Launch Jupyter (jupyter lab)
                ↓
3. Run 01_base_model.ipynb (cells 1-9 in order)
        ~30-60 seconds execution time
        Produces: results/base/*.csv and results/base/*.png
                ↓
4. Run 02_credit_model.ipynb (cells 1-9 in order)
        ~60-90 seconds execution time
        Produces: results/credit/*.csv and results/credit/*.png
                ↓
5. Run 03_comparison.ipynb (cells 1-5)
        ~10 seconds execution time
        Produces: results/comparison.png
                ↓
6. Review results in results/ folder
                ↓
7. (Optional) Modify calibration and re-run
```

**Total time:** ~5 minutes (first run)

---

## File Organization (After Cleanup)

```
GE Modelling/
├── notebooks/                              ← START HERE
│   ├── 01_base_model.ipynb                ← RUN FIRST
│   ├── 02_credit_model.ipynb              ← RUN SECOND
│   ├── 03_comparison.ipynb                ← RUN THIRD
│   └── README.md                          ← Detailed guide
│
├── src/ge_model/                          ← Core library (do not edit unless extending)
│   ├── __init__.py
│   ├── core.py                            (Tauchen, stationary_dist)
│   ├── model.py                           (Base model solver)
│   ├── model_credit.py                    (Credit model solver)
│   ├── scenarios.py                       (Base model regimes)
│   ├── scenarios_credit.py                (Credit model regimes)
│   └── plotting.py                        (Visualization functions)
│
├── results/                               ← OUTPUTS (auto-created on first run)
│   ├── base/
│   │   ├── results_table.csv
│   │   ├── output_loss.png
│   │   └── employment_reallocation.png
│   └── credit/
│       ├── results_table.csv
│       ├── output.png
│       └── constrained_share.png
│
├── requirements.txt                       ← Dependencies
├── README.md                              ← Original project description
├── PROJECT_STRUCTURE.md                   ← Architecture overview
└── RESTRUCTURING_COMPLETE.md              ← What changed
```

---

## Running the Notebooks: Detailed Instructions

### Method 1: Interactive (Recommended)

```bash
jupyter lab
# Opens browser, navigate to notebooks/01_base_model.ipynb
# Run cells one by one (Shift+Enter or click play button)
# Read markdown between cells
```

**Advantages:**
- See results immediately
- Easy to modify parameters and re-run
- Plots display inline
- Can save notebook with your notes

### Method 2: Run All Cells at Once

1. Open notebook
2. Press `Ctrl+A` (Mac: `Cmd+A`) to select all
3. Or use menu: `Kernel → Restart & Run All`

**Advantages:**
- Faster (no waiting between cells)
- Reproduces results exactly

**Disadvantages:**
- Can't modify/re-run individual cells easily

### Method 3: Convert to Python (Advanced)

```bash
jupyter nbconvert --to script notebooks/01_base_model.ipynb
python notebooks/01_base_model.py
```

---

## Cadence (Suggested Pace)

### Session 1: Exploration (30 minutes)
1. Run 01_base_model.ipynb
2. Run 02_credit_model.ipynb
3. Run 03_comparison.ipynb
4. Read the key findings
5. Browse results/ folder to see outputs

### Session 2: Understanding (1 hour)
1. Go back and read markdown cells carefully
2. Understand the model specification
3. Look at calibration parameters
4. Review the charts and tables

### Session 3: Customization (as needed)
1. Edit calibration parameters
2. Re-run notebooks to see sensitivity
3. Modify plot aesthetics in plotting.py
4. Add new analyses (optional)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'ge_model'"
- Make sure you're in the `GE Modelling` directory when you launch Jupyter
- First cell of notebook should have: `sys.path.insert(0, 'src')` ✓ (already there)

### "No module named jupyter"
- Run: `pip install -r requirements.txt`

### Plots not displaying
- Make sure `%matplotlib inline` is in first code cell ✓ (already there)
- Restart kernel: `Kernel → Restart`

### Slow performance
- VFI converges to 1e-9 tolerance (very accurate, slow)
- Normal: ~30-90 seconds per notebook
- First run is sometimes slower due to compilation

### Results folder not created
- Auto-created on first notebook run
- If missing, manually create: `mkdir -p results/base results/credit`

---

## What Happens in Each Notebook

### Notebook 1: Base Model (01_base_model.ipynb)
- **Question answered:** How much output do uncorrelated vs. mistargeted distortions cost?
- **Time:** 5-7 minutes (including computation)
- **Output:** 3 regimes solved, 2 charts, 1 CSV table
- **Key finding:** Mistargeting costs 31% output vs. 11% for uncorrelated distortion

### Notebook 2: Credit Model (02_credit_model.ipynb)
- **Question answered:** When can targeted policy actually help?
- **Time:** 7-10 minutes (including computation)
- **Output:** 4 regimes solved, 2 charts, 1 CSV table
- **Key finding:** Targeted credit policy closes ~50% of friction gap

### Notebook 3: Comparison (03_comparison.ipynb)
- **Question answered:** What's the difference between the two models?
- **Time:** 2-3 minutes
- **Output:** Side-by-side comparison chart
- **Key finding:** The central insight — targeting works only when there's a real friction

---

## Next Steps After Running the Notebooks

1. **Share results** — Export notebooks as PDF for presentations
2. **Modify parameters** — Change calibration and see how results change
3. **Add analysis** — Create `04_sensitivity_analysis.ipynb` for parameter sweeps
4. **Extend the model** — Add capital to base model, or add taxes to credit model
5. **Write a paper** — Use notebooks as appendix to main document

---

## One-Page Cheat Sheet

```
QUICK START:

1. pip install -r requirements.txt
2. jupyter lab
3. Open notebooks/01_base_model.ipynb
4. Run all cells (Shift+Enter each cell)
5. Repeat for 02_credit_model.ipynb
6. Repeat for 03_comparison.ipynb
7. Check results/ folder for outputs

TOTAL TIME: 5-10 minutes
```

---

## Questions?

- **How do I modify the model?** → Edit src/ge_model/model.py or model_credit.py
- **How do I add a new regime?** → Edit scenarios.py and add to notebook
- **How do I change calibration?** → Edit the CALIBRATION dict in scenarios.py
- **How do I save results?** → Notebooks auto-save to results/base/ and results/credit/
- **Can I use this for a paper?** → Yes! Export to PDF and include as appendix

---

**Status:** Clean setup, ready to run. Follow the cadence above.
