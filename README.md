# Should a Credit Guarantee Program Screen Applicants by Productivity?

A self-contained general equilibrium policy analysis notebook.

---

## Overview

Credit guarantee schemes for small and medium firms typically face one early design question: **screen applicants by productivity/growth potential, or extend credit on a first-come basis?**

This notebook builds a small general equilibrium (GE) model to inform that choice. Rather than evaluating a program only on the firms it directly supports, the model solves for economy-wide prices — wages and the cost of capital — that adjust in response to the policy. A design that looks effective in partial equilibrium can deliver a different result once these economy-wide effects are accounted for.

---

## The Model

Firms have two independent characteristics:
- **Productivity** (`s`) — how efficiently they combine inputs
- **Net worth** (`a`) — the collateral they can pledge to a lender

A lender will only finance capital up to `k ≤ λ·a`. A highly productive firm with little net worth can be held below its efficient scale — not for lack of talent, but because no lender will finance the capital it needs.

The model solves for the firm-size distribution and output price consistent with free entry and labor-market clearing, then compares aggregate output across four policy regimes that differ only in which firms get their borrowing limit (`λ`) raised.

**Five building blocks:**
1. **Technology** — Cobb-Douglas production with decreasing returns; AR(1) productivity process discretized via Tauchen's method
2. **Constrained firm problem** — static profit maximization subject to the collateral cap `k ≤ λ·a`
3. **Dynamic exit decision** — Bellman equation with an exit option; firms shut down rather than accumulate losses
4. **Aggregation** — stationary distribution of firms across productivity and net-worth types
5. **Market clearing** — free entry pins down the output price `p`; labor clearing pins down the mass of active firms `M`

**Solution cadence:** price first → stationary distribution second → entrant mass last.

---

## Policy Experiments

Four economies are compared (all with the same labor supply):

| Regime | Description |
|---|---|
| **Baseline** | Uniform collateral multiplier `λ = 1.5` for all firms |
| **Untargeted** | `λ` raised to 5.0 for a randomly selected subset of firms |
| **Targeted (productive)** | `λ` raised to 5.0 for the top-quintile productivity entrants |
| **Mistargeted (unproductive)** | `λ` raised to 5.0 for the bottom-quintile productivity entrants |

---

## Key Findings

- **Targeted credit access works** — directing relaxed borrowing limits to the most productive firms closes a meaningful share of the output gap between the constrained economy and the frictionless benchmark, because it relaxes a constraint that was genuinely binding on exactly those firms.
- **Mistargeting is wasted, not harmful** — subsidizing low-productivity entrants with more borrowing room does little to aggregate output, because those firms had limited demand for capital to begin with. Unlike a tax-and-subsidy scheme, you cannot force a firm to use a credit line it has no productive use for.
- **The general lesson** — whether "pick the winners" is good policy depends entirely on whether there is a real, independent market failure for the policy to correct.

---

## Parameters (Stylized Calibration)

| Parameter | Value | Description |
|---|---|---|
| `ρ` | 0.90 | Persistence of productivity AR(1) |
| `σ` | 0.20 | Volatility of productivity shocks |
| `θ_k` | 0.30 | Capital curvature |
| `θ_n` | 0.35 | Labor curvature |
| `r` | 0.10 | Capital rental rate |
| `β` | 0.85 | Discount factor |
| `λ_base` | 1.5 | Baseline collateral multiplier |
| `λ_boost` | 5.0 | Policy collateral multiplier |

Parameters are illustrative, not estimated from country-specific data.

---

## Limitations

- Capital is supplied from outside at a fixed rental rate — the interest rate does not respond to credit policy
- Calibration is stylized; an operational version would require firm-level data (e.g., World Bank Enterprise Surveys) to discipline the productivity process and entry distribution
- Distortions are static; a richer version would allow eligibility to evolve with firm characteristics over time

---

## Requirements

```
numpy
pandas
matplotlib
scipy
```

Run `pip install -r requirements.txt` if needed.

---

## References

- Hopenhayn, H. A. (1992). Entry, exit, and firm dynamics in long run equilibrium. *Econometrica*, 60(5), 1127–1150.
- Restuccia, D., & Rogerson, R. (2008). Policy distortions and aggregate productivity with heterogeneous establishments. *Review of Economic Dynamics*, 11(4), 707–720.
- Buera, F. J., Kaboski, J. P., & Shin, Y. (2011). Finance and development: A tale of two sectors. *American Economic Review*, 101(5), 1964–2002.
- Tauchen, G. (1986). Finite state Markov-chain approximations to univariate and vector autoregressions. *Economics Letters*, 20(2), 177–181.
