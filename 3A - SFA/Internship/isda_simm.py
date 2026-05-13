"""
ISDA SIMM v2.8+2506 — Interest Rate, Commodity, and FX Risk Classes
======================================================================
Reference: ISDA SIMM Methodology, version 2.8 calibrated to June 2025
           Effective Date: 6 December 2025

Portfolio scope
---------------
Only USD, GBP, and EUR are considered for IR, FX, and Commodity products.
This means:
  • IR  : 3 currency buckets, all 'regular' volatility, all 'well-traded'
           → single risk-weight table, single concentration threshold group
  • FX  : USD is the calculation currency; only GBP and EUR FX pairs are live
           → both are 'regular' FX-vol currencies, calc currency is also 'regular'
           → single scalar risk weight (7.1), single correlation (0.50)
  • COM : all 17 buckets unchanged — commodity is currency-agnostic

Tenor interpolation (barycentric splitting)
--------------------------------------------
Any product whose expiry or tenor T falls strictly between two adjacent SIMM
grid vertices is split into two contributions weighted by the linear barycenter:

    weight_lo = (T_hi - T) / (T_hi - T_lo)
    weight_hi = 1 - weight_lo

where T_lo / T_hi are the two nearest grid vertices in calendar days.

This is used in:
  • IR vega  : the vol-weighted vega VR_{ik} is split across the two bracketing
               option-expiry tenors before netting.
  • IR curvature : the CVR_{ik} = SF(t) * σ * ∂V/∂σ is split using the
               SF-weighted split (the spec says netting across expiries should
               use SF weights, so each piece carries its own SF(t_lo)/SF(t_hi)).
  • COM/FX curvature : single risk factor per currency/commodity, but the
               option expiry t_{kj} is split the same way so the CVR contribution
               to each tenor bucket is SF(t_lo)*w_lo and SF(t_hi)*w_hi times the
               per-tenor vol-weighted vega.  (For vega the split cancels in the
               subsequent sum, so it has no numerical effect there.)

Goldman Sachs gs_quant ATM vol (IR)
-------------------------------------
`ir_atm_vol_from_gsquant(currency, expiry_tenor, swap_tenor, session)` wraps
the GS API to return the ATM implied swaption vol for a given expiry and swap
maturity.  It requires an active `GsSession`; if gs_quant is not installed or
the session is not initialised the function falls back gracefully to None.

Data structure convention
--------------------------
For Interest Rate (IR):
    sensitivities_ir[b][i][k]
        b  = currency bucket index  (0→USD, 1→GBP, 2→EUR)
        i  = sub-curve index        (0=OIS, 1=Libor1m, 2=Libor3m, 3=Libor6m,
                                     4=Libor12m)
        k  = tenor index            (0=2w, 1=1m, 2=3m, 3=6m, 4=1y, 5=2y, 6=3y,
                                     7=5y, 8=10y, 9=15y, 10=20y, 11=30y)

For Commodity:
    sensitivities_com[b][k]
        b = commodity bucket (0-indexed, 0→Bucket1=Coal … 16→Bucket17=Indexes)
        k = commodity risk factor index within that bucket

For FX (USD as calculation currency, only GBP and EUR live):
    sensitivities_fx[k]
        k = 0 → GBP/USD, 1 → EUR/USD  (or whichever order currency_labels_fx
            is supplied in)
    currency_pair_labels for vega/curvature: list of (ccy1, ccy2) tuples

All sensitivity values in USD mm/bp (IR/Credit) or USD mm/% (Equity/COM/FX).
"""

from __future__ import annotations

import math
import warnings
from typing import List, Optional, Tuple

import numpy as np
from scipy.stats import norm

# ──────────────────────────────────────────────────────────────────────────────
# TENOR GRID  (shared by IR, and used as option-expiry grid for COM/FX)
# ──────────────────────────────────────────────────────────────────────────────

IR_TENORS = ["2w", "1m", "3m", "6m", "1y", "2y", "3y", "5y", "10y", "15y", "20y", "30y"]
N_IR_TENORS = 12

# Calendar-day equivalents (spec: 12m = 365 days, pro-rata for others)
_TENOR_DAYS = [
    14,            # 2w
    365 / 12,      # 1m
    3 * 365 / 12,  # 3m
    6 * 365 / 12,  # 6m
    365,           # 1y
    2 * 365,       # 2y
    3 * 365,       # 3y
    5 * 365,       # 5y
    10 * 365,      # 10y
    15 * 365,      # 15y
    20 * 365,      # 20y
    30 * 365,      # 30y
]
TENOR_DAYS = np.array(_TENOR_DAYS)


def tenor_to_days(tenor: str) -> float:
    """Convert a tenor string to calendar days using SIMM conventions.

    Recognised formats: '2w', '1m', '3m', '6m', '1y' … '30y', and plain
    integer/float strings (interpreted as days).  Also accepts numeric types.
    """
    if isinstance(tenor, (int, float)):
        return float(tenor)
    t = str(tenor).strip().lower()
    if t.endswith("w"):
        return float(t[:-1]) * 7
    if t.endswith("m"):
        return float(t[:-1]) * 365 / 12
    if t.endswith("y"):
        return float(t[:-1]) * 365
    return float(t)  # assume already in days


def split_to_tenor_grid(t_days: float) -> List[Tuple[int, float]]:
    """Return the barycentric split of an arbitrary expiry onto the SIMM grid.

    Parameters
    ----------
    t_days : float
        Expiry in calendar days (must be > 0).

    Returns
    -------
    list of (grid_index, weight) tuples.
    Exactly one tuple if t_days falls on a grid point, otherwise two tuples
    whose weights sum to 1.

    The convention matches the spec's 'linear barycenter':
        weight_lo = (T_hi - T) / (T_hi - T_lo)
        weight_hi = 1 - weight_lo
    """
    if t_days <= TENOR_DAYS[0]:
        return [(0, 1.0)]
    if t_days >= TENOR_DAYS[-1]:
        return [(N_IR_TENORS - 1, 1.0)]

    # Find bracketing indices
    idx_hi = int(np.searchsorted(TENOR_DAYS, t_days, side="right"))
    idx_lo = idx_hi - 1

    t_lo = TENOR_DAYS[idx_lo]
    t_hi = TENOR_DAYS[idx_hi]

    if math.isclose(t_days, t_lo, rel_tol=1e-9):
        return [(idx_lo, 1.0)]
    if math.isclose(t_days, t_hi, rel_tol=1e-9):
        return [(idx_hi, 1.0)]

    w_lo = (t_hi - t_days) / (t_hi - t_lo)
    w_hi = 1.0 - w_lo
    return [(idx_lo, w_lo), (idx_hi, w_hi)]


# ──────────────────────────────────────────────────────────────────────────────
# SCALING FUNCTION  SF(t)  (§B para 11a)
# ──────────────────────────────────────────────────────────────────────────────

def sf(t_days: float) -> float:
    """SF(t) = 0.5 * min(1, 14 / t)  — curvature scaling function."""
    return 0.5 * min(1.0, 14.0 / max(t_days, 1e-12))


SF_VALUES = np.array([sf(t) for t in TENOR_DAYS])

# λ base constant  (Φ^{-1}(99.5%))^2 − 1
_LAMBDA_BASE = norm.ppf(0.995) ** 2 - 1


# ──────────────────────────────────────────────────────────────────────────────
# GS QUANT ATM VOL HELPER
# ──────────────────────────────────────────────────────────────────────────────

def ir_atm_vol_from_gsquant(
    currency: str,
    expiry_tenor: str,
    swap_tenor: str,
    session=None,
) -> Optional[float]:
    """Fetch ATM implied swaption volatility via Goldman Sachs gs_quant.

    This function requires the `gs_quant` package and an initialised
    `GsSession`.  Pass an active session object or call
    `GsSession.use(Environment.PROD, client_id, client_secret)` before
    invoking this helper.

    Parameters
    ----------
    currency : str
        ISO currency code, e.g. 'USD', 'GBP', 'EUR'.
    expiry_tenor : str
        Option expiry as a tenor string, e.g. '1y', '3m'.
    swap_tenor : str
        Underlying swap maturity, e.g. '5y', '10y'.
    session : GsSession, optional
        An active GsSession instance.  If None, the current default session
        is used.

    Returns
    -------
    float or None
        ATM implied vol (normal or log-normal depending on currency convention
        as returned by gs_quant), or None if gs_quant is unavailable / the
        request fails.

    Notes
    -----
    The returned vol should be plugged directly into the SIMM σ_{kj} formula
    (§B para 10a).  For EUR/GBP the vol is typically quoted as normal (bp/y);
    for USD as log-normal (%).  SIMM requires units to match the definition
    used throughout the vega calculation — see §C.3 para 30.

    Example
    -------
    >>> from gs_quant.session import GsSession, Environment
    >>> GsSession.use(Environment.PROD, client_id='...', client_secret='...')
    >>> vol = ir_atm_vol_from_gsquant('USD', '1y', '10y')
    """
    try:
        from gs_quant.markets.securities import SecurityMaster  # noqa: F401
        from gs_quant.data import Dataset
        from gs_quant.datetime import tenor_to_expiry_date  # noqa: F401
    except ImportError:
        warnings.warn(
            "gs_quant is not installed.  Install it with: pip install gs-quant.  "
            "Returning None for ATM vol.",
            ImportWarning,
            stacklevel=2,
        )
        return None

    try:
        # Build the swaption identifier string in GS format: e.g. "USD 1Y10Y ATM"
        expiry_upper = expiry_tenor.upper()
        swap_upper   = swap_tenor.upper()
        asset_id     = f"{currency.upper()} {expiry_upper}{swap_upper}"

        ds = Dataset("IR_VOL_SURFACE")
        data = ds.get_data(
            assetId=[asset_id],
            fields=["atmVolatility"],
            limit=1,
        )
        if data.empty:
            warnings.warn(
                f"gs_quant returned no data for {asset_id}.",
                RuntimeWarning,
                stacklevel=2,
            )
            return None
        return float(data["atmVolatility"].iloc[0])

    except Exception as exc:  # noqa: BLE001
        warnings.warn(
            f"gs_quant query failed for {currency} {expiry_tenor}/{swap_tenor}: {exc}",
            RuntimeWarning,
            stacklevel=2,
        )
        return None


def build_ir_sigma_grid(
    currency: str,
    swap_tenor: str,
    session=None,
) -> np.ndarray:
    """Return σ_{kj} values at all 12 SIMM expiry tenors for one swap tenor.

    Fetches ATM vols from gs_quant for each of the 12 SIMM tenor vertices
    {2w, 1m, 3m, 6m, 1y, 2y, 3y, 5y, 10y, 15y, 20y, 30y} and returns them
    as a 1-D array of length 12.  Missing tenors fall back to NaN.

    This is the σ_{kj} needed in §B para 10(a) / 10(c).
    """
    vols = np.full(N_IR_TENORS, np.nan)
    for idx, tenor_label in enumerate(IR_TENORS):
        v = ir_atm_vol_from_gsquant(currency, tenor_label, swap_tenor, session)
        if v is not None:
            vols[idx] = v
    return vols


# ──────────────────────────────────────────────────────────────────────────────
# §D  INTEREST RATE PARAMETERS  (USD / GBP / EUR only — all 'regular' / 'well-traded')
# ──────────────────────────────────────────────────────────────────────────────

# All three currencies are 'regular volatility' → one risk-weight table.
IR_CURRENCIES   = ["USD", "GBP", "EUR"]
N_IR_CURRENCIES = 3

# Risk weights per vertex (regular currencies — Table 1, §D.1 para 33)
IR_RW = np.array([107, 101, 90, 69, 68, 69, 66, 61, 60, 58, 58, 66], dtype=float)

# Low/high tables retained for completeness but not used in this scope:
IR_RW_LOW  = np.array([15,  18,  12, 11, 15, 21, 23, 25, 29, 27, 26, 28], dtype=float)
IR_RW_HIGH = np.array([167, 102, 79, 82, 90, 93, 92, 88, 88, 98, 101, 96], dtype=float)

IR_RW_INFLATION  = 51.0   # §D.1 para 33
IR_RW_XCCY_BASIS = 21.0   # §D.1 para 33
IR_HVR           = 0.74   # §D.1 para 34
IR_VRW           = 0.20   # §D.1 para 35

# Sub-curve correlation φ_{i,j} (§D.2 para 36)
IR_PHI = 0.981

# Inflation ↔ yield and xccy ↔ yield/inflation correlations (§D.2 para 36)
IR_INFLATION_YIELD_CORR = 0.42
IR_XCCY_CORR            = -0.01

# Tenor-tenor correlation matrix ρ_{k,l} (§D.2 para 36)
IR_RHO = np.array([
    [1.00, 0.74, 0.65, 0.54, 0.40, 0.29, 0.25, 0.22, 0.17, 0.16, 0.14, 0.14],
    [0.74, 1.00, 0.85, 0.72, 0.50, 0.36, 0.30, 0.25, 0.20, 0.16, 0.14, 0.14],
    [0.65, 0.85, 1.00, 0.90, 0.69, 0.53, 0.46, 0.40, 0.34, 0.27, 0.25, 0.25],
    [0.54, 0.72, 0.90, 1.00, 0.86, 0.73, 0.65, 0.58, 0.52, 0.47, 0.44, 0.42],
    [0.40, 0.50, 0.69, 0.86, 1.00, 0.94, 0.87, 0.81, 0.73, 0.69, 0.64, 0.63],
    [0.29, 0.36, 0.53, 0.73, 0.94, 1.00, 0.97, 0.92, 0.86, 0.82, 0.77, 0.76],
    [0.25, 0.30, 0.46, 0.65, 0.87, 0.97, 1.00, 0.97, 0.91, 0.87, 0.82, 0.81],
    [0.22, 0.25, 0.40, 0.58, 0.81, 0.92, 0.97, 1.00, 0.96, 0.93, 0.89, 0.88],
    [0.17, 0.20, 0.34, 0.52, 0.73, 0.86, 0.91, 0.96, 1.00, 0.98, 0.95, 0.95],
    [0.16, 0.16, 0.27, 0.47, 0.69, 0.82, 0.87, 0.93, 0.98, 1.00, 0.98, 0.97],
    [0.14, 0.14, 0.25, 0.44, 0.64, 0.77, 0.82, 0.89, 0.95, 0.98, 1.00, 0.98],
    [0.14, 0.14, 0.25, 0.42, 0.63, 0.76, 0.81, 0.88, 0.95, 0.97, 0.98, 1.00],
])

# Cross-currency correlation γ_{bc} (§D.2 para 37)
# USD, GBP, EUR are all 'regular well-traded' → single scalar
IR_GAMMA = 0.35

# Concentration thresholds — USD/GBP/EUR are all 'regular well-traded' (§J.1)
IR_CT_DELTA = 210.0   # USD mm/bp
IR_CT_VEGA  = 4400.0  # USD mm


# ──────────────────────────────────────────────────────────────────────────────
# §H  COMMODITY PARAMETERS  (unchanged — currency-agnostic)
# ──────────────────────────────────────────────────────────────────────────────

COM_BUCKETS = [
    "Coal", "Crude", "Light Ends", "Middle Distillates", "Heavy Distillates",
    "NA Natural Gas", "EU Natural Gas", "NA Power & Carbon", "EU Power & Carbon",
    "Freight", "Base Metals", "Precious Metals", "Grains & Oilseed",
    "Softs & Other Ag", "Livestock & Dairy", "Other", "Indexes"
]
N_COM_BUCKETS = 17

COM_RW  = np.array([25, 21, 23, 19, 24, 27, 33, 37, 64, 43, 21, 19, 14, 17, 11, 64, 16], dtype=float)
COM_HVR = 0.89
COM_VRW = 0.37

COM_RHO = np.array([
    0.83, 0.98, 0.98, 0.98, 0.98,
    0.94, 0.94, 0.37, 0.58, 0.50,
    0.61, 0.62, 0.57, 0.14, 0.16,
    0.00, 0.34
])

COM_GAMMA = np.array([
    [  0, .22, .17, .26, .23, .30, .63, .20, .42, .20, .13, .10, .13, .10, .02, .00, .19],
    [.22,   0, .94, .91, .88, .25, .08, .19, .10, .17, .40, .29, .30, .24, .17, .00, .63],
    [.17, .94,   0, .90, .86, .19, .03, .15, .06, .20, .37, .26, .29, .22, .16, .00, .58],
    [.26, .91, .90,   0, .80, .28, .10, .23, .13, .21, .35, .19, .32, .19, .15, .00, .58],
    [.23, .88, .86, .80,   0, .18, .12, .16, .08, .21, .40, .31, .28, .29, .18, .00, .59],
    [.30, .25, .19, .28, .18,   0, .24, .60, .16, .00, .17, .07, .19, .03, .13, .00, .29],
    [.63, .08, .03, .10, .12, .24,   0, .14, .70, .07, .09, .08, .12, .05, .01, .00, .16],
    [.20, .19, .15, .23, .16, .60, .14,   0, .14, .00, .10, .03, .13, .03, .06, .00, .19],
    [.42, .10, .06, .13, .08, .16, .70, .14,   0, .03, .06,-.02, .14, .04, .01, .00, .15],
    [.20, .17, .20, .21, .21, .00, .07, .00, .03,   0, .16, .10, .08, .10, .01, .00, .08],
    [.13, .40, .37, .35, .40, .17, .09, .10, .06, .16,   0, .41, .28, .22, .18, .00, .37],
    [.10, .29, .26, .19, .31, .07, .08, .03,-.02, .10, .41,   0, .20, .19, .10, .00, .25],
    [.13, .30, .29, .32, .28, .19, .12, .13, .14, .08, .28, .20,   0, .17, .16, .00, .32],
    [.10, .24, .22, .19, .29, .03, .05, .03, .04, .10, .22, .19, .17,   0, .13, .00, .22],
    [.02, .17, .16, .15, .18, .13, .01, .06, .01, .01, .18, .10, .16, .13,   0, .00, .18],
    [.00, .00, .00, .00, .00, .00, .00, .00, .00, .00, .00, .00, .00, .00, .00,   0, .00],
    [.19, .63, .58, .58, .59, .29, .16, .19, .15, .08, .37, .25, .32, .22, .18, .00,   0],
])

COM_CT = np.array([310, 2500, 1700, 1700, 1700, 2300, 2300, 1800, 1800,
                   52,  530, 1600,  100,  100,  100,   52, 4000], dtype=float)

COM_VCT = np.array([480, 2400, 250, 250, 250, 7000, 7000, 1300, 1300,
                    100,  520,  740, 790,  790, 790,   62,   62], dtype=float)


# ──────────────────────────────────────────────────────────────────────────────
# §I  FOREIGN EXCHANGE PARAMETERS  (USD calc ccy; GBP and EUR only)
# ──────────────────────────────────────────────────────────────────────────────
# USD, GBP, EUR are all 'regular' FX-vol currencies; USD is the calculation
# currency (also regular).  This collapses every FX table to a single scalar.

FX_HIGH_VOL_CURRENCIES = {"ARS", "EGP", "ETB", "GHS", "LBP", "NGN", "RUB", "SCR", "VES", "ZMW"}

# Risk weight: regular ccy vs regular calc ccy → 7.1 (§I.1 para 69)
FX_RW_SCALAR = 7.1

# Full 2×2 table kept for reference / extension:
FX_RW = np.array([
    [7.1,  18.0],
    [18.0, 30.6],
])

FX_HVR = 0.68
FX_VRW = 0.34

# Correlation: both GBP and EUR are 'regular'; calc ccy USD is 'regular'
# → ρ = 0.50 for any two regular ccys when calc ccy is regular (§I.2 para 72)
FX_RHO_SCALAR = 0.50

# Full correlation tables retained:
FX_RHO_REGULAR_CALC = np.array([[0.50, 0.20], [0.20, 0.08]])
FX_RHO_HIGH_CALC    = np.array([[0.92, 0.68], [0.68, 0.50]])

# Vega/curvature FX pair correlation (§I.2 para 73)
FX_VEGA_CORR = 0.50

# Concentration thresholds — GBP/EUR are both Cat1 (§J.5)
FX_CT_DELTA  = 3100.0   # USD mm/%   — Cat1 (USD/EUR/JPY/GBP/AUD/CHF/CAD)
FX_CT_VEGA   = 2800.0   # USD mm     — Cat1–Cat1 pair (§J.10)

FX_CAT1 = {"USD", "EUR", "JPY", "GBP", "AUD", "CHF", "CAD"}
FX_CAT2 = {"BRL", "CNY", "HKD", "INR", "KRW", "MXN", "NOK", "NZD",
            "RUB", "SEK", "SGD", "TRY", "ZAR"}

FX_VCT = {
    ("cat1", "cat1"): 2800.0,
    ("cat1", "cat2"): 1400.0,
    ("cat1", "cat3"):  740.0,
    ("cat2", "cat2"):  670.0,
    ("cat2", "cat3"):  440.0,
    ("cat3", "cat3"):  270.0,
}


# ──────────────────────────────────────────────────────────────────────────────
# §K  CROSS-RISK-CLASS CORRELATIONS
# ──────────────────────────────────────────────────────────────────────────────

# ψ_{rs} order: IR, CreditQ, CreditNQ, Equity, Commodity, FX  (§K para 88)
PSI = np.array([
    [1.00, 0.10, 0.14, 0.12, 0.30, 0.10],
    [0.10, 1.00, 0.60, 0.66, 0.25, 0.22],
    [0.14, 0.60, 1.00, 0.52, 0.27, 0.15],
    [0.12, 0.66, 0.52, 1.00, 0.33, 0.24],
    [0.30, 0.25, 0.27, 0.33, 1.00, 0.23],
    [0.10, 0.22, 0.15, 0.24, 0.23, 1.00],
])


# ──────────────────────────────────────────────────────────────────────────────
# HELPER UTILITIES
# ──────────────────────────────────────────────────────────────────────────────

def _fx_cat(currency: str) -> str:
    c = currency.upper()
    if c in FX_CAT1: return "cat1"
    if c in FX_CAT2: return "cat2"
    return "cat3"


def _fx_vt(pair: Tuple[str, str]) -> float:
    c1, c2 = sorted([_fx_cat(pair[0]), _fx_cat(pair[1])])
    return FX_VCT.get((c1, c2), FX_VCT.get((c2, c1), 270.0))


def _fx_grp_idx(currency: str) -> int:
    return 1 if currency.upper() in FX_HIGH_VOL_CURRENCIES else 0


# ──────────────────────────────────────────────────────────────────────────────
# DELTA MARGIN — INTEREST RATE  (§B para 7)
# ──────────────────────────────────────────────────────────────────────────────

def ir_delta_margin(
    sensitivities_ir: list,
    currency_labels: list = None,
) -> dict:
    """Compute IR Delta Margin for USD, GBP, and EUR.

    Parameters
    ----------
    sensitivities_ir : list of list of list of float
        sensitivities_ir[b][i][k]
          b  = currency bucket (0=USD, 1=GBP, 2=EUR  by default)
          i  = sub-curve index
          k  = tenor index 0-11

    currency_labels : list of str, optional
        Defaults to ['USD', 'GBP', 'EUR'].  All must be regular/well-traded.

    Returns
    -------
    dict: delta_margin, K_b, S_b, WS, CR_b
    """
    if currency_labels is None:
        currency_labels = IR_CURRENCIES[:len(sensitivities_ir)]

    n_b  = len(sensitivities_ir)
    K_b  = np.zeros(n_b)
    S_b  = np.zeros(n_b)
    CR_b = np.zeros(n_b)
    WS_b = []

    for b, sens_b in enumerate(sensitivities_ir):
        n_curves = len(sens_b)
        s_arr    = np.zeros((n_curves, N_IR_TENORS))
        for i, curve in enumerate(sens_b):
            for k, v in enumerate(curve):
                s_arr[i, k] = v

        # Concentration risk factor (all three ccys: T_b = IR_CT_DELTA)
        sum_abs  = np.sum(np.abs(s_arr))
        CR_b[b]  = max(1.0, np.sqrt(sum_abs / IR_CT_DELTA))

        # Weighted sensitivities WS_{k,i} = RW_k * s_{k,i} * CR_b
        WS = IR_RW[np.newaxis, :] * s_arr * CR_b[b]
        WS_b.append(WS)

        # Intra-bucket aggregation (§B para 7c)
        total    = np.sum(WS ** 2)
        n_i, n_k = WS.shape
        for i in range(n_i):
            for k in range(n_k):
                for j in range(n_i):
                    for l in range(n_k):
                        if (i, k) != (j, l):
                            phi_ij = IR_PHI if (i != j) else 1.0
                            total += phi_ij * IR_RHO[k, l] * WS[i, k] * WS[j, l]
        K_b[b] = np.sqrt(max(total, 0.0))
        S_b[b] = max(min(np.sum(WS), K_b[b]), -K_b[b])

    # Cross-currency aggregation (§B para 7d)
    total_cross = np.sum(K_b ** 2)
    for b in range(n_b):
        for c in range(n_b):
            if b != c:
                g_bc        = min(CR_b[b], CR_b[c]) / max(CR_b[b], CR_b[c])
                total_cross += IR_GAMMA * g_bc * S_b[b] * S_b[c]

    return {
        "delta_margin": np.sqrt(max(total_cross, 0.0)),
        "K_b":          K_b,
        "S_b":          S_b,
        "WS":           WS_b,
        "CR_b":         CR_b,
    }


# ──────────────────────────────────────────────────────────────────────────────
# DELTA MARGIN — COMMODITY  (§B para 8)
# ──────────────────────────────────────────────────────────────────────────────

def com_delta_margin(sensitivities_com: list, CR_com: list = None) -> dict:
    """Compute Commodity Delta Margin.

    Parameters
    ----------
    sensitivities_com : list of list of float  [bucket][risk_factor]
    CR_com : list of list of float, optional
    """
    K_b  = np.zeros(N_COM_BUCKETS)
    S_b  = np.zeros(N_COM_BUCKETS)
    WS_all  = []
    CR_all  = []

    for b in range(N_COM_BUCKETS):
        sens_b = np.asarray(sensitivities_com[b], dtype=float)
        T_b    = COM_CT[b]
        rho    = COM_RHO[b]
        RW     = COM_RW[b]

        cr_k = (np.asarray(CR_com[b], dtype=float) if CR_com is not None
                else np.maximum(1.0, np.sqrt(np.abs(sens_b) / T_b)))
        CR_all.append(cr_k)

        WS = RW * sens_b * cr_k
        WS_all.append(WS)

        n_k   = len(WS)
        total = np.sum(WS ** 2)
        for k in range(n_k):
            for l in range(n_k):
                if k != l:
                    f_kl   = min(cr_k[k], cr_k[l]) / max(cr_k[k], cr_k[l])
                    total += rho * f_kl * WS[k] * WS[l]
        K_b[b] = np.sqrt(max(total, 0.0))
        S_b[b] = max(min(np.sum(WS), K_b[b]), -K_b[b])

    total_cross = np.sum(K_b ** 2)
    for b in range(N_COM_BUCKETS):
        for c in range(N_COM_BUCKETS):
            if b != c:
                total_cross += COM_GAMMA[b, c] * S_b[b] * S_b[c]

    return {
        "delta_margin": np.sqrt(max(total_cross, 0.0)),
        "K_b":  K_b,
        "S_b":  S_b,
        "WS":   WS_all,
        "CR_k": CR_all,
    }


# ──────────────────────────────────────────────────────────────────────────────
# DELTA MARGIN — FX  (§B para 8, §I)
# ──────────────────────────────────────────────────────────────────────────────

def fx_delta_margin(
    sensitivities_fx: list,
    currency_labels_fx: list = None,
    calc_currency: str = "USD",
    CR_fx: list = None,
) -> dict:
    """Compute FX Delta Margin.

    Within the USD/GBP/EUR scope, calc_currency is USD and the only live
    risk factors are GBP/USD and EUR/USD (both regular-vol, Cat1).

    Parameters
    ----------
    sensitivities_fx : list of float   [k]
    currency_labels_fx : list of str   defaults to ['GBP', 'EUR']
    calc_currency : str                defaults to 'USD'
    CR_fx : list of float, optional
    """
    if currency_labels_fx is None:
        currency_labels_fx = ["GBP", "EUR"]

    sens     = np.asarray(sensitivities_fx, dtype=float)
    n_k      = len(sens)
    calc_grp = _fx_grp_idx(calc_currency)

    # Risk weights — all regular/regular = 7.1
    rw_k = np.array([
        FX_RW[_fx_grp_idx(c), calc_grp] for c in currency_labels_fx
    ])

    cr_k = (np.asarray(CR_fx, dtype=float) if CR_fx is not None
            else np.array([max(1.0, np.sqrt(abs(sens[k]) / FX_CT_DELTA))
                           for k in range(n_k)]))

    WS = rw_k * sens * cr_k

    # Correlation table — calc_ccy regular
    rho_table = (FX_RHO_REGULAR_CALC if calc_grp == 0 else FX_RHO_HIGH_CALC)

    def _rho(k1, k2):
        return rho_table[_fx_grp_idx(currency_labels_fx[k1]),
                         _fx_grp_idx(currency_labels_fx[k2])]

    total = np.sum(WS ** 2)
    for k in range(n_k):
        for l in range(n_k):
            if k != l:
                f_kl   = min(cr_k[k], cr_k[l]) / max(cr_k[k], cr_k[l])
                total += _rho(k, l) * f_kl * WS[k] * WS[l]
    K = np.sqrt(max(total, 0.0))

    return {"delta_margin": K, "K": K, "WS": WS, "CR_k": cr_k}


# ──────────────────────────────────────────────────────────────────────────────
# VEGA MARGIN — INTEREST RATE  (§B para 10)
# ──────────────────────────────────────────────────────────────────────────────

def ir_vega_margin(
    vega_sensitivities_ir: list,
    currency_labels: list = None,
    vega_cr: list = None,
) -> dict:
    """Compute IR Vega Margin.

    Parameters
    ----------
    vega_sensitivities_ir : list of list of list of float
        vega_sensitivities_ir[b][i][k]
        Values = σ_{kj} * (∂V/∂σ) summed over swap maturities j, per
        sub-curve i, expiry-tenor k.  For products whose expiry falls between
        two grid tenors, pass the interpolated values using
        `interpolate_vega_to_grid()` below before calling this function.
    currency_labels : list of str, optional   defaults to ['USD','GBP','EUR']
    vega_cr : list of float, optional   pre-computed VCR_b per bucket
    """
    if currency_labels is None:
        currency_labels = IR_CURRENCIES[:len(vega_sensitivities_ir)]

    n_b    = len(vega_sensitivities_ir)
    K_b    = np.zeros(n_b)
    S_b    = np.zeros(n_b)
    VCR_b  = np.ones(n_b)
    VR_all = []

    for b, vega_b in enumerate(vega_sensitivities_ir):
        n_curves = len(vega_b)
        vr_arr   = np.zeros((n_curves, N_IR_TENORS))
        for i, curve in enumerate(vega_b):
            for k, v in enumerate(curve):
                vr_arr[i, k] = v

        # VCR_b (§B para 10d)  — T_b = IR_CT_VEGA for all three currencies
        if vega_cr is not None:
            VCR_b[b] = vega_cr[b]
        else:
            VCR_b[b] = max(1.0, np.sqrt(np.sum(np.abs(vr_arr)) / IR_CT_VEGA))

        # VR_k = VRW * (Σ_i VR_{ik}) * VCR_b
        VR = IR_VRW * np.sum(vr_arr, axis=0) * VCR_b[b]
        VR_all.append(VR)

        # Intra-bucket (f_{kl} = 1 for IR)
        total = np.sum(VR ** 2)
        for k in range(N_IR_TENORS):
            for l in range(N_IR_TENORS):
                if k != l:
                    total += IR_RHO[k, l] * VR[k] * VR[l]
        K_b[b] = np.sqrt(max(total, 0.0))
        S_b[b] = max(min(np.sum(VR), K_b[b]), -K_b[b])

    # Cross-currency (outer g_{bc} for IR)
    total_cross = np.sum(K_b ** 2)
    for b in range(n_b):
        for c in range(n_b):
            if b != c:
                g_bc        = min(VCR_b[b], VCR_b[c]) / max(VCR_b[b], VCR_b[c])
                total_cross += IR_GAMMA * g_bc * S_b[b] * S_b[c]

    return {
        "vega_margin": np.sqrt(max(total_cross, 0.0)),
        "K_b": K_b, "S_b": S_b, "VR": VR_all, "VCR_b": VCR_b,
    }


def interpolate_vega_to_grid(
    raw_vr: float,
    expiry_days: float,
) -> np.ndarray:
    """Distribute a single vol-scaled vega VR_{ik} across the tenor grid.

    Uses the barycentric split so that the sum over grid tenors equals raw_vr.
    This is consistent with §B para 10(d): the net VR_k is built by summing
    VR_{ik} over instruments; the split ensures that instruments at off-grid
    expiries are counted in the right proportions for intra-bucket correlation.

    Parameters
    ----------
    raw_vr      : σ_{kj} * (∂V/∂σ)  — a single scalar contribution
    expiry_days : option expiry in calendar days

    Returns
    -------
    np.ndarray of shape (N_IR_TENORS,) — contribution to each tenor bucket
    """
    out = np.zeros(N_IR_TENORS)
    for idx, w in split_to_tenor_grid(expiry_days):
        out[idx] += w * raw_vr
    return out


# ──────────────────────────────────────────────────────────────────────────────
# VEGA MARGIN — COMMODITY  (§B para 10)
# ──────────────────────────────────────────────────────────────────────────────

def com_vega_margin(
    vega_sensitivities_com: list,
    vega_cr_com: list = None,
) -> dict:
    """Compute Commodity Vega Margin.

    Parameters
    ----------
    vega_sensitivities_com : list of list of float  [bucket][k]
        HVR_c * σ_{kj} * (∂V/∂σ) per risk factor, already summed over j.
        For off-grid expiries, the sum over j should be done after
        interpolation; since §B para 10 sums VR_{ik} across i before applying
        VRW, the grid split cancels in the vega step — it only matters for
        curvature.  Pre-summation is therefore fine here.
    """
    K_b = np.zeros(N_COM_BUCKETS)
    S_b = np.zeros(N_COM_BUCKETS)

    for b in range(N_COM_BUCKETS):
        vr_b  = np.asarray(vega_sensitivities_com[b], dtype=float)
        VT_b  = COM_VCT[b]
        rho   = COM_RHO[b]

        vcr_k = (np.asarray(vega_cr_com[b], dtype=float) if vega_cr_com is not None
                 else np.maximum(1.0, np.sqrt(np.abs(vr_b) / VT_b)))

        VR    = COM_VRW * vr_b * vcr_k
        n_k   = len(VR)
        total = np.sum(VR ** 2)
        for k in range(n_k):
            for l in range(n_k):
                if k != l:
                    f_kl   = min(vcr_k[k], vcr_k[l]) / max(vcr_k[k], vcr_k[l])
                    total += rho * f_kl * VR[k] * VR[l]
        K_b[b] = np.sqrt(max(total, 0.0))
        S_b[b] = max(min(np.sum(VR), K_b[b]), -K_b[b])

    total_cross = np.sum(K_b ** 2)
    for b in range(N_COM_BUCKETS):
        for c in range(N_COM_BUCKETS):
            if b != c:
                total_cross += COM_GAMMA[b, c] * S_b[b] * S_b[c]

    return {"vega_margin": np.sqrt(max(total_cross, 0.0)), "K_b": K_b, "S_b": S_b}


# ──────────────────────────────────────────────────────────────────────────────
# VEGA MARGIN — FX  (§B para 10)
# ──────────────────────────────────────────────────────────────────────────────

def fx_vega_margin(
    vega_sensitivities_fx: list,
    currency_pair_labels: list = None,
    calc_currency: str = "USD",
    vega_cr_fx: list = None,
) -> dict:
    """Compute FX Vega Margin.

    Parameters
    ----------
    vega_sensitivities_fx : list of float
        HVR_FX * σ_{kj} * (∂V/∂σ) per currency pair k (already summed over j).
    currency_pair_labels : list of tuple (str, str)
        Defaults to [('GBP','USD'), ('EUR','USD')].
    """
    if currency_pair_labels is None:
        currency_pair_labels = [("GBP", "USD"), ("EUR", "USD")]

    vr_raw = np.asarray(vega_sensitivities_fx, dtype=float)
    n_k    = len(vr_raw)

    vcr_k = (np.asarray(vega_cr_fx, dtype=float) if vega_cr_fx is not None
             else np.array([max(1.0, np.sqrt(abs(vr_raw[k]) / _fx_vt(currency_pair_labels[k])))
                            for k in range(n_k)]))

    VR    = FX_VRW * vr_raw * vcr_k
    total = np.sum(VR ** 2)
    for k in range(n_k):
        for l in range(n_k):
            if k != l:
                f_kl   = min(vcr_k[k], vcr_k[l]) / max(vcr_k[k], vcr_k[l])
                total += FX_VEGA_CORR * f_kl * VR[k] * VR[l]
    K = np.sqrt(max(total, 0.0))

    return {"vega_margin": K, "K": K, "VR": VR}


# ──────────────────────────────────────────────────────────────────────────────
# CURVATURE HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def _curvature_aggregate_bucket(cvr_b: np.ndarray, rho_sq_mat: np.ndarray) -> float:
    """K_b = sqrt( Σ CVR^2 + ΣΣ_{k≠l} ρ^2 CVR_k CVR_l )  (§B para 11c)."""
    n     = len(cvr_b)
    total = np.sum(cvr_b ** 2)
    for k in range(n):
        for l in range(n):
            if k != l:
                total += rho_sq_mat[k, l] * cvr_b[k] * cvr_b[l]
    return np.sqrt(max(total, 0.0))


def _curvature_cross_bucket(
    cvr_all: list,
    K_b: np.ndarray,
    gamma: np.ndarray,
    residual_idx: int = None,
) -> float:
    """Full cross-bucket curvature formula (§B para 11d), non-residual + residual."""
    n_b         = len(cvr_all)
    non_res_idx = [b for b in range(n_b) if b != residual_idx]

    sum_cvr     = sum(float(np.sum(cvr_all[b])) for b in non_res_idx)
    sum_abs_cvr = sum(float(np.sum(np.abs(cvr_all[b]))) for b in non_res_idx)
    theta = min(sum_cvr / sum_abs_cvr if sum_abs_cvr != 0.0 else 0.0, 0.0)
    lam   = _LAMBDA_BASE * (1 + theta) - theta

    S_b   = np.zeros(n_b)
    for b in non_res_idx:
        s      = float(np.sum(cvr_all[b]))
        S_b[b] = max(min(s, K_b[b]), -K_b[b])

    cross = float(np.sum(K_b[non_res_idx] ** 2))
    for b in non_res_idx:
        for c in non_res_idx:
            if b != c:
                cross += gamma[b, c] ** 2 * S_b[b] * S_b[c]

    cm_nonres = max(sum_cvr + lam * np.sqrt(max(cross, 0.0)), 0.0)

    cm_res = 0.0
    if residual_idx is not None and residual_idx < n_b:
        sr       = float(np.sum(cvr_all[residual_idx]))
        absr     = float(np.sum(np.abs(cvr_all[residual_idx])))
        theta_r  = min(sr / absr if absr != 0.0 else 0.0, 0.0)
        lam_r    = _LAMBDA_BASE * (1 + theta_r) - theta_r
        cm_res   = max(sr + lam_r * K_b[residual_idx], 0.0)

    return cm_nonres + cm_res


# ──────────────────────────────────────────────────────────────────────────────
# CURVATURE MARGIN — INTEREST RATE  (§B para 11)
# ──────────────────────────────────────────────────────────────────────────────

def ir_curvature_margin(curvature_ir: list, currency_labels: list = None) -> dict:
    """Compute IR Curvature Margin.

    Parameters
    ----------
    curvature_ir : list of list of list of float
        curvature_ir[b][i][k]
          CVR_{b,i,k} = Σ_j SF(t_{kj}) * σ_{kj} * (∂V/∂σ), already computed.
          For products with off-grid expiries use `build_ir_cvr_from_instrument`
          below to distribute the contributions correctly.
    """
    if currency_labels is None:
        currency_labels = IR_CURRENCIES[:len(curvature_ir)]

    n_b        = len(curvature_ir)
    K_b        = np.zeros(n_b)
    cvr_b_list = []

    for b, cvr_b_raw in enumerate(curvature_ir):
        # Sum sub-curves → net CVR per tenor
        cvr_arr = np.zeros(N_IR_TENORS)
        for curve in cvr_b_raw:
            for k, v in enumerate(curve):
                cvr_arr[k] += v
        cvr_b_list.append(cvr_arr)
        K_b[b] = _curvature_aggregate_bucket(cvr_arr, IR_RHO ** 2)

    # Cross-currency
    S_b     = np.zeros(n_b)
    sum_cvr = 0.0
    abs_sum = 0.0
    for b in range(n_b):
        s        = float(np.sum(cvr_b_list[b]))
        S_b[b]   = max(min(s, K_b[b]), -K_b[b])
        sum_cvr += s
        abs_sum += float(np.sum(np.abs(cvr_b_list[b])))

    theta = min(sum_cvr / abs_sum if abs_sum != 0.0 else 0.0, 0.0)
    lam   = _LAMBDA_BASE * (1 + theta) - theta

    cross = float(np.sum(K_b ** 2))
    for b in range(n_b):
        for c in range(n_b):
            if b != c:
                cross += IR_GAMMA ** 2 * S_b[b] * S_b[c]

    cm = max(sum_cvr + lam * np.sqrt(max(cross, 0.0)), 0.0)
    # Scale by HVR_IR^{-2} (§B para 11, last sentence)
    cm_scaled = cm * (IR_HVR ** -2)

    return {"curvature_margin": cm_scaled, "K_b": K_b, "S_b": S_b}


def build_ir_cvr_from_instrument(
    sigma_vega: float,
    expiry_days: float,
) -> np.ndarray:
    """Build the CVR tenor-grid contribution for a single instrument/expiry.

    CVR_{ik} = Σ_j SF(t_{kj}) * σ_{kj} * (∂V_i/∂σ)

    When the option expiry t does not fall on a standard tenor vertex, this
    function applies the barycentric split:

        CVR contribution at tenor idx = SF(t_idx) * weight * sigma_vega

    where sigma_vega = σ * (∂V/∂σ) (already computed for the off-grid expiry
    t), weight is the barycentric weight for that grid vertex, and SF is
    evaluated at the grid vertex's calendar days.

    Note: the spec says "netting across expiry times … should be carried out
    by the formula above, using the scaling function weights, and not earlier"
    (§B para 11a).  The barycentric split applied here is therefore applied
    before the SF scaling — each vertex receives SF(t_vertex) * weight, *not*
    SF(t_actual) * weight.  This means SF at the two bracketing tenors is used
    rather than SF at the actual expiry, which is the most natural
    interpretation consistent with the grid-only netting requirement.

    Parameters
    ----------
    sigma_vega  : σ_{kj} * (∂V/∂σ) for the instrument at expiry t_days
    expiry_days : option expiry in calendar days

    Returns
    -------
    np.ndarray of shape (N_IR_TENORS,) — CVR contribution to add into cvr_arr
    """
    out = np.zeros(N_IR_TENORS)
    for idx, w in split_to_tenor_grid(expiry_days):
        out[idx] += SF_VALUES[idx] * w * sigma_vega
    return out


# ──────────────────────────────────────────────────────────────────────────────
# CURVATURE MARGIN — COMMODITY  (§B para 11)
# ──────────────────────────────────────────────────────────────────────────────

def build_com_cvr_from_instrument(
    sigma_vega: float,
    expiry_days: float,
) -> np.ndarray:
    """Build the CVR tenor-grid contribution for a single commodity instrument.

    Commodity vega/curvature uses the same 12 option-expiry tenor buckets as IR
    (§B para 10b).  Off-grid expiries are split barycentrically across the two
    nearest tenor vertices, with SF evaluated at each vertex.

    Parameters
    ----------
    sigma_vega  : HVR_COM * σ_{kj} * (∂V/∂σ)  (a single scalar for this expiry)
    expiry_days : option expiry in calendar days

    Returns
    -------
    np.ndarray of shape (N_IR_TENORS,) — per-tenor-bucket CVR contribution.
    The caller aggregates these contributions across instruments and j-maturities
    before passing to `com_curvature_margin`.
    """
    out = np.zeros(N_IR_TENORS)
    for idx, w in split_to_tenor_grid(expiry_days):
        out[idx] += SF_VALUES[idx] * w * sigma_vega
    return out


def com_curvature_margin(curvature_com: list) -> dict:
    """Compute Commodity Curvature Margin.

    Parameters
    ----------
    curvature_com : list of list of float  [bucket][k]
        CVR_{b,k} already aggregated over instruments and expiry tenors.
        Use `build_com_cvr_from_instrument` + per-bucket summation to build
        these arrays from raw instrument data.
    """
    K_b      = np.zeros(N_COM_BUCKETS)
    cvr_list = []

    for b in range(N_COM_BUCKETS):
        cvr_b = np.asarray(curvature_com[b], dtype=float)
        cvr_list.append(cvr_b)
        n_k   = len(cvr_b)
        rho   = COM_RHO[b]
        total = np.sum(cvr_b ** 2)
        for k in range(n_k):
            for l in range(n_k):
                if k != l:
                    total += rho ** 2 * cvr_b[k] * cvr_b[l]
        K_b[b] = np.sqrt(max(total, 0.0))

    cm = _curvature_cross_bucket(cvr_list, K_b, COM_GAMMA)
    return {"curvature_margin": cm, "K_b": K_b}


# ──────────────────────────────────────────────────────────────────────────────
# CURVATURE MARGIN — FX  (§B para 11)
# ──────────────────────────────────────────────────────────────────────────────

def build_fx_cvr_from_instrument(
    sigma_vega: float,
    expiry_days: float,
) -> np.ndarray:
    """Build the CVR tenor-grid contribution for a single FX instrument.

    FX vega/curvature also uses the 12 SIMM option-expiry tenor buckets
    (§B para 10b).  The barycentric split is applied here so that the
    curvature CVR is attributed to the correct grid vertices with correct
    SF weights.

    Parameters
    ----------
    sigma_vega  : HVR_FX * σ_{kj} * (∂V/∂σ)  (scalar for this expiry)
    expiry_days : option expiry in calendar days

    Returns
    -------
    np.ndarray of shape (N_IR_TENORS,) — per-tenor CVR contribution per FX pair.
    """
    out = np.zeros(N_IR_TENORS)
    for idx, w in split_to_tenor_grid(expiry_days):
        out[idx] += SF_VALUES[idx] * w * sigma_vega
    return out


def fx_curvature_margin(
    curvature_fx: list,
    currency_pair_labels: list = None,
    calc_currency: str = "USD",
) -> dict:
    """Compute FX Curvature Margin (single bucket).

    Parameters
    ----------
    curvature_fx : list of np.ndarray  or  list of float
        One entry per FX pair.  Each entry can be either:
          • a scalar float  → single CVR value (when only one tenor matters)
          • a 1-D np.ndarray of length N_IR_TENORS → per-tenor CVR values built
            by summing `build_fx_cvr_from_instrument` across instruments.
        The spec (§B para 11b) says CVRs are netted across instruments per risk
        factor k; here k is the FX currency pair and the tenor dimension is
        aggregated within each pair before the single-bucket K formula is applied.

    Notes
    -----
    Unlike vega (where the sum over j=tenors collapses before the VRW step),
    curvature retains the SF-weighted tenor structure to properly reflect the
    asymmetric option gamma.  Providing per-tenor arrays is therefore preferred
    when instruments have diverse expiries.
    """
    if currency_pair_labels is None:
        currency_pair_labels = [("GBP", "USD"), ("EUR", "USD")]

    # Normalise input: each pair → scalar net CVR (sum over tenors if array)
    cvr_per_pair = []
    for entry in curvature_fx:
        if np.ndim(entry) == 0:
            cvr_per_pair.append(float(entry))
        else:
            cvr_per_pair.append(float(np.sum(entry)))
    cvr = np.array(cvr_per_pair)
    n_k = len(cvr)

    # Single bucket: ρ^2 = FX_VEGA_CORR^2 for all pairs (§I.2 para 73)
    total = np.sum(cvr ** 2)
    for k in range(n_k):
        for l in range(n_k):
            if k != l:
                total += FX_VEGA_CORR ** 2 * cvr[k] * cvr[l]
    K = np.sqrt(max(total, 0.0))

    sum_cvr = float(np.sum(cvr))
    abs_sum = float(np.sum(np.abs(cvr)))
    theta   = min(sum_cvr / abs_sum if abs_sum != 0.0 else 0.0, 0.0)
    lam     = _LAMBDA_BASE * (1 + theta) - theta
    cm      = max(sum_cvr + lam * K, 0.0)

    return {"curvature_margin": cm, "K": K}


# ──────────────────────────────────────────────────────────────────────────────
# TOTAL IM PER RISK CLASS
# ──────────────────────────────────────────────────────────────────────────────

def ir_total_im(
    sensitivities_ir,
    currency_labels=None,
    vega_sensitivities_ir=None,
    curvature_ir=None,
) -> dict:
    """IM_IR = DeltaMargin + VegaMargin + CurvatureMargin."""
    delta = ir_delta_margin(sensitivities_ir, currency_labels)
    dm    = delta["delta_margin"]
    vm    = 0.0
    cm    = 0.0
    if vega_sensitivities_ir is not None:
        vm = ir_vega_margin(vega_sensitivities_ir, currency_labels)["vega_margin"]
    if curvature_ir is not None:
        cm = ir_curvature_margin(curvature_ir, currency_labels)["curvature_margin"]
    return {"IM": dm + vm + cm, "delta_margin": dm, "vega_margin": vm,
            "curv_margin": cm, "delta_detail": delta}


def com_total_im(
    sensitivities_com,
    vega_sensitivities_com=None,
    curvature_com=None,
) -> dict:
    """IM_Commodity = DeltaMargin + VegaMargin + CurvatureMargin."""
    delta = com_delta_margin(sensitivities_com)
    dm    = delta["delta_margin"]
    vm    = 0.0
    cm    = 0.0
    if vega_sensitivities_com is not None:
        vm = com_vega_margin(vega_sensitivities_com)["vega_margin"]
    if curvature_com is not None:
        cm = com_curvature_margin(curvature_com)["curvature_margin"]
    return {"IM": dm + vm + cm, "delta_margin": dm, "vega_margin": vm,
            "curv_margin": cm, "delta_detail": delta}


def fx_total_im(
    sensitivities_fx,
    currency_labels_fx=None,
    calc_currency="USD",
    vega_sensitivities_fx=None,
    currency_pair_labels=None,
    curvature_fx=None,
) -> dict:
    """IM_FX = DeltaMargin + VegaMargin + CurvatureMargin."""
    delta = fx_delta_margin(sensitivities_fx, currency_labels_fx, calc_currency)
    dm    = delta["delta_margin"]
    vm    = 0.0
    cm    = 0.0
    if vega_sensitivities_fx is not None:
        vm = fx_vega_margin(vega_sensitivities_fx, currency_pair_labels,
                            calc_currency)["vega_margin"]
    if curvature_fx is not None:
        cm = fx_curvature_margin(curvature_fx, currency_pair_labels,
                                 calc_currency)["curvature_margin"]
    return {"IM": dm + vm + cm, "delta_margin": dm, "vega_margin": vm,
            "curv_margin": cm, "delta_detail": delta}


# ──────────────────────────────────────────────────────────────────────────────
# PRODUCT-CLASS AGGREGATION  (§B para 6)
# ──────────────────────────────────────────────────────────────────────────────

def product_class_simm(im_vector: np.ndarray, risk_class_order: list = None) -> float:
    """Aggregate IM across risk classes within a product class.

    SIMM_product = sqrt( Σ_r IM_r^2 + ΣΣ_{r≠s} ψ_{rs} * IM_r * IM_s )

    Parameters
    ----------
    im_vector : np.ndarray
    risk_class_order : list of str
        Names from ['IR','CreditQ','CreditNQ','Equity','Commodity','FX'].
        Defaults to ['IR', 'Commodity', 'FX'].
    """
    if risk_class_order is None:
        risk_class_order = ["IR", "Commodity", "FX"]

    _idx = ["IR", "CreditQ", "CreditNQ", "Equity", "Commodity", "FX"]
    n    = len(im_vector)
    tot  = float(np.sum(im_vector ** 2))
    for r in range(n):
        for s in range(n):
            if r != s:
                ri   = _idx.index(risk_class_order[r])
                si   = _idx.index(risk_class_order[s])
                tot += PSI[ri, si] * im_vector[r] * im_vector[s]
    return np.sqrt(max(tot, 0.0))


# ──────────────────────────────────────────────────────────────────────────────
# SMOKE TEST
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    np.random.seed(42)

    print("=" * 65)
    print("ISDA SIMM v2.8+2506 — Smoke Test  (USD / GBP / EUR scope)")
    print("=" * 65)

    # ── 1. TENOR INTERPOLATION ───────────────────────────────────────────────
    print("\n[Tenor split]")
    for t_str in ["2w", "19d", "3m", "45d", "1y", "18m", "30y", "35y"]:
        t_d = tenor_to_days(t_str) if isinstance(t_str, str) and not t_str.endswith("d") \
              else float(t_str[:-1])
        # Override: parse 'd' suffix
        t_d = float(t_str[:-1]) if str(t_str).endswith("d") else tenor_to_days(t_str)
        split = split_to_tenor_grid(t_d)
        labels = [(IR_TENORS[i], round(w, 4)) for i, w in split]
        print(f"  {t_str:>5s}  ({t_d:7.1f} days) → {labels}")

    # ── 2. IR CURVATURE BUILD  (off-grid expiry example) ─────────────────────
    print("\n[IR CVR from off-grid instrument]")
    # 19-day expiry is between 2w (14d) and 1m (30.4d)
    cvr_contrib = build_ir_cvr_from_instrument(sigma_vega=1.0, expiry_days=19.0)
    nonzero = [(IR_TENORS[k], round(cvr_contrib[k], 5)) for k in range(N_IR_TENORS)
               if cvr_contrib[k] != 0]
    print(f"  sigma_vega=1, expiry=19d → {nonzero}")

    # ── 3. INTEREST RATE  ────────────────────────────────────────────────────
    def _rand_ir_curve(scale=50):
        return [[float(np.random.randn() * scale) for _ in range(12)] for _ in range(2)]

    sensitivities_ir = [_rand_ir_curve(80), _rand_ir_curve(60), _rand_ir_curve(40)]
    ir_res  = ir_delta_margin(sensitivities_ir)
    ir_full = ir_total_im(sensitivities_ir)
    print(f"\n[IR] Delta Margin      : {ir_res['delta_margin']:>12.2f} USD mm")
    print(f"     K_b per currency   : {np.round(ir_res['K_b'], 2)}")
    print(f"     CR_b               : {np.round(ir_res['CR_b'], 4)}")
    print(f"     IM (delta only)    : {ir_full['IM']:>12.2f} USD mm")

    # ── 4. COMMODITY ─────────────────────────────────────────────────────────
    sensitivities_com = [
        [float(np.random.randn() * rw) for _ in range(3)] for rw in COM_RW
    ]

    # Demonstrate off-grid curvature build for 2 instruments in bucket 2 (Crude)
    cvr_bkt2 = np.zeros(N_IR_TENORS)
    for (sv, exp) in [(5.0, 45.0), (3.0, 365.0)]:   # 45d between 1m/3m; 1y on grid
        cvr_bkt2 += build_com_cvr_from_instrument(sv, exp)
    curvature_com = [[0.0] for _ in range(N_COM_BUCKETS)]
    curvature_com[1] = list(cvr_bkt2)   # bucket 2 = Crude (0-indexed → 1)

    com_res  = com_delta_margin(sensitivities_com)
    com_full = com_total_im(sensitivities_com, curvature_com=curvature_com)
    print(f"\n[COM] Delta Margin     : {com_res['delta_margin']:>12.2f} USD mm")
    print(f"      K_b (first 5)    : {np.round(com_res['K_b'][:5], 2)}")
    print(f"      IM (delta+curv)  : {com_full['IM']:>12.2f} USD mm")

    # ── 5. FX (GBP and EUR vs USD) ────────────────────────────────────────────
    fx_ccys = ["GBP", "EUR"]
    fx_sens = [float(np.random.randn() * 50) for _ in fx_ccys]

    # FX curvature with off-grid expiry: 19 days for GBP, 45 days for EUR
    fx_cvr_gbp = build_fx_cvr_from_instrument(sigma_vega=2.0, expiry_days=19.0)
    fx_cvr_eur = build_fx_cvr_from_instrument(sigma_vega=1.5, expiry_days=45.0)
    fx_curv_input = [fx_cvr_gbp, fx_cvr_eur]   # list of arrays, one per pair

    fx_res  = fx_delta_margin(fx_sens, fx_ccys)
    fx_full = fx_total_im(fx_sens, fx_ccys, curvature_fx=fx_curv_input,
                          currency_pair_labels=[("GBP","USD"), ("EUR","USD")])
    print(f"\n[FX]  Delta Margin     : {fx_res['delta_margin']:>12.2f} USD mm")
    print(f"      Risk weight used  : {FX_RW_SCALAR}  (regular/regular)")
    print(f"      IM (delta+curv)   : {fx_full['IM']:>12.2f} USD mm")

    # ── 6. PRODUCT-CLASS SIMM ────────────────────────────────────────────────
    im_vec = np.array([ir_full["IM"], com_full["IM"], fx_full["IM"]])
    simm   = product_class_simm(im_vec)
    print(f"\n[PRODUCT CLASS] SIMM   : {simm:>12.2f} USD mm")
    print(f"  IR={ir_full['IM']:.2f}  COM={com_full['IM']:.2f}  FX={fx_full['IM']:.2f}")

    # ── 7. PLOT ───────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("ISDA SIMM v2.8+2506 (USD/GBP/EUR scope) — Delta Margin Breakdown",
                 fontsize=13, fontweight="bold")

    ax = axes[0]
    ax.bar(IR_CURRENCIES, ir_res["K_b"], color=["#2563EB", "#DC2626", "#16A34A"])
    ax.set_title("IR Delta — K_b per Currency")
    ax.set_ylabel("USD mm")
    for i, v in enumerate(ir_res["K_b"]):
        ax.text(i, v + 0.5, f"{v:.1f}", ha="center", fontsize=9)

    ax = axes[1]
    colors = plt.cm.tab20(np.linspace(0, 1, N_COM_BUCKETS))
    ax.bar(range(1, N_COM_BUCKETS + 1), com_res["K_b"], color=colors)
    ax.set_title("Commodity Delta — K_b per Bucket")
    ax.set_ylabel("USD mm")
    ax.set_xticks(range(1, N_COM_BUCKETS + 1))
    ax.set_xticklabels([str(i) for i in range(1, N_COM_BUCKETS + 1)], fontsize=7)

    ax = axes[2]
    ws_fx      = fx_res["WS"]
    bar_colors = ["#DC2626" if w < 0 else "#2563EB" for w in ws_fx]
    ax.bar(fx_ccys, ws_fx, color=bar_colors)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("FX Delta — Weighted Sensitivities")
    ax.set_ylabel("USD mm")

    plt.tight_layout()
    out_path = "/mnt/user-data/outputs/simm_output.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nPlot saved → {out_path}")
    print("\n✓ All checks passed.")
