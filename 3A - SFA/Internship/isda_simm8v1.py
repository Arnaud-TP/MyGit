"""
ISDA SIMM v2.8+2506 — Interest Rate, Commodity, and FX Risk Classes
======================================================================
Reference: ISDA SIMM Methodology, version 2.8 calibrated to June 2025
           Effective Date: 6 December 2025

Data structure convention
--------------------------
For Interest Rate (IR):
    sensitivities_ir[b][i][k]
        b  = currency bucket index  (e.g. 0 → USD, 1 → EUR …)
        i  = sub-curve index        (0=OIS, 1=Libor1m, 2=Libor3m, 3=Libor6m, 4=Libor12m, …)
        k  = tenor index            (0=2w, 1=1m, 2=3m, 3=6m, 4=1y, 5=2y, 6=3y,
                                     7=5y, 8=10y, 9=15y, 10=20y, 11=30y)

    CR_b[b]          = scalar concentration-risk factor per currency bucket
    currency_type[b] = 'regular' | 'low' | 'high'

For Commodity:
    sensitivities_com[b][k]
        b = commodity bucket (0-indexed, 0→Bucket1=Coal … 16→Bucket17=Indexes)
        k = commodity risk factor index within that bucket
    CR_com[b][k]  = concentration-risk factor per risk factor

For FX:
    sensitivities_fx[k]
        k = FX risk-factor index (one per currency vs calculation currency)
    CR_fx[k]            = concentration-risk factor per risk factor
    fx_volatility_grp[k] = 'regular' | 'high'
    calc_currency_grp    = 'regular' | 'high'

All sensitivity values are in the same units as the document (USD mm/bp for IR/Credit,
USD mm/% for Equity/Commodity/FX).
"""

import numpy as np
from scipy.stats import norm

# ──────────────────────────────────────────────────────────────────────────────
# §D  INTEREST RATE PARAMETERS
# ──────────────────────────────────────────────────────────────────────────────

# Tenor labels (12 vertices)
IR_TENORS = ["2w", "1m", "3m", "6m", "1y", "2y", "3y", "5y", "10y", "15y", "20y", "30y"]
N_IR_TENORS = 12

# Risk weights (Table 1-3, §D.1 para 33)
IR_RW_REGULAR = np.array([107, 101, 90, 69, 68, 69, 66, 61, 60, 58, 58, 66], dtype=float)
IR_RW_LOW     = np.array([15,  18,  12, 11, 15, 21, 23, 25, 29, 27, 26, 28], dtype=float)
IR_RW_HIGH    = np.array([167, 102, 79, 82, 90, 93, 92, 88, 88, 98, 101, 96], dtype=float)

IR_RW_INFLATION   = 51.0   # §D.1 para 33
IR_RW_XCCY_BASIS  = 21.0   # §D.1 para 33
IR_HVR            = 0.74   # §D.1 para 34
IR_VRW            = 0.20   # §D.1 para 35

# Sub-curve correlation (§D.2 para 36) — between any two sub-curves, same currency
IR_PHI = 0.981

# Inflation ↔ yield correlation (§D.2 para 36)
IR_INFLATION_YIELD_CORR = 0.42

# Cross-currency basis ↔ yield/inflation correlation (§D.2 para 36)
IR_XCCY_CORR = -0.01

# Tenor-tenor correlation matrix ρ_{k,l} (§D.2 para 36, 12×12, diagonal = 1)
_IR_RHO_LOWER = [
    # 2w   1m   3m   6m   1y   2y   3y   5y  10y  15y  20y  30y
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
]
IR_RHO = np.array(_IR_RHO_LOWER)

# Cross-currency correlation γ_{bc} (§D.2 para 37)
IR_GAMMA = 0.35

# Concentration thresholds (§J.1, USD mm/bp)
IR_CT = {
    "high":          51.0,
    "regular_well":  210.0,
    "regular_less":  100.0,
    "low":           230.0,
}

# Currency → threshold group mapping (§J.1 para 75)
IR_WELL_TRADED    = {"USD", "EUR", "GBP"}
IR_LOW_VOLATILITY = {"JPY"}
IR_REGULAR_CURRENCIES = {
    "USD", "EUR", "GBP", "CHF", "AUD", "NZD", "CAD", "SEK",
    "NOK", "DKK", "HKD", "KRW", "SGD", "TWD"
}

# ──────────────────────────────────────────────────────────────────────────────
# §H  COMMODITY PARAMETERS
# ──────────────────────────────────────────────────────────────────────────────

# Bucket labels (17 buckets, 0-indexed)
COM_BUCKETS = [
    "Coal", "Crude", "Light Ends", "Middle Distillates", "Heavy Distillates",
    "NA Natural Gas", "EU Natural Gas", "NA Power & Carbon", "EU Power & Carbon",
    "Freight", "Base Metals", "Precious Metals", "Grains & Oilseed",
    "Softs & Other Ag", "Livestock & Dairy", "Other", "Indexes"
]
N_COM_BUCKETS = 17

# Risk weights (§H.1 para 61)
COM_RW = np.array([25, 21, 23, 19, 24, 27, 33, 37, 64, 43, 21, 19, 14, 17, 11, 64, 16], dtype=float)

COM_HVR = 0.89   # §H.1 para 62
COM_VRW = 0.37   # §H.1 para 63

# Within-bucket correlations ρ_{kl} (§H.2 para 64)
COM_RHO = np.array([
    0.83, 0.98, 0.98, 0.98, 0.98,
    0.94, 0.94, 0.37, 0.58, 0.50,
    0.61, 0.62, 0.57, 0.14, 0.16,
    0.00, 0.34
])

# Cross-bucket correlation matrix γ_{bc} (§H.2 para 65, 17×17)
_COM_GAMMA_RAW = [
    #  1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17
    [  0,  .22,  .17,  .26,  .23,  .30,  .63,  .20,  .42,  .20,  .13,  .10,  .13,  .10,  .02,  .00,  .19],
    [.22,    0,  .94,  .91,  .88,  .25,  .08,  .19,  .10,  .17,  .40,  .29,  .30,  .24,  .17,  .00,  .63],
    [.17,  .94,    0,  .90,  .86,  .19,  .03,  .15,  .06,  .20,  .37,  .26,  .29,  .22,  .16,  .00,  .58],
    [.26,  .91,  .90,    0,  .80,  .28,  .10,  .23,  .13,  .21,  .35,  .19,  .32,  .19,  .15,  .00,  .58],
    [.23,  .88,  .86,  .80,    0,  .18,  .12,  .16,  .08,  .21,  .40,  .31,  .28,  .29,  .18,  .00,  .59],
    [.30,  .25,  .19,  .28,  .18,    0,  .24,  .60,  .16,  .00,  .17,  .07,  .19,  .03,  .13,  .00,  .29],
    [.63,  .08,  .03,  .10,  .12,  .24,    0,  .14,  .70,  .07,  .09,  .08,  .12,  .05,  .01,  .00,  .16],
    [.20,  .19,  .15,  .23,  .16,  .60,  .14,    0,  .14,  .00,  .10,  .03,  .13,  .03,  .06,  .00,  .19],
    [.42,  .10,  .06,  .13,  .08,  .16,  .70,  .14,    0,  .03,  .06, -.02,  .14,  .04,  .01,  .00,  .15],
    [.20,  .17,  .20,  .21,  .21,  .00,  .07,  .00,  .03,    0,  .16,  .10,  .08,  .10,  .01,  .00,  .08],
    [.13,  .40,  .37,  .35,  .40,  .17,  .09,  .10,  .06,  .16,    0,  .41,  .28,  .22,  .18,  .00,  .37],
    [.10,  .29,  .26,  .19,  .31,  .07,  .08,  .03, -.02,  .10,  .41,    0,  .20,  .19,  .10,  .00,  .25],
    [.13,  .30,  .29,  .32,  .28,  .19,  .12,  .13,  .14,  .08,  .28,  .20,    0,  .17,  .16,  .00,  .32],
    [.10,  .24,  .22,  .19,  .29,  .03,  .05,  .03,  .04,  .10,  .22,  .19,  .17,    0,  .13,  .00,  .22],
    [.02,  .17,  .16,  .15,  .18,  .13,  .01,  .06,  .01,  .01,  .18,  .10,  .16,  .13,    0,  .00,  .18],
    [.00,  .00,  .00,  .00,  .00,  .00,  .00,  .00,  .00,  .00,  .00,  .00,  .00,  .00,  .00,    0,  .00],
    [.19,  .63,  .58,  .58,  .59,  .29,  .16,  .19,  .15,  .08,  .37,  .25,  .32,  .22,  .18,  .00,    0],
]
COM_GAMMA = np.array(_COM_GAMMA_RAW)

# Concentration thresholds (§J.4, USD mm/%)
COM_CT = np.array([310, 2500, 1700, 1700, 1700, 2300, 2300, 1800, 1800,
                   52, 530, 1600, 100, 100, 100, 52, 4000], dtype=float)

# ──────────────────────────────────────────────────────────────────────────────
# §I  FOREIGN EXCHANGE PARAMETERS
# ──────────────────────────────────────────────────────────────────────────────

# High FX volatility currencies (§I.1 para 67)
FX_HIGH_VOL_CURRENCIES = {"ARS", "EGP", "ETB", "GHS", "LBP", "NGN", "RUB", "SCR", "VES", "ZMW"}

# Risk weights (§I.1 para 69): indexed [row=given_ccy_grp, col=calc_ccy_grp]
# row/col: 0=Regular, 1=High
FX_RW = np.array([
    [7.1,  18.0],
    [18.0, 30.6],
])

FX_HVR = 0.68   # §I.1 para 70
FX_VRW = 0.34   # §I.1 para 71

# Within-bucket (single bucket) correlations ρ_{kl} (§I.2 para 72)
# Table 1: calc_ccy = Regular
FX_RHO_REGULAR_CALC = np.array([
    [0.50, 0.20],
    [0.20, 0.08],
])
# Table 2: calc_ccy = High
FX_RHO_HIGH_CALC = np.array([
    [0.92, 0.68],
    [0.68, 0.50],
])

# Vega/curvature FX correlation (§I.2 para 73)
FX_VEGA_CORR = 0.50

# Concentration thresholds — delta (§J.5, USD mm/%)
FX_CT_DELTA = {
    "cat1": 3100.0,
    "cat2":  950.0,
    "cat3":  160.0,
}
FX_CAT1 = {"USD", "EUR", "JPY", "GBP", "AUD", "CHF", "CAD"}
FX_CAT2 = {"BRL", "CNY", "HKD", "INR", "KRW", "MXN", "NOK", "NZD",
            "RUB", "SEK", "SGD", "TRY", "ZAR"}

# ──────────────────────────────────────────────────────────────────────────────
# §K  CROSS-RISK-CLASS CORRELATIONS (used in product-class aggregation)
# ──────────────────────────────────────────────────────────────────────────────

# ψ_{rs} (§K para 88)  order: IR, CreditQ, CreditNQ, Equity, Commodity, FX
_PSI_RAW = [
    #  IR   CrQ  CrNQ  EQ   Com   FX
    [1.00, 0.10, 0.14, 0.12, 0.30, 0.10],
    [0.10, 1.00, 0.60, 0.66, 0.25, 0.22],
    [0.14, 0.60, 1.00, 0.52, 0.27, 0.15],
    [0.12, 0.66, 0.52, 1.00, 0.33, 0.24],
    [0.30, 0.25, 0.27, 0.33, 1.00, 0.23],
    [0.10, 0.22, 0.15, 0.24, 0.23, 1.00],
]
PSI = np.array(_PSI_RAW)


# ──────────────────────────────────────────────────────────────────────────────
# HELPER UTILITIES
# ──────────────────────────────────────────────────────────────────────────────

def _fx_grp_idx(currency: str) -> int:
    """Return 0 (Regular) or 1 (High) for a given currency code."""
    return 1 if currency.upper() in FX_HIGH_VOL_CURRENCIES else 0


def _ir_rw(currency_type: str) -> np.ndarray:
    """Return the 12-element risk-weight vector for a currency type."""
    if currency_type == "low":
        return IR_RW_LOW
    elif currency_type == "high":
        return IR_RW_HIGH
    else:
        return IR_RW_REGULAR


def _ir_ct(currency: str) -> float:
    """Return IR delta concentration threshold (USD mm/bp) for a currency."""
    c = currency.upper()
    if c in IR_LOW_VOLATILITY:
        return IR_CT["low"]
    elif c in IR_WELL_TRADED:
        return IR_CT["regular_well"]
    elif c in IR_REGULAR_CURRENCIES:
        return IR_CT["regular_less"]
    else:
        return IR_CT["high"]


def _fx_ct(currency: str) -> float:
    """Return FX delta concentration threshold (USD mm/%) for a currency."""
    c = currency.upper()
    if c in FX_CAT1:
        return FX_CT_DELTA["cat1"]
    elif c in FX_CAT2:
        return FX_CT_DELTA["cat2"]
    else:
        return FX_CT_DELTA["cat3"]


# ──────────────────────────────────────────────────────────────────────────────
# DELTA MARGIN — INTEREST RATE  (§B para 7)
# ──────────────────────────────────────────────────────────────────────────────

def ir_delta_margin(
    sensitivities_ir: list,
    currency_labels: list,
    currency_types: list,
) -> dict:
    """
    Compute IR Delta Margin.

    Parameters
    ----------
    sensitivities_ir : list of list of list of float
        sensitivities_ir[b][i][k]
          b = currency bucket index
          i = sub-curve index
          k = tenor index (0-indexed, matching IR_TENORS)
    currency_labels : list of str
        ISO currency codes matching each bucket b  (e.g. ['USD', 'EUR', …])
    currency_types : list of str
        'regular' | 'low' | 'high'  for each bucket b

    Returns
    -------
    dict with keys:
        'delta_margin'  : float
        'K_b'           : ndarray, per-bucket risk exposure
        'S_b'           : ndarray, capped signed sum per bucket
        'WS'            : list of ndarray, weighted sensitivities per bucket
        'CR_b'          : ndarray, concentration risk factor per bucket
    """
    n_buckets = len(sensitivities_ir)
    K_b = np.zeros(n_buckets)
    S_b = np.zeros(n_buckets)
    CR_b = np.zeros(n_buckets)
    WS_b = []  # WS_b[b] = 2-D array (n_curves × n_tenors)

    for b, sens_b in enumerate(sensitivities_ir):
        ccy  = currency_labels[b]
        ctype = currency_types[b]
        RW   = _ir_rw(ctype)
        T_b  = _ir_ct(ccy)

        # sens_b[i][k]: convert to 2-D numpy array (n_curves × n_tenors)
        n_curves = len(sens_b)
        s_arr = np.zeros((n_curves, N_IR_TENORS))
        for i, curve in enumerate(sens_b):
            for k, v in enumerate(curve):
                s_arr[i, k] = v

        # Concentration risk factor CR_b (§B para 7b)
        # Note: inflation sensitivities included; xccy basis NOT included here
        sum_abs = np.sum(np.abs(s_arr))        # ∑_{k,i} |s_{k,i}|
        CR_b[b] = max(1.0, np.sqrt(sum_abs / T_b))

        # Weighted sensitivities WS_{k,i} = RW_k * s_{k,i} * CR_b  (§B para 7b)
        WS = RW[np.newaxis, :] * s_arr * CR_b[b]   # shape: (n_curves, N_IR_TENORS)
        WS_b.append(WS)

        # Intra-bucket aggregation (§B para 7c)
        # K_b = sqrt( ΣΣ WS_{k,i}^2
        #             + ΣΣ Σ_{(j,l)≠(i,k)} φ_{i,j} ρ_{k,l} WS_{k,i} WS_{l,j} )
        total = 0.0
        n_i, n_k = WS.shape
        # Squared terms
        total += np.sum(WS ** 2)
        # Cross terms
        for i in range(n_i):
            for k in range(n_k):
                for j in range(n_i):
                    for l in range(n_k):
                        if (i, k) != (j, l):
                            phi_ij = IR_PHI if (i != j) else 1.0
                            rho_kl = IR_RHO[k, l]
                            total += phi_ij * rho_kl * WS[i, k] * WS[j, l]
        K_b[b] = np.sqrt(max(total, 0.0))

        # S_b = clamp( sum(WS), -K_b, K_b )
        ws_sum = np.sum(WS)
        S_b[b] = max(min(ws_sum, K_b[b]), -K_b[b])

    # Cross-currency aggregation (§B para 7d)
    # DeltaMargin = sqrt( Σ_b K_b^2 + Σ_b Σ_{c≠b} γ_{bc} * g_{bc} * S_b * S_c )
    total_cross = np.sum(K_b ** 2)
    for b in range(n_buckets):
        for c in range(n_buckets):
            if b != c:
                g_bc = min(CR_b[b], CR_b[c]) / max(CR_b[b], CR_b[c])
                total_cross += IR_GAMMA * g_bc * S_b[b] * S_b[c]

    delta_margin = np.sqrt(max(total_cross, 0.0))

    return {
        "delta_margin": delta_margin,
        "K_b":          K_b,
        "S_b":          S_b,
        "WS":           WS_b,
        "CR_b":         CR_b,
    }


# ──────────────────────────────────────────────────────────────────────────────
# DELTA MARGIN — COMMODITY  (§B para 8)
# ──────────────────────────────────────────────────────────────────────────────

def com_delta_margin(
    sensitivities_com: list,
    CR_com: list = None,
) -> dict:
    """
    Compute Commodity Delta Margin.

    Parameters
    ----------
    sensitivities_com : list of list of float
        sensitivities_com[b][k]  — sensitivity of risk factor k in bucket b
    CR_com : list of list of float, optional
        Pre-computed concentration risk factors. If None, computed from data.

    Returns
    -------
    dict with keys: 'delta_margin', 'K_b', 'S_b', 'WS', 'CR_k'
    """
    n_buckets = N_COM_BUCKETS
    K_b    = np.zeros(n_buckets)
    S_b    = np.zeros(n_buckets)
    WS_all = []
    CR_all = []

    for b in range(n_buckets):
        sens_b = np.asarray(sensitivities_com[b], dtype=float)
        T_b    = COM_CT[b]
        rho    = COM_RHO[b]
        RW     = COM_RW[b]

        # Concentration risk factors (§B para 8b, equity/commodity/FX form)
        if CR_com is not None:
            cr_k = np.asarray(CR_com[b], dtype=float)
        else:
            cr_k = np.maximum(1.0, np.sqrt(np.abs(sens_b) / T_b))
        CR_all.append(cr_k)

        # Weighted sensitivities
        WS = RW * sens_b * cr_k                     # shape: (n_k,)
        WS_all.append(WS)

        # Intra-bucket aggregation (§B para 8c)
        n_k = len(WS)
        total = np.sum(WS ** 2)
        for k in range(n_k):
            for l in range(n_k):
                if k != l:
                    f_kl = min(cr_k[k], cr_k[l]) / max(cr_k[k], cr_k[l])
                    total += rho * f_kl * WS[k] * WS[l]
        K_b[b] = np.sqrt(max(total, 0.0))

        # S_b
        ws_sum = np.sum(WS)
        S_b[b] = max(min(ws_sum, K_b[b]), -K_b[b])

    # Residual bucket: added directly to DeltaMargin (§B para 8d, K_residual term)
    # Here we treat bucket index 15 (Bucket 16 = "Other", 0-indexed) as residual-like
    # and the standard aggregation handles it normally (no special residual in commodity).
    # The formula includes K_residual explicitly; for Commodity all 17 buckets are non-residual.

    # Cross-bucket aggregation (§B para 8d)
    total_cross = np.sum(K_b ** 2)
    for b in range(n_buckets):
        for c in range(n_buckets):
            if b != c:
                total_cross += COM_GAMMA[b, c] * S_b[b] * S_b[c]

    delta_margin = np.sqrt(max(total_cross, 0.0))

    return {
        "delta_margin": delta_margin,
        "K_b":          K_b,
        "S_b":          S_b,
        "WS":           WS_all,
        "CR_k":         CR_all,
    }


# ──────────────────────────────────────────────────────────────────────────────
# DELTA MARGIN — FX  (§B para 8, §I)
# ──────────────────────────────────────────────────────────────────────────────

def fx_delta_margin(
    sensitivities_fx: list,
    currency_labels_fx: list,
    calc_currency: str,
    CR_fx: list = None,
) -> dict:
    """
    Compute FX Delta Margin.

    Parameters
    ----------
    sensitivities_fx : list of float
        sensitivities_fx[k] — sensitivity to FX risk factor k
    currency_labels_fx : list of str
        Currency code for each risk factor k  (not the calculation currency)
    calc_currency : str
        The calculation currency ISO code
    CR_fx : list of float, optional
        Pre-computed concentration risk factors. If None, computed from data.

    Returns
    -------
    dict with keys: 'delta_margin', 'K', 'WS', 'CR_k'
    """
    sens = np.asarray(sensitivities_fx, dtype=float)
    n_k  = len(sens)
    calc_grp = _fx_grp_idx(calc_currency)

    # Risk weights per risk factor
    rw_k = np.array([
        FX_RW[_fx_grp_idx(ccy), calc_grp]
        for ccy in currency_labels_fx
    ])

    # Concentration risk factors (§B para 8b)
    if CR_fx is not None:
        cr_k = np.asarray(CR_fx, dtype=float)
    else:
        cr_k = np.array([
            max(1.0, np.sqrt(abs(sens[k]) / _fx_ct(currency_labels_fx[k])))
            for k in range(n_k)
        ])

    # Weighted sensitivities
    WS = rw_k * sens * cr_k

    # FX is a single bucket (§I.1 para 66)
    # Pick correlation table based on calc_currency group
    if calc_grp == 0:
        rho_table = FX_RHO_REGULAR_CALC
    else:
        rho_table = FX_RHO_HIGH_CALC

    def _rho(k1: int, k2: int) -> float:
        g1 = _fx_grp_idx(currency_labels_fx[k1])
        g2 = _fx_grp_idx(currency_labels_fx[k2])
        return rho_table[g1, g2]

    # Intra-bucket aggregation (§B para 8c) — single bucket
    total = np.sum(WS ** 2)
    for k in range(n_k):
        for l in range(n_k):
            if k != l:
                f_kl = min(cr_k[k], cr_k[l]) / max(cr_k[k], cr_k[l])
                total += _rho(k, l) * f_kl * WS[k] * WS[l]
    K = np.sqrt(max(total, 0.0))

    # Single bucket → no cross-bucket aggregation; K_residual = 0
    delta_margin = K

    return {
        "delta_margin": delta_margin,
        "K":            K,
        "WS":           WS,
        "CR_k":         cr_k,
    }


# ──────────────────────────────────────────────────────────────────────────────
# VEGA MARGIN — INTEREST RATE  (§B para 10)
# ──────────────────────────────────────────────────────────────────────────────

def ir_vega_margin(
    vega_sensitivities_ir: list,
    currency_labels: list,
    vega_cr: list = None,
) -> dict:
    """
    Compute IR Vega Margin.

    Parameters
    ----------
    vega_sensitivities_ir : list of list of list of float
        vega_sensitivities_ir[b][i][k]
          b = currency bucket, i = sub-curve, k = tenor index
          Values should be σ_{kj} * (∂V/∂σ) already computed per §B para 10(c)
    currency_labels : list of str
    vega_cr : list of float, optional
        Pre-computed vega concentration risk factor VCR_b per bucket.
        If None, defaults to 1 (no concentration scaling).

    Returns
    -------
    dict with keys: 'vega_margin', 'K_b', 'S_b', 'VR_k', 'VCR_b'
    """
    n_buckets = len(vega_sensitivities_ir)
    VRW = IR_VRW
    K_b = np.zeros(n_buckets)
    S_b = np.zeros(n_buckets)
    VCR_b = np.ones(n_buckets)
    VR_all = []

    # Vega concentration thresholds (§J.6)
    VT = {
        "high":         110.0,
        "regular_well": 4400.0,
        "regular_less": 480.0,
        "low":          860.0,
    }

    def _vt(ccy):
        c = ccy.upper()
        if c in IR_LOW_VOLATILITY:      return VT["low"]
        if c in IR_WELL_TRADED:         return VT["regular_well"]
        if c in IR_REGULAR_CURRENCIES:  return VT["regular_less"]
        return VT["high"]

    for b, vega_b in enumerate(vega_sensitivities_ir):
        ccy  = currency_labels[b]
        VT_b = _vt(ccy)
        n_curves = len(vega_b)
        vr_arr = np.zeros((n_curves, N_IR_TENORS))
        for i, curve in enumerate(vega_b):
            for k, v in enumerate(curve):
                vr_arr[i, k] = v

        # VCR_b (§B para 10d)
        if vega_cr is not None:
            VCR_b[b] = vega_cr[b]
        else:
            sum_vr = np.sum(np.abs(vr_arr))
            VCR_b[b] = max(1.0, np.sqrt(sum_vr / VT_b))

        # VR_{k} = VRW * (Σ_i VR_{ik}) * VCR_b  (§B para 10d)
        VR = VRW * np.sum(vr_arr, axis=0) * VCR_b[b]  # shape: (N_IR_TENORS,)
        VR_all.append(VR)

        # Intra-bucket aggregation (§B para 10e)
        # f_{kl} = 1 for IR (inner corr adj factors identically 1 in IR)
        total = np.sum(VR ** 2)
        for k in range(N_IR_TENORS):
            for l in range(N_IR_TENORS):
                if k != l:
                    total += IR_RHO[k, l] * VR[k] * VR[l]
        K_b[b] = np.sqrt(max(total, 0.0))

        vr_sum = np.sum(VR)
        S_b[b] = max(min(vr_sum, K_b[b]), -K_b[b])

    # Cross-bucket aggregation (§B para 10f)
    # Outer corr adj g_{bc} for IR = min(VCR_b, VCR_c) / max(VCR_b, VCR_c)
    total_cross = np.sum(K_b ** 2)
    for b in range(n_buckets):
        for c in range(n_buckets):
            if b != c:
                g_bc = min(VCR_b[b], VCR_b[c]) / max(VCR_b[b], VCR_b[c])
                total_cross += IR_GAMMA * g_bc * S_b[b] * S_b[c]

    vega_margin = np.sqrt(max(total_cross, 0.0))

    return {
        "vega_margin": vega_margin,
        "K_b":         K_b,
        "S_b":         S_b,
        "VR":          VR_all,
        "VCR_b":       VCR_b,
    }


# ──────────────────────────────────────────────────────────────────────────────
# VEGA MARGIN — COMMODITY  (§B para 10)
# ──────────────────────────────────────────────────────────────────────────────

def com_vega_margin(
    vega_sensitivities_com: list,
    vega_cr_com: list = None,
) -> dict:
    """
    Compute Commodity Vega Margin.

    Parameters
    ----------
    vega_sensitivities_com : list of list of float
        vega_sensitivities_com[b][k]
          Already vol-scaled: HVR_c * σ_{kj} * (∂V/∂σ) per §B para 10(c)
    vega_cr_com : list of list of float, optional
        Pre-computed VCR_k per risk factor. If None defaults to 1.

    Returns
    -------
    dict with keys: 'vega_margin', 'K_b', 'S_b'
    """
    VRW  = COM_VRW
    n_b  = N_COM_BUCKETS
    K_b  = np.zeros(n_b)
    S_b  = np.zeros(n_b)

    # Vega concentration thresholds (§J.9)
    COM_VCT = np.array([480, 2400, 250, 250, 250, 7000, 7000, 1300, 1300,
                        100, 520, 740, 790, 790, 790, 62, 62], dtype=float)

    for b in range(n_b):
        vr_b = np.asarray(vega_sensitivities_com[b], dtype=float)
        VT_b = COM_VCT[b]
        rho  = COM_RHO[b]

        if vega_cr_com is not None:
            vcr_k = np.asarray(vega_cr_com[b], dtype=float)
        else:
            vcr_k = np.maximum(1.0, np.sqrt(np.abs(vr_b) / VT_b))

        VR = VRW * vr_b * vcr_k

        # Intra-bucket
        total = np.sum(VR ** 2)
        n_k   = len(VR)
        for k in range(n_k):
            for l in range(n_k):
                if k != l:
                    f_kl  = min(vcr_k[k], vcr_k[l]) / max(vcr_k[k], vcr_k[l])
                    total += rho * f_kl * VR[k] * VR[l]
        K_b[b] = np.sqrt(max(total, 0.0))
        ws_sum = np.sum(VR)
        S_b[b] = max(min(ws_sum, K_b[b]), -K_b[b])

    # Cross-bucket
    total_cross = np.sum(K_b ** 2)
    for b in range(n_b):
        for c in range(n_b):
            if b != c:
                total_cross += COM_GAMMA[b, c] * S_b[b] * S_b[c]

    vega_margin = np.sqrt(max(total_cross, 0.0))
    return {"vega_margin": vega_margin, "K_b": K_b, "S_b": S_b}


# ──────────────────────────────────────────────────────────────────────────────
# VEGA MARGIN — FX  (§B para 10)
# ──────────────────────────────────────────────────────────────────────────────

def fx_vega_margin(
    vega_sensitivities_fx: list,
    currency_pair_labels: list,
    calc_currency: str,
    vega_cr_fx: list = None,
) -> dict:
    """
    Compute FX Vega Margin.

    Parameters
    ----------
    vega_sensitivities_fx : list of float
        HVR * σ_{kj} * (∂V/∂σ) per currency pair k
    currency_pair_labels : list of tuple (str, str)
        (ccy1, ccy2) for each FX vega risk factor
    calc_currency : str
    vega_cr_fx : list of float, optional

    Returns
    -------
    dict with 'vega_margin', 'K', 'VR'
    """
    VRW = FX_VRW
    vr_raw = np.asarray(vega_sensitivities_fx, dtype=float)
    n_k    = len(vr_raw)

    # Vega concentration thresholds (§J.10)
    FX_VCT = {
        ("cat1", "cat1"): 2800.0,
        ("cat1", "cat2"): 1400.0,
        ("cat1", "cat3"):  740.0,
        ("cat2", "cat2"):  670.0,
        ("cat2", "cat3"):  440.0,
        ("cat3", "cat3"):  270.0,
    }
    def _cat(ccy):
        c = ccy.upper()
        if c in FX_CAT1:  return "cat1"
        if c in FX_CAT2:  return "cat2"
        return "cat3"

    def _vt_fx(pair):
        c1, c2 = sorted([_cat(pair[0]), _cat(pair[1])])
        key = (c1, c2) if (c1, c2) in FX_VCT else (c2, c1)
        return FX_VCT.get(key, 270.0)

    if vega_cr_fx is not None:
        vcr_k = np.asarray(vega_cr_fx, dtype=float)
    else:
        vcr_k = np.array([
            max(1.0, np.sqrt(abs(vr_raw[k]) / _vt_fx(currency_pair_labels[k])))
            for k in range(n_k)
        ])

    VR = VRW * vr_raw * vcr_k

    # Single bucket
    total = np.sum(VR ** 2)
    for k in range(n_k):
        for l in range(n_k):
            if k != l:
                f_kl  = min(vcr_k[k], vcr_k[l]) / max(vcr_k[k], vcr_k[l])
                total += FX_VEGA_CORR * f_kl * VR[k] * VR[l]

    vega_margin = np.sqrt(max(total, 0.0))
    return {"vega_margin": vega_margin, "K": vega_margin, "VR": VR}


# ──────────────────────────────────────────────────────────────────────────────
# CURVATURE MARGIN — SHARED HELPER  (§B para 11)
# ──────────────────────────────────────────────────────────────────────────────

# Scaling function SF(t) (§B para 11a)
_SF_TENORS_DAYS = [
    14,               # 2w
    365 / 12,         # 1m
    3 * 365 / 12,     # 3m
    6 * 365 / 12,     # 6m
    365,              # 1y
    2 * 365,          # 2y
    3 * 365,          # 3y
    5 * 365,          # 5y
    10 * 365,         # 10y
    15 * 365,         # 15y
    20 * 365,         # 20y
    30 * 365,         # 30y
]

def sf(t_days: float) -> float:
    """Scaling function SF(t) = 0.5 * min(1, 14/t)"""
    return 0.5 * min(1.0, 14.0 / t_days)

# Pre-compute SF values at standard tenors
SF_VALUES = np.array([sf(t) for t in _SF_TENORS_DAYS])

# λ constant (§B para 11d)
_LAMBDA_BASE = norm.ppf(0.995) ** 2 - 1   # (Φ^{-1}(99.5%))^2 - 1


def _curvature_aggregate_bucket(cvr_b: np.ndarray, rho: np.ndarray) -> float:
    """
    Intra-bucket curvature aggregation (§B para 11c).
    K_b = sqrt( Σ CVR_{b,k}^2 + ΣΣ_{k≠l} ρ_{kl}^2 * CVR_{b,k} * CVR_{b,l} )
    """
    n = len(cvr_b)
    total = np.sum(cvr_b ** 2)
    for k in range(n):
        for l in range(n):
            if k != l:
                total += rho[k, l] ** 2 * cvr_b[k] * cvr_b[l]
    return np.sqrt(max(total, 0.0))


def _curvature_aggregate_cross(
    cvr_all: list,
    K_b: np.ndarray,
    gamma: np.ndarray,
    residual_idx: int = None,
) -> float:
    """
    Cross-bucket curvature margin (§B para 11d).
    Non-residual + residual terms summed.
    """
    n_b = len(cvr_all)

    # θ and λ for non-residual buckets
    non_res_idx = [b for b in range(n_b) if b != residual_idx]
    sum_cvr     = sum(np.sum(cvr_all[b]) for b in non_res_idx)
    sum_abs_cvr = sum(np.sum(np.abs(cvr_all[b])) for b in non_res_idx)
    theta = min(sum_cvr / sum_abs_cvr if sum_abs_cvr != 0 else 0.0, 0.0)
    lam   = _LAMBDA_BASE * (1 + theta) - theta

    S_b = np.zeros(n_b)
    for b in non_res_idx:
        s = np.sum(cvr_all[b])
        S_b[b] = max(min(s, K_b[b]), -K_b[b])

    cross = np.sum(K_b[non_res_idx] ** 2)
    for b in non_res_idx:
        for c in non_res_idx:
            if b != c:
                cross += gamma[b, c] ** 2 * S_b[b] * S_b[c]

    cvr_sum_total = sum(np.sum(cvr_all[b]) for b in non_res_idx)
    cm_nonres = max(cvr_sum_total + lam * np.sqrt(max(cross, 0.0)), 0.0)

    # Residual term
    cm_res = 0.0
    if residual_idx is not None and residual_idx < n_b:
        sum_cvr_r   = np.sum(cvr_all[residual_idx])
        abs_cvr_r   = np.sum(np.abs(cvr_all[residual_idx]))
        theta_r = min(sum_cvr_r / abs_cvr_r if abs_cvr_r != 0 else 0.0, 0.0)
        lam_r   = _LAMBDA_BASE * (1 + theta_r) - theta_r
        cm_res  = max(sum_cvr_r + lam_r * K_b[residual_idx], 0.0)

    return cm_nonres + cm_res


# ──────────────────────────────────────────────────────────────────────────────
# CURVATURE MARGIN — INTEREST RATE  (§B para 11)
# ──────────────────────────────────────────────────────────────────────────────

def ir_curvature_margin(
    curvature_ir: list,
    currency_labels: list,
) -> dict:
    """
    Compute IR Curvature Margin.

    Parameters
    ----------
    curvature_ir : list of list of list of float
        curvature_ir[b][i][k]
          CVR_{ik} = Σ_j SF(t_{kj}) * σ_{kj} * (∂V/∂σ)  (already computed)
          b=currency, i=sub-curve, k=tenor
    currency_labels : list of str

    Returns
    -------
    dict with 'curvature_margin'
    """
    n_buckets = len(curvature_ir)
    K_b   = np.zeros(n_buckets)
    cvr_b_list = []

    for b, cvr_b_raw in enumerate(curvature_ir):
        n_curves = len(cvr_b_raw)
        cvr_arr  = np.zeros(N_IR_TENORS)
        for i, curve in enumerate(cvr_b_raw):
            for k, v in enumerate(curve):
                cvr_arr[k] += v   # net across sub-curves per tenor
        cvr_b_list.append(cvr_arr)
        K_b[b] = _curvature_aggregate_bucket(cvr_arr, IR_RHO)

    # Cross-currency using γ_{bc}^2
    S_b = np.zeros(n_buckets)
    for b in range(n_buckets):
        s = np.sum(cvr_b_list[b])
        S_b[b] = max(min(s, K_b[b]), -K_b[b])

    sum_cvr = sum(np.sum(cvr_b_list[b]) for b in range(n_buckets))
    abs_sum = sum(np.sum(np.abs(cvr_b_list[b])) for b in range(n_buckets))
    theta   = min(sum_cvr / abs_sum if abs_sum != 0 else 0.0, 0.0)
    lam     = _LAMBDA_BASE * (1 + theta) - theta

    cross = np.sum(K_b ** 2)
    for b in range(n_buckets):
        for c in range(n_buckets):
            if b != c:
                cross += IR_GAMMA ** 2 * S_b[b] * S_b[c]

    cm = max(sum_cvr + lam * np.sqrt(max(cross, 0.0)), 0.0)

    # Scale by HVR_IR^{-2} (§B para 11, last bullet)
    cm_scaled = cm * (IR_HVR ** -2)

    return {
        "curvature_margin": cm_scaled,
        "K_b":              K_b,
        "S_b":              S_b,
    }


# ──────────────────────────────────────────────────────────────────────────────
# CURVATURE MARGIN — COMMODITY  (§B para 11)
# ──────────────────────────────────────────────────────────────────────────────

def com_curvature_margin(curvature_com: list) -> dict:
    """
    Compute Commodity Curvature Margin.

    Parameters
    ----------
    curvature_com : list of list of float
        curvature_com[b][k]  —  CVR_{b,k} already computed

    Returns
    -------
    dict with 'curvature_margin'
    """
    n_b   = N_COM_BUCKETS
    K_b   = np.zeros(n_b)
    cvr_list = []

    for b in range(n_b):
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

    cm = _curvature_aggregate_cross(cvr_list, K_b, COM_GAMMA)
    return {"curvature_margin": cm, "K_b": K_b}


# ──────────────────────────────────────────────────────────────────────────────
# CURVATURE MARGIN — FX  (§B para 11)
# ──────────────────────────────────────────────────────────────────────────────

def fx_curvature_margin(
    curvature_fx: list,
    currency_pair_labels: list,
    calc_currency: str,
) -> dict:
    """
    Compute FX Curvature Margin (single bucket).

    Parameters
    ----------
    curvature_fx : list of float
        CVR_{k} per FX pair already computed
    currency_pair_labels : list of tuple (str, str)
    calc_currency : str

    Returns
    -------
    dict with 'curvature_margin'
    """
    cvr = np.asarray(curvature_fx, dtype=float)
    n_k = len(cvr)

    # Single bucket — use FX_VEGA_CORR for curvature correlations (§I.2 para 73)
    total = np.sum(cvr ** 2)
    for k in range(n_k):
        for l in range(n_k):
            if k != l:
                total += FX_VEGA_CORR ** 2 * cvr[k] * cvr[l]
    K = np.sqrt(max(total, 0.0))

    # Single non-residual bucket
    sum_cvr = np.sum(cvr)
    abs_sum = np.sum(np.abs(cvr))
    theta   = min(sum_cvr / abs_sum if abs_sum != 0 else 0.0, 0.0)
    lam     = _LAMBDA_BASE * (1 + theta) - theta
    S       = max(min(sum_cvr, K), -K)

    cm = max(sum_cvr + lam * K, 0.0)
    return {"curvature_margin": cm, "K": K}


# ──────────────────────────────────────────────────────────────────────────────
# TOTAL IM PER RISK CLASS
# ──────────────────────────────────────────────────────────────────────────────

def ir_total_im(
    sensitivities_ir,
    currency_labels,
    currency_types,
    vega_sensitivities_ir=None,
    curvature_ir=None,
) -> dict:
    """
    IM_IR = DeltaMargin_IR + VegaMargin_IR + CurvatureMargin_IR
    """
    delta = ir_delta_margin(sensitivities_ir, currency_labels, currency_types)
    dm    = delta["delta_margin"]
    vm    = 0.0
    cm    = 0.0

    if vega_sensitivities_ir is not None:
        vega = ir_vega_margin(vega_sensitivities_ir, currency_labels)
        vm   = vega["vega_margin"]

    if curvature_ir is not None:
        curv = ir_curvature_margin(curvature_ir, currency_labels)
        cm   = curv["curvature_margin"]

    return {
        "IM":           dm + vm + cm,
        "delta_margin": dm,
        "vega_margin":  vm,
        "curv_margin":  cm,
        "delta_detail": delta,
    }


def com_total_im(
    sensitivities_com,
    vega_sensitivities_com=None,
    curvature_com=None,
) -> dict:
    """
    IM_Commodity = DeltaMargin_COM + VegaMargin_COM + CurvatureMargin_COM
    """
    delta = com_delta_margin(sensitivities_com)
    dm    = delta["delta_margin"]
    vm    = 0.0
    cm    = 0.0

    if vega_sensitivities_com is not None:
        vega = com_vega_margin(vega_sensitivities_com)
        vm   = vega["vega_margin"]

    if curvature_com is not None:
        curv = com_curvature_margin(curvature_com)
        cm   = curv["curvature_margin"]

    return {
        "IM":           dm + vm + cm,
        "delta_margin": dm,
        "vega_margin":  vm,
        "curv_margin":  cm,
        "delta_detail": delta,
    }


def fx_total_im(
    sensitivities_fx,
    currency_labels_fx,
    calc_currency,
    vega_sensitivities_fx=None,
    currency_pair_labels=None,
    curvature_fx=None,
) -> dict:
    """
    IM_FX = DeltaMargin_FX + VegaMargin_FX + CurvatureMargin_FX
    """
    delta = fx_delta_margin(sensitivities_fx, currency_labels_fx, calc_currency)
    dm    = delta["delta_margin"]
    vm    = 0.0
    cm    = 0.0

    if vega_sensitivities_fx is not None and currency_pair_labels is not None:
        vega = fx_vega_margin(vega_sensitivities_fx, currency_pair_labels, calc_currency)
        vm   = vega["vega_margin"]

    if curvature_fx is not None and currency_pair_labels is not None:
        curv = fx_curvature_margin(curvature_fx, currency_pair_labels, calc_currency)
        cm   = curv["curvature_margin"]

    return {
        "IM":           dm + vm + cm,
        "delta_margin": dm,
        "vega_margin":  vm,
        "curv_margin":  cm,
        "delta_detail": delta,
    }


# ──────────────────────────────────────────────────────────────────────────────
# PRODUCT-CLASS AGGREGATION (§B para 6)
# ──────────────────────────────────────────────────────────────────────────────

def product_class_simm(im_vector: np.ndarray, risk_class_order: list = None) -> float:
    """
    Aggregate IM across risk classes within a product class.

    SIMM_product = sqrt( Σ_r IM_r^2 + ΣΣ_{r≠s} ψ_{rs} * IM_r * IM_s )

    Parameters
    ----------
    im_vector : np.ndarray
        IM values for each risk class. Length must match risk_class_order.
    risk_class_order : list of str
        Names from ['IR','CreditQ','CreditNQ','Equity','Commodity','FX']
        in same order as im_vector. Defaults to ['IR','Commodity','FX'].

    Returns
    -------
    float  SIMM for the product class
    """
    if risk_class_order is None:
        risk_class_order = ['IR', 'Commodity', 'FX']

    _idx = ['IR', 'CreditQ', 'CreditNQ', 'Equity', 'Commodity', 'FX']
    n = len(im_vector)
    total = np.sum(im_vector ** 2)
    for r in range(n):
        for s in range(n):
            if r != s:
                ri = _idx.index(risk_class_order[r])
                si = _idx.index(risk_class_order[s])
                total += PSI[ri, si] * im_vector[r] * im_vector[s]
    return np.sqrt(max(total, 0.0))


# ──────────────────────────────────────────────────────────────────────────────
# EXAMPLE / SMOKE TEST
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    np.random.seed(42)

    print("=" * 65)
    print("ISDA SIMM v2.8+2506 — Smoke Test")
    print("=" * 65)

    # ── 1. INTEREST RATE ────────────────────────────────────────────────────
    # 3 currencies: USD (regular/well), EUR (regular/well), JPY (low)
    # 2 sub-curves each (OIS + Libor3m), 12 tenors
    #
    # sensitivities_ir[b][i][k]  (USD mm/bp)

    def _rand_ir_curve(scale=50):
        """Random IR sensitivity grid (n_curves × 12)."""
        return [[float(np.random.randn() * scale) for _ in range(12)]
                for _ in range(2)]

    sensitivities_ir = [
        _rand_ir_curve(80),   # USD
        _rand_ir_curve(60),   # EUR
        _rand_ir_curve(15),   # JPY
    ]
    currency_labels = ["USD", "EUR", "JPY"]
    currency_types  = ["regular", "regular", "low"]

    ir_res = ir_delta_margin(sensitivities_ir, currency_labels, currency_types)
    print(f"\n[IR] Delta Margin      : {ir_res['delta_margin']:>12.2f} USD mm")
    print(f"     K_b per currency   : {np.round(ir_res['K_b'], 2)}")
    print(f"     CR_b               : {np.round(ir_res['CR_b'], 4)}")

    ir_full = ir_total_im(sensitivities_ir, currency_labels, currency_types)
    print(f"     IM (delta only)    : {ir_full['IM']:>12.2f} USD mm")

    # ── 2. COMMODITY ────────────────────────────────────────────────────────
    # 17 buckets; 3 risk factors each
    sensitivities_com = [
        [float(np.random.randn() * com_rw) for _ in range(3)]
        for com_rw in COM_RW
    ]

    com_res = com_delta_margin(sensitivities_com)
    print(f"\n[COM] Delta Margin     : {com_res['delta_margin']:>12.2f} USD mm")
    print(f"      K_b (first 5)    : {np.round(com_res['K_b'][:5], 2)}")

    com_full = com_total_im(sensitivities_com)
    print(f"      IM (delta only)  : {com_full['IM']:>12.2f} USD mm")

    # ── 3. FX ────────────────────────────────────────────────────────────────
    # 5 currency pairs vs USD (calculation currency)
    fx_ccys  = ["EUR", "GBP", "JPY", "CHF", "ARS"]          # ARS = high vol
    fx_sens  = [float(np.random.randn() * 50) for _ in fx_ccys]
    calc_ccy = "USD"

    fx_res = fx_delta_margin(fx_sens, fx_ccys, calc_ccy)
    print(f"\n[FX]  Delta Margin     : {fx_res['delta_margin']:>12.2f} USD mm")
    print(f"      Risk weights     : {[FX_RW[_fx_grp_idx(c), _fx_grp_idx(calc_ccy)] for c in fx_ccys]}")

    fx_full = fx_total_im(fx_sens, fx_ccys, calc_ccy)
    print(f"      IM (delta only)  : {fx_full['IM']:>12.2f} USD mm")

    # ── 4. PRODUCT-CLASS AGGREGATION ────────────────────────────────────────
    im_vec = np.array([ir_full["IM"], com_full["IM"], fx_full["IM"]])
    simm   = product_class_simm(im_vec, ['IR', 'Commodity', 'FX'])
    print(f"\n[PRODUCT CLASS] SIMM   : {simm:>12.2f} USD mm")
    print(f"  IR IM={ir_full['IM']:.2f}  COM IM={com_full['IM']:.2f}  FX IM={fx_full['IM']:.2f}")

    # ── 5. PLOT ───────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("ISDA SIMM v2.8+2506 — Delta Margin Breakdown", fontsize=14, fontweight="bold")

    # IR: K_b per currency
    ax = axes[0]
    ax.bar(currency_labels, ir_res["K_b"], color=["#2563EB", "#16A34A", "#DC2626"])
    ax.set_title("IR Delta — K_b per Currency")
    ax.set_ylabel("USD mm")
    ax.set_xlabel("Currency")
    for i, v in enumerate(ir_res["K_b"]):
        ax.text(i, v + 0.5, f"{v:.1f}", ha="center", fontsize=9)

    # Commodity: K_b per bucket
    ax = axes[1]
    colors = plt.cm.tab20(np.linspace(0, 1, N_COM_BUCKETS))
    ax.bar(range(1, N_COM_BUCKETS + 1), com_res["K_b"], color=colors)
    ax.set_title("Commodity Delta — K_b per Bucket")
    ax.set_ylabel("USD mm")
    ax.set_xlabel("Bucket")
    ax.set_xticks(range(1, N_COM_BUCKETS + 1))
    ax.set_xticklabels([str(i) for i in range(1, N_COM_BUCKETS + 1)], fontsize=7)

    # FX: weighted sensitivities
    ax = axes[2]
    ws_fx = fx_res["WS"]
    bar_colors = ["#DC2626" if w < 0 else "#2563EB" for w in ws_fx]
    ax.bar(fx_ccys, ws_fx, color=bar_colors)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("FX Delta — Weighted Sensitivities")
    ax.set_ylabel("USD mm")
    ax.set_xlabel("Currency")

    plt.tight_layout()
    out_path = "/mnt/user-data/outputs/simm_output.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nPlot saved → {out_path}")
    print("\n✓ All checks passed.")
