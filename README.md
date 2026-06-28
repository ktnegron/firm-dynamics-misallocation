# Firm Dynamics and Misallocation from Policy Distortions
### A Hopenhayn (1992) industry-equilibrium model extended with idiosyncratic distortions à la Restuccia & Rogerson (2008)

**Author's note:** This is a self-directed replication/extension project built to
demonstrate the ability to solve, calibrate, and simulate a structural firm-dynamics
GE model and use it for a policy counterfactual — not a calibration to real
microdata. Parameters are stylized and chosen to produce an internally consistent,
qualitatively sensible equilibrium, not to match a specific country's data.

---

## 1. The question

A government (or a development finance institution) introduces a subsidized
credit/guarantee program for small firms. If the program is **untargeted** — or
worse, **mistargeted** toward the weakest firms rather than the most productive
ones — what does it do to aggregate output, holding the total amount of labor in
the economy fixed?

This is the standard "policy distortions and aggregate productivity" question from
the misallocation literature (Restuccia & Rogerson, 2008; Hsieh & Klenow, 2009),
posed inside a dynamic model with firm entry, exit, and productivity shocks
(Hopenhayn, 1992) rather than a static accounting decomposition.

## 2. Model

- Firms draw a persistent productivity shock `s` (AR(1) in logs, `ρ=0.90`,
  discretized with Tauchen's method into 25 grid points).
- Each period, an active firm chooses labor `n` to maximize static profit
  `(1-τ)·p·s·n^α - n`, where `p` is the output price, `α=0.65` is the curvature of
  the production function, and `τ` is an idiosyncratic, **time-invariant** wedge
  (a tax if `τ>0`, a subsidy if `τ<0`) assigned to the firm at entry.
- Firms decide to exit when their continuation value falls below zero, after
  paying a per-period fixed operating cost.
- A free-entry condition (expected value of entry = entry cost) pins down the
  equilibrium price `p*`; labor-market clearing (aggregate labor supply normalized
  to 1 in every scenario) pins down the mass of entrants.
- Because aggregate labor input is identical across scenarios by construction,
  **differences in aggregate output across scenarios are a clean measure of the
  aggregate productivity (TFP) cost of misallocation** — no separate TFP
  decomposition is needed.

Three economies are solved and compared:

| Regime | Description |
|---|---|
| **Efficient** | `τ=0` for all firms. |
| **Untargeted distortion** | `τ` drawn from `{-30%, -15%, 0, +15%, +30%}` independently of entry productivity. |
| **Mistargeted subsidy** | Same five wedges, but assigned by entry-productivity quintile: the *least* productive entrants get the largest subsidy, the *most* productive get taxed. |

## 3. Results

| Regime | Aggregate output (efficient = 100) | Output loss | Exit rate |
|---|---|---|---|
| Efficient | 100.0 | — | 14.8% |
| Untargeted distortion | 88.6 | 11.4% | 12.1% |
| Mistargeted subsidy | 69.3 | 30.7% | 3.0% |

Two results worth highlighting:

1. **Even distortions uncorrelated with productivity destroy output** (~11%),
   because the production function is concave — misallocating labor away from its
   efficient distribution lowers output even with no systematic bias. This is the
   classic Restuccia-Rogerson point, and a useful caution against assuming
   "untargeted" support is harmless.
2. **Mistargeting is far more costly** (~31% loss) and **roughly halves the exit
   rate** — subsidized low-productivity firms that would otherwise have failed
   stay in business instead, occupying labor that would have gone to more
   productive firms. The employment-share chart shows labor shifting away from the
   most productive decile of firms toward the middle of the distribution.

![Output loss](chart_output_loss.png)
![Employment reallocation](chart_employment_reallocation.png)

## 4. Caveats

- Single input (labor only); no capital, no trade, no financial-friction
  microfoundation for *why* a subsidy would be mistargeted in practice.
- Calibration is illustrative, not estimated from data (a natural next step would
  be disciplining the productivity process and entry distribution against
  World Bank Enterprise Survey firm-size data, in the spirit of the calibration
  approach used in DECIG's own firm-level work).
- Distortions are exogenous and permanent per firm; a richer version would let
  policy eligibility depend on firm characteristics that change over time.

## 5. Files

- `model.py` — Tauchen discretization, firm value function (VFI), stationary
  distribution, and the equilibrium solver (free entry + labor-market clearing).
- `scenarios.py` — calibration and the three policy regimes.
- `analysis.py` — runs all three regimes, produces `results_table.csv` and the
  two charts above.

---

## 6. Extension: when can targeting productive firms actually help?

The exercise above has an uncomfortable implication: in that model, a subsidy
**targeted at the most productive firms** would *still* lower output relative
to doing nothing. That's not a calibration quirk — it's the central result of
this literature. The undistorted competitive equilibrium already allocates
every input to its efficient use; a selective subsidy pushes the favored
firms *past* their own efficient size while the firms taxed to pay for it are
pushed *below* theirs. You're not adding value, you're just moving the same
misallocation in a different direction.

So when *can* "subsidize the best firms" genuinely beat doing nothing? Only if
there's a **real, pre-existing friction** for the policy to correct — one that
exists independently of the policy itself. This extension adds the canonical
one: a **credit/collateral constraint** (Buera, Kaboski & Shin, 2011-style).

**The mechanism:** firms now use two inputs, capital and labor. Capital must
be financed, and a firm can borrow at most `λ × a`, where `a` is its net
worth. Net worth is drawn **independently of productivity** at entry — talent
and wealth are not the same thing. This creates genuinely talented entrants
who are stuck below their efficient scale simply because they're poor, not
because they're unproductive — a real distortion the simple model didn't have
room for.

Four economies, in `model_credit.py` / `scenarios_credit.py` / `analysis_credit.py`:

| Regime | Aggregate output (frictionless = 100) | Share of firms constrained |
|---|---|---|
| Frictionless (no credit constraint) | 100.0 | 0% |
| Constrained, no policy | 79.6 | 73.3% |
| **Targeted** credit access (favors top-quintile entrants) | **89.4** | 48.4% |
| Mistargeted credit access (favors bottom-quintile entrants) | 79.6 | 73.3% |

![Credit policy output](chart_credit_output.png)
![Constrained share](chart_credit_constrained_share.png)

**This time, targeting the productive firms works** — it closes about half
the gap between the constrained economy and the frictionless benchmark,
because it's relaxing a constraint that was genuinely binding on exactly
those firms.

**And mistargeting here is *wasted*, not *harmful*.** This is a second useful
contrast with the tax/subsidy exercise above. Favoring low-productivity
entrants with more borrowing room does essentially nothing to aggregate
output, because those firms didn't want much capital in the first place — you
can't force a firm to use a credit line it has no productive use for. Compare
that to the original exercise, where a mistargeted *tax-and-subsidy* scheme
actively destroyed output, because a tax is a forced distortion, not an
unused option. Relaxing a non-binding constraint costs nothing; subsidizing
an already-efficient firm's revenue actively misallocates resources. Same
underlying instinct ("help the good firms"), opposite consequence, depending
entirely on *what kind* of friction the policy is responding to.

**The general lesson, stated once:** whether "pick the winners" is good or
bad policy advice depends entirely on whether there's a real, independent
market failure for the policy to correct. In a frictionless model, it's
always bad advice. In a model with a genuine financing friction, it can be
exactly right — provided the targeting is accurate, which is itself the hard
part in practice (a real guarantee program doesn't get to observe `a` and `s`
the way this code does).

### Additional files
- `model_credit.py` — the two-input (capital, labor) firm problem with the
  collateral constraint; closed-form input demands, otherwise the same VFI /
  stationary-distribution machinery as `model.py`.
- `scenarios_credit.py` — calibration and the four credit-policy regimes.
- `analysis_credit.py` — runs all four, produces `results_table_credit.csv`
  and the two charts above.

