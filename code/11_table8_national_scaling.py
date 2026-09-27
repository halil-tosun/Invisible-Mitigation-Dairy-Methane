"""
11_table8_national_scaling.py -- Table 8.

National-scale abatement potential and Tier 1 representation status, by
lever (Lever C at its primary point estimate; Table 5 reports the
alternative higher-effect scenario).

This script performs no new random draws: it loads and formats the
national-scale Monte Carlo results already computed in
07_monte_carlo.py, which continues that script's single random-number-
generator stream (carbon price and biological/economic draws, then
adoption-rate draws, in that order) so that Table 8 is bit-for-bit
consistent with the manuscript's reported figures (Methods Sec. 2.8).

Requires: 07_monte_carlo.py

Produces: output/Table8_national_scaling.csv
"""
import numpy as np
import pandas as pd
import _paths as p

draws = np.load(p.OUTPUT / "mc_raw_draws.npz")

lever_names = {
    "A": "A -- Dietary NDF reduction", "B": "B -- 3-NOP",
    "C": "C -- Rumen-available fat (primary)", "D": "D -- Replacement rate reduction",
}
national_mmt = {code: draws[f"national_mmt_{code}"] for code in "ABCD"}

rows = []
for code in ["A", "B", "C", "D"]:
    lo, hi = p.ADOPTION_RATE_RANGE[code]
    pt = p.ADOPTION_RATE[code]
    mmt = national_mmt[code]
    rows.append(dict(
        lever=lever_names[code],
        adoption_rate_range=f"{pt*100:.0f}% ({lo*100:.0f}-{hi*100:.0f}%)",
        achieved_median_MMT=round(np.median(mmt), 3),
        ui_90_low=round(np.percentile(mmt, 5), 3),
        ui_90_high=round(np.percentile(mmt, 95), 3),
    ))

table8 = pd.DataFrame(rows)
print(table8.to_string(index=False))

national_total_mmt = sum(national_mmt.values())
aggregate_median = np.median(national_total_mmt)
tier1_representable_mmt = np.median(national_mmt["D"])
not_represented_mmt = aggregate_median - tier1_representable_mmt
not_represented_pct = not_represented_mmt / aggregate_median * 100

print(f"\nAggregate (sum of four independently scaled scenarios, median): {aggregate_median:.3f} MMT CO2e/yr")
print(f"Tier 1-representable (Lever D only): {tier1_representable_mmt:.3f} MMT ({100 - not_represented_pct:.1f}%)")
print(f"Not represented (Levers A+B+C): {not_represented_mmt:.3f} MMT ({not_represented_pct:.1f}%)")

# ---- Verification against manuscript Table 8 / Results Sec. 3.4 ----
assert round(aggregate_median, 3) == 4.258, aggregate_median
assert round(not_represented_pct, 1) == 91.4, not_represented_pct
assert round(100 - not_represented_pct, 1) == 8.6
assert round(table8.loc[0, "achieved_median_MMT"], 3) == 0.052   # Lever A
assert round(table8.loc[1, "achieved_median_MMT"], 3) == 2.563 or round(table8.loc[1, "achieved_median_MMT"], 2) == 2.56  # Lever B
assert round(table8.loc[2, "achieved_median_MMT"], 3) == 1.279 or round(table8.loc[2, "achieved_median_MMT"], 2) == 1.28  # Lever C
assert round(table8.loc[3, "achieved_median_MMT"], 3) == 0.364   # Lever D
print("\nVERIFIED: matches manuscript Table 8 and Sec. 3.4 (4.258 MMT total; 91.4% not represented).")

table8.to_csv(p.OUTPUT / "Table8_national_scaling.csv", index=False)
print(f"\nSaved: {p.OUTPUT / 'Table8_national_scaling.csv'}")
