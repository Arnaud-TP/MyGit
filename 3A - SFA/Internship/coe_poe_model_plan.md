# COE / POE Commodity Exposure Model
## Documentation Summary · Python Project Outline · Mathematical Modelling Plan

---

## PART I — DOCUMENTATION LANDSCAPE

### 1. Regulatory & Industry Standards

#### 1.1 ISDA SIMM (already implemented — `isda_simm.py`)
- **Version**: SIMM v2.8+2506, effective 6 December 2025
- **Relevance**: Provides the commodity bucket taxonomy (17 buckets), within-bucket correlations `ρ_{kl}`, cross-bucket correlations `γ_{bc}`, risk weights `RW_b`, concentration thresholds `CT_b`, and cross-risk-class correlations `ψ_{rs}`. All of these feed directly into the COE/POE sensitivity grid.
- **Key sections to re-read**: §H (Commodity), §B (delta/vega/curvature aggregation formulas), §J.4 (concentration thresholds).

#### 1.2 Basel III / CRR2 — SA-CCR (Standardised Approach for Counterparty Credit Risk)
- **Document**: BCBS 279 "The standardised approach for measuring counterparty credit risk exposures" (March 2014, revised April 2014); CRR2 Art. 274–280 (EU implementation).
- **Relevance**: Defines Replacement Cost (RC) and Potential Future Exposure (PFE) add-ons for commodity derivatives. The PFE add-on methodology uses *supervisory delta*, *supervisory duration*, and *hedging sets* — directly analogous to the COE/POE decomposition.
- **Key tables**: Table 2 (commodity supervisory factors), Table 3 (correlation parameters ρ = 0.40 for commodity same hedging set), maturity factor `MF`.

#### 1.3 ISDA Credit Support Annex (CSA) / FRTB-CVA
- **Relevance**: Governs margining schedules; COE/POE must be computed under both margined (MPOR) and unmargined regimes. FRTB-CVA (BCBS 325) defines the CVA sensitivity framework and stress scenarios.

#### 1.4 EMIR / Dodd-Frank Margin Rules
- **Relevance**: Initial margin and variation margin for OTC commodity derivatives. Defines the holding period (MPOR ≥ 10 days for bilateral, 5 days for cleared) used in volatility scaling.

---

### 2. Derivative Pricing & Risk References

#### 2.1 Options on Commodity Futures — Black (1976)
- **Document**: Fischer Black, "The pricing of commodity contracts", *Journal of Financial Economics*, 1976.
- **Relevance**: Foundation for European option pricing on futures. Gives closed-form delta, gamma, vega, theta for commodity options. Required for computing the Greeks used in COE/POE sensitivity grids.

#### 2.2 Commodity Swap Valuation
- **Reference**: Hull, *Options, Futures and Other Derivatives*, 11th ed., Chapter 35; Clewlow & Strickland, *Energy Derivatives*.
- **Relevance**: Fixed-for-floating commodity swaps are valued as a strip of forward contracts. Delta (price sensitivity) is the PV01 of the forward strip. Each fixing date contributes an additive forward delta.

#### 2.3 Spread Options (Crack spreads, Spark spreads)
- **Reference**: Margrabe (1978) for exchange options; Kirk (1995) approximation for spread options; 2-factor Bachelier for gas/power spreads.
- **Relevance**: Cross-commodity exposure (e.g. gas–power, crude–middle distillates) introduces *joint* delta sensitivities that require the full correlation matrix between underliers.

#### 2.4 Stochastic Commodity Models
| Model | Reference | Relevance |
|---|---|---|
| Schwartz 1-factor | Schwartz (1997) | Mean-reverting spot; simple volatility term structure |
| Schwartz-Smith 2-factor | Schwartz & Smith (2000) | Short-run deviation + long-run equilibrium; used for gas/power |
| Gibson-Schwartz | Gibson & Schwartz (1990) | Spot + convenience yield; crude/refined products |
| Seasonal ARMA + GARCH | Cartea & Figueroa (2005) | Natural gas with seasonality and spikes |
| Multi-factor HJM | Heath-Jarrow-Morton adapted | Forward curve evolution; directly observable |

#### 2.5 Correlation Modelling
- **Reference**: Rebonato & Jäckel (1999) "The most general methodology for constructing a positive semi-definite correlation matrix"; Embrechts, McNeil & Straumann (2002) on copulas for energy markets.
- **Relevance**: The cross-commodity and cross-tenor correlation matrices must be PSD. The project needs both historical estimation and stress-scenario correlation overrides.

---

### 3. Numerical Methods References

#### 3.1 Monte Carlo Simulation
- **Reference**: Glasserman, *Monte Carlo Methods in Financial Engineering* (2003), Chapters 3–4.
- **Relevance**: Path simulation for POE (max expected exposure over the life of the trade). Antithetic variates, control variates, quasi-Monte Carlo (Sobol) for variance reduction.

#### 3.2 Finite Differences & Greeks
- **Reference**: Wilmott, *Paul Wilmott on Quantitative Finance*, Chapter 5–8.
- **Relevance**: Numerical delta/gamma computation via bumping (`ΔP / ΔS`). Central differences for Greeks; automatic differentiation (JAX/autograd) as an alternative.

#### 3.3 Cholesky Decomposition for Correlated Paths
- **Reference**: Press et al., *Numerical Recipes*, Chapter 2.
- **Relevance**: Generating correlated GBM / OU increments from the commodity correlation matrix.

#### 3.4 Exposure Profile Metrics
- **Reference**: Gregory, *Counterparty Credit Risk and Credit Value Adjustment* (2012), Chapters 7–10.
- **Relevance**: Defines Expected Exposure (EE), Potential Future Exposure (PFE), and their relationship to COE/POE. Peak EE vs percentile-based PFE.

---

### 4. Alignment with Existing `isda_simm.py`

| Existing component | COE/POE reuse |
|---|---|
| `COM_BUCKETS` (17 buckets) | Same taxonomy for bucket assignment |
| `COM_RHO` (within-bucket ρ) | Intra-bucket correlation in the sensitivity covariance matrix |
| `COM_GAMMA` (cross-bucket γ) | Cross-bucket correlation in the full covariance matrix |
| `COM_RW` risk weights | Can be repurposed as volatility proxies for scaling |
| `COM_CT` concentration thresholds | Reused to detect concentration regime |
| `PSI` cross-risk-class correlations | IR–Commodity–FX joint covariance for multi-asset trades |
| `ir_delta_margin` / `com_delta_margin` | Delta sensitivities feed directly into COE |

---

## PART II — PYTHON PROJECT OUTLINE

```
coe_poe_model/
├── README.md
├── requirements.txt                  # numpy, scipy, pandas, matplotlib, numba, tqdm
├── config/
│   └── market_params.yaml            # Vol surfaces, correlation overrides, scenario sets
├── data/
│   ├── forward_curves.csv            # Commodity forward curves by tenor & bucket
│   ├── vol_surfaces.csv              # Implied vol surface (strike × maturity)
│   └── hist_prices.csv               # Historical daily prices for correlation estimation
├── isda_simm.py                      # Existing — imported as a module
│
├── core/
│   ├── __init__.py
│   ├── instruments.py                # Trade object definitions
│   ├── market_data.py                # Forward curve, vol surface loaders
│   ├── greeks.py                     # Delta, gamma, vega via Black-76 / numerical bumping
│   ├── correlation.py                # Correlation matrix estimation & stress
│   └── covariance.py                 # Full covariance matrix assembly (SIMM-aligned)
│
├── pricing/
│   ├── __init__.py
│   ├── black76.py                    # European options on futures (gas, oil, power)
│   ├── swap_pricer.py                # Fixed-for-floating commodity swap valuation
│   ├── spread_option.py              # Kirk / Bachelier spread option pricer
│   └── asian_option.py              # Arithmetic Asian options (common in energy)
│
├── exposure/
│   ├── __init__.py
│   ├── coe.py                        # Current Outward Exposure (mark-to-market based)
│   ├── poe.py                        # Potential Outward Exposure (simulation based)
│   ├── sensitivity_grid.py           # Build delta/gamma sensitivity grids per bucket
│   └── scenario_shift.py            # Apply Δ = 1% and larger shifts, compute ΔP
│
├── simulation/
│   ├── __init__.py
│   ├── path_generator.py             # Correlated GBM / OU path simulation
│   ├── monte_carlo.py                # Full MC engine for POE profile
│   └── variance_reduction.py        # Antithetic, control variates, quasi-MC
│
├── portfolio/
│   ├── __init__.py
│   ├── netting.py                    # Netting set aggregation
│   └── aggregator.py                 # Portfolio-level COE/POE with correlation offsets
│
├── reporting/
│   ├── __init__.py
│   ├── exposure_profile.py           # COE/POE term structure plots
│   └── sensitivity_report.py        # Bucketed sensitivity breakdown
│
└── tests/
    ├── test_black76.py
    ├── test_swap_pricer.py
    ├── test_coe.py
    ├── test_poe.py
    └── test_correlation.py
```

### Key class interfaces

```python
# core/instruments.py
@dataclass
class CommoditySwap:
    notional: float          # USD
    fixed_price: float       # USD/MMBtu (gas) or USD/bbl (oil)
    fixing_dates: list       # list of datetime
    commodity_bucket: int    # 0-indexed SIMM bucket
    underlier: str           # e.g. "TTF", "NBP", "Brent", "WTI"
    direction: int           # +1 = pay fixed, -1 = receive fixed

@dataclass
class CommodityOption:
    option_type: str         # 'call' | 'put'
    strike: float
    expiry: float            # years to expiry
    notional: float
    commodity_bucket: int
    underlier: str
    direction: int
    exercise: str            # 'european' | 'asian'

# exposure/coe.py
class COEEngine:
    """
    Current Outward Exposure = max(MtM, 0) for each trade,
    aggregated across netting set with correlation adjustment.
    Also computes sensitivity to price shifts delta = 1%, 2%, 5%, 10%.
    """
    def compute(self, portfolio, market_data) -> dict: ...
    def sensitivity_profile(self, portfolio, market_data, deltas) -> pd.DataFrame: ...

# exposure/poe.py
class POEEngine:
    """
    Potential Outward Exposure via Monte Carlo simulation.
    Returns the exposure profile EE(t), POE(t) = percentile_q(exposure(t))
    for each future time step t.
    """
    def run(self, portfolio, market_data, n_paths, time_steps, confidence=0.95) -> dict: ...
```

---

## PART III — MATHEMATICAL MODELLING & NUMERICAL SIMULATION PLAN

### 3.1 Instrument Pricing

#### Commodity Options — Black-76

For a European call on a futures contract with futures price `F`, strike `K`, time to expiry `T`, risk-free rate `r`, and implied volatility `σ`:

```
d₁ = [ln(F/K) + ½σ²T] / (σ√T)
d₂ = d₁ − σ√T

Call = e^{−rT} [F·N(d₁) − K·N(d₂)]
Put  = e^{−rT} [K·N(−d₂) − F·N(−d₁)]
```

Greeks (analytical):
```
Δ = e^{−rT} N(d₁)                          # delta (call)
Γ = e^{−rT} N'(d₁) / (F·σ·√T)             # gamma
V = F·e^{−rT}·N'(d₁)·√T                   # vega (per unit vol)
```

#### Commodity Swap — Forward Strip

For a swap with fixing dates `{t₁, …, tₙ}` and fixed price `K`:

```
V_swap = Σᵢ DF(tᵢ) · [F(0, tᵢ) − K] · notional · Δtᵢ
```

Delta of the swap to forward `F(0, tᵢ)`:

```
∂V/∂F(0,tᵢ) = DF(tᵢ) · notional · Δtᵢ
```

This gives a vector of forward-level sensitivities, bucketed by tenor.

---

### 3.2 COE Definition and Computation

**Current Outward Exposure (COE)** is the current positive mark-to-market of the netting set:

```
COE = max( Σᵢ MtM(trade_i), 0 )
```

With netting, this is computed at netting-set level. Without netting:

```
COE_gross = Σᵢ max( MtM(trade_i), 0 )
```

#### COE Sensitivity to Price Shift δ

For a price shift `δ` applied to underlier `u` (keeping all other inputs fixed):

```
COE(δ) = max( Σᵢ MtM_i(F_u + δ·F_u), 0 )

ΔCOE(δ) = COE(δ) − COE(0)
```

The full sensitivity profile across `δ ∈ {−10%, −5%, −2%, −1%, +1%, +2%, +5%, +10%}` reveals:
- **Linearity**: how closely COE tracks delta
- **Convexity**: gamma effects from options in the portfolio
- **Asymmetry**: netting effects under directional moves

For a portfolio with analytical delta `Δ_net` and gamma `Γ_net`:

```
ΔCOE(δ) ≈ Δ_net · δ·F + ½ · Γ_net · (δ·F)²   [Taylor expansion]
```

---

### 3.3 POE Definition and Computation

**Potential Outward Exposure (POE)** at confidence level `q` and horizon `t`:

```
POE(t, q) = Quantile_q [ max( V(t), 0 ) ]
```

where `V(t)` is the mark-to-market of the netting set at future time `t`, under the risk-neutral (or real-world) measure.

The **Expected Positive Exposure** (EPE):

```
EPE(t) = E[ max(V(t), 0) ]
```

The **exposure profile** is the term structure `{POE(tᵢ, q)}ᵢ₌₁..ₙ`.

---

### 3.4 Stochastic Process for Forward Curves

#### Multi-Factor Log-Normal Forward Curve Model (HJM-inspired)

For each underlier `u` with forward curve `{F_u(0, tᵢ)}`:

```
dF_u(t, T) / F_u(t, T) = σ_u(t, T) · dW_u(t)
```

where `σ_u(t, T)` is the time-to-maturity-dependent volatility (from the vol surface), and `W_u` is a Brownian motion.

Discrete simulation of the log-forward:

```
ln F_u(t+Δt, T) = ln F_u(t, T) − ½ σ_u²(t,T)·Δt + σ_u(t,T)·√Δt · Z_u(t)
```

where `Z_u(t)` is a standard normal draw.

#### Correlated Multi-Underlier Simulation

For `n` underliers (e.g. TTF gas, NBP gas, Brent, WTI, European Power), the joint simulation uses the **full correlation matrix** `Σ` (n × n):

```
Z = L · ε
```

where `L` is the Cholesky factor `L = chol(Σ)` and `ε ~ N(0, I_n)`.

The full correlation matrix `Σ` is assembled as:

```
Σ[u, v] = ρ_within   if u, v are in the same SIMM bucket (use COM_RHO[b])
Σ[u, v] = γ_{bc}     if u is in bucket b, v is in bucket c (use COM_GAMMA[b,c])
Σ[u, u] = 1
```

**PSD enforcement**: If `Σ` fails the PSD check (e.g. after stress overrides), apply nearest-correlation-matrix projection (Higham 2002).

---

### 3.5 POE via Monte Carlo — Full Algorithm

```
Input:
  - Portfolio of N trades
  - Market data: forward curves F_u(0, T), vol surfaces σ_u(K, T)
  - Correlation matrix Σ (n_underliers × n_underliers)
  - Time grid {t₀=0, t₁, t₂, …, t_M}   (monthly or quarterly steps)
  - n_paths (e.g. 10,000–100,000)
  - Confidence level q (e.g. 95%, 97.5%)

Algorithm:
  1. Cholesky: L = chol(Σ)
  2. For each path p = 1..n_paths:
       a. For each time step tₘ:
            i.  Draw ε ~ N(0, I_n)
            ii. Z = L · ε   (correlated shocks)
            iii. Update forward curves: F_u(tₘ, T) for all u, T
            iv.  Reprice all trades → V_i(tₘ, p)
            v.   V_portfolio(tₘ, p) = Σᵢ V_i(tₘ, p)
            vi.  Exposure(tₘ, p) = max(V_portfolio(tₘ, p), 0)
  3. For each time step tₘ:
       EE(tₘ)  = mean( Exposure(tₘ, ·) )
       POE(tₘ) = quantile_q( Exposure(tₘ, ·) )
       PEAK_POE = max_m POE(tₘ)

Output:
  - Exposure profile arrays EE[t], POE[t]
  - Peak POE scalar
  - Per-underlier contribution (pathwise attribution)
```

---

### 3.6 POE Sensitivity to δ-Shifts

To study how POE varies as a function of price shift `δ`:

```
For δ in {−10%, −5%, −2%, −1%, +1%, +2%, +5%, +10%}:
    Shift all forward curves: F_u → F_u · (1 + δ)   [parallel shift]
    Re-run MC (or reuse paths via pathwise estimator)
    Compute POE(t, q; δ)
    ΔPOE(δ) = POE(t, q; δ) − POE(t, q; 0)
```

This gives the **POE delta ladder** — the analogue of a DV01 ladder but for exposure.

For options-heavy portfolios, `ΔPOE(δ)` will be convex (gamma dominates). For linear swaps, `ΔPOE(δ)` will be approximately linear.

---

### 3.7 Correlation Sensitivity

To quantify the impact of correlation assumptions:

#### Within-bucket correlation stress
```
ρ_stressed = ρ · (1 − α) + α · ρ_floor   # α ∈ [0,1], ρ_floor = 0 (worst-case)
```

#### Cross-bucket correlation stress
```
γ_stressed[b,c] = γ[b,c] · (1 − β) + β · 0   # decorrelation scenario
```

#### Between-instrument correlation (within same underlier, different maturities)
Use the Nelson-Siegel factor structure to parameterise the forward-curve correlation matrix across tenors, consistent with the observed vol term structure.

---

### 3.8 Variance Reduction

| Technique | Implementation | Gain |
|---|---|---|
| Antithetic variates | Use `(Z, −Z)` pairs | ~40–60% variance reduction for near-linear portfolios |
| Control variates | Analytical swap value as control | Works well when swap dominates portfolio |
| Quasi-MC (Sobol) | `scipy.stats.qmc.Sobol` → inverse-normal transform | Order-of-magnitude improvement for smooth payoffs |
| Stratified sampling | Partition paths by underlier quantile | Useful for tail (POE) estimation |

---

### 3.9 Parameter Estimation

#### Volatility
- **Implied vol**: read from exchange-listed options (TTF, Brent, Henry Hub). Use SVI or polynomial interpolation for missing strikes.
- **Historical vol**: 60-day EWMA with λ = 0.94 (RiskMetrics), or GARCH(1,1) for fat-tail adjustment.
- **Vol term structure**: fit exponential decay `σ(τ) = σ_∞ + (σ_0 − σ_∞)·e^{−κτ}` (Samuelson effect).

#### Correlation
- **Realised correlation**: compute from 1-year rolling daily returns. Use DCC-GARCH for time-varying correlation.
- **Shrinkage**: Ledoit-Wolf shrinkage toward a structured target (e.g. constant-correlation model) to stabilise the matrix when the number of instruments is large.
- **SIMM-alignment**: wherever possible, use the `COM_GAMMA` values as prior; deviate only for within-bucket intra-maturity correlations not captured by SIMM.

#### Stress Scenarios
| Scenario | Description |
|---|---|
| Gas supply shock | TTF/NBP +50%, crude +20%, power +30%, cross-correlations stressed up |
| Oil demand collapse | Brent/WTI −40%, gas −15%, all correlations → 1 (crisis) |
| Refinery margin squeeze | Middle distillates +30%, crude flat → crack spread widens |
| Decorrelation scenario | γ_{bc} → 0 for all cross-bucket pairs; within-bucket ρ unchanged |
| Perfect correlation | All ρ = γ = 1 → maximum diversification penalty |

---

### 3.10 Aggregation with Netting & Margin

Under a **CSA with daily VM**:
```
POE_margined(t) = max( POE_unmargined(t_MPOR) − MTA, 0 )
```

where `MTA` is the Minimum Transfer Amount and `t_MPOR` is the margin period of risk (10 business days for bilateral OTC).

For **portfolio netting**:
```
V_netting_set(t) = Σᵢ V_i(t)   [no flooring at trade level]
Exposure(t) = max( V_netting_set(t), 0 )
```

---

### 3.11 Numerical Implementation Notes

- **Vectorisation**: Represent the portfolio as a matrix `(n_paths × n_time_steps × n_trades)`. Use `numpy` broadcasting throughout; avoid Python loops in the hot path.
- **Numba JIT**: Decorate the inner repricing loop with `@numba.njit` for 10–50× speedup on large path counts.
- **PSD check**: Before each simulation run, verify `np.linalg.eigvalsh(Sigma).min() > 0`. If not, apply `nearestPD(Sigma)` (Higham projection).
- **Memory**: For `n_paths = 100,000`, `n_steps = 36`, `n_trades = 50`, the exposure matrix is `100k × 36 × 50 = 180M` floats = ~1.4 GB. Use `float32` and process in batches.
- **Reproducibility**: Set `np.random.seed()` and store seeds in config for audit trail.

---

### 3.12 Deliverables & Milestones

| Milestone | Module | Output |
|---|---|---|
| M1 — Pricing | `pricing/` | Black-76, swap, spread option pricers with unit tests |
| M2 — Greeks | `core/greeks.py` | Analytical + numerical delta/gamma/vega per instrument |
| M3 — Correlation | `core/correlation.py` | Full Σ assembly; PSD enforcement; stress scenarios |
| M4 — COE Engine | `exposure/coe.py` | COE with netting; δ-sensitivity profile |
| M5 — MC Engine | `simulation/` | Correlated path generator; variance reduction |
| M6 — POE Engine | `exposure/poe.py` | Exposure profile EE(t), POE(t, q) |
| M7 — δ Analysis | `exposure/scenario_shift.py` | ΔCOE(δ), ΔPOE(δ) ladder |
| M8 — Reporting | `reporting/` | Term-structure plots, sensitivity reports, stress tables |

---

*Built to extend `isda_simm.py` — reusing bucket taxonomy, correlation matrices, and concentration parameters from ISDA SIMM v2.8+2506.*
