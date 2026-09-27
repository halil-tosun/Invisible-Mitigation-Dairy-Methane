"""
15_supplementary_text_values.py -- Verifies numeric values reported
directly in the manuscript's running text (Results Sec. 3.2), which are
not presented as a standalone table or figure:

  (a) The naive-additive vs. interaction-corrected comparison for
      Lever B: applying the Kebreab et al. (2022) equation to the
      unmodified BAU diet (NDF = 34.1%) versus the Lever-A-optimized
      diet (NDF = 33.67%) at the reference 3-NOP dose.
  (b) The standardized-regression tornado-sensitivity coefficients
      ranking which uncertain parameters most influence Lever B's
      $/ton CO2e estimate (regression-based sensitivity analysis on
      the existing Monte Carlo draws).

Requires: 03_lever_b_3nop.py, 07_monte_carlo.py

Produces: no files (verification-only; prints results to stdout)
"""
import numpy as np
import pandas as pd
import _paths as p

# ================= (a) Naive-additive vs. interaction-corrected =================
lever_b = pd.read_csv(p.OUTPUT / "LeverB_3NOP_results.csv")

naive = lever_b.query(
    "context == 'BAU diet (highest NDF)' and cost_source == 'DSM-linked cost' "
    "and carbon_price_scenario == 'mid'").iloc[0]
corrected = lever_b.query(
    "context == 'Lever-A-optimized diet (NFC-constrained)' and cost_source == 'DSM-linked cost' "
    "and carbon_price_scenario == 'mid'").iloc[0]

print("=" * 70)
print("(a) Lever B: naive-additive vs. interaction-corrected")
print("=" * 70)
print(f"Naive (BAU diet, NDF=34.1%):              "
      f"{naive['pct_ch4_intensity_change']:.2f}% CH4 change, ${naive['net_dollar_per_ton_co2e']:.2f}/ton")
print(f"Interaction-corrected (Lever-A-opt diet):  "
      f"{corrected['pct_ch4_intensity_change']:.2f}% CH4 change, ${corrected['net_dollar_per_ton_co2e']:.2f}/ton")

assert round(naive["pct_ch4_intensity_change"], 2) == -32.13
assert round(corrected["pct_ch4_intensity_change"], 2) == -32.44
assert round(naive["net_dollar_per_ton_co2e"], 2) == 63.44
assert round(corrected["net_dollar_per_ton_co2e"], 2) == 62.79
print("VERIFIED: matches manuscript Results Sec. 3.2 "
      "(-32.13% naive vs. -32.44% corrected; $63.44/ton vs. $62.79/ton).")

# ================= (b) Tornado sensitivity coefficients =================
d = np.load(p.OUTPUT / "mc_raw_draws.npz")
y = d["dollar_per_ton_B"]
inputs = {
    "Carbon price ($/ton)": d["carbon_price"],
    "3-NOP cost ($/cow/yr)": d["nop_cost"],
    "Kebreab intercept": d["intercept"],
    "Kebreab NDF coefficient": d["ndf_coef"],
}
names = list(inputs.keys())
X = np.column_stack([inputs[n] for n in names])
Xz = (X - X.mean(axis=0)) / X.std(axis=0)
yz = (y - y.mean()) / y.std()
Xz1 = np.column_stack([np.ones(len(yz)), Xz])
coefs, *_ = np.linalg.lstsq(Xz1, yz, rcond=None)
std_coefs = dict(zip(names, coefs[1:]))

print("\n" + "=" * 70)
print("(b) Standardized regression coefficients (Lever B $/ton CO2e)")
print("=" * 70)
for n in sorted(std_coefs, key=lambda k: -abs(std_coefs[k])):
    print(f"  {n}: {std_coefs[n]:+.3f}")

assert round(std_coefs["Carbon price ($/ton)"], 3) == -0.760
assert round(std_coefs["3-NOP cost ($/cow/yr)"], 3) == 0.583
assert round(std_coefs["Kebreab intercept"], 3) == 0.302
assert round(std_coefs["Kebreab NDF coefficient"], 3) == 0.032
print("\nVERIFIED: matches manuscript Results Sec. 3.2 tornado coefficients exactly.")
