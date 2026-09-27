"""
07_monte_carlo.py -- Table 3 and Table 5.

Monte Carlo uncertainty propagation (10,000 iterations, seed=42) across
the four levers, producing the pooled-distribution farm-level cost-
effectiveness ranking (Table 3) and the Lever C primary-vs-alternative-
higher-effect coefficient sensitivity (Table 5). Also saves raw draws
for Figure 2 and the tornado-sensitivity values reported in Results
Sec. 3.2 (see 13_supplementary_text_values.py).

Distributional choices (Methods Sec. 2.4):
  - Normal, using reported standard errors: Kebreab et al. (2022)
    3-NOP x NDF coefficients (intercept SE=1.2, NDF-coefficient SE=0.167).
  - Triangular (min/mode/max), for parameters reported only as a
    literature range: carbon price, 3-NOP net cost, Lever D emission-
    intensity reduction and heifer-rearing cost, and Lever A ingredient-
    price shock (+/-20%).
  - Carbon price is drawn ONCE per iteration and applied identically to
    all four levers (correct correlation structure: all levers face the
    same market price in a given draw); this pooled triangular
    distribution across three heterogeneous market benchmarks is a
    disclosed simplification (Methods Sec. 2.4; Table 6 provides a
    scenario-conditional point-estimate alternative for Lever C).
  - Lever C's methane-response coefficient is held at its primary point
    estimate (3.77%/point; de Ondarza et al., 2024) in this main
    simulation; the alternative higher-effect coefficient (19.5%/point;
    Hristov et al., 2022) is evaluated separately below (Table 5), not
    pooled into the main distribution.

Requires: 02_lever_a_optimization.py, 03_lever_b_3nop.py,
          04_lever_c_fat.py, 05_lever_d_replacement.py

Produces: output/Table3_macc_comparison.csv
          output/Table5_leverC_sensitivity.csv
          output/mc_raw_draws.npz (raw draws, used by Figure 2 and by
          13_supplementary_text_values.py's tornado-sensitivity check)
"""
import numpy as np
import pandas as pd
import _paths as p
from _calc import FPCM, MILK_REVENUE_USD_PER_DAY  # noqa: F401 (MILK_REVENUE kept for parity)

rng = np.random.default_rng(p.MC_SEED)
N = p.MC_ITERATIONS
DAYS_PER_YEAR = 365

frontier = pd.read_csv(p.OUTPUT / "LeverA_ndf_frontier.csv")
bau = frontier.iloc[(frontier["ndf_floor"] - p.NASEM_MEAN_NDF).abs().idxmin()]
opt = frontier.loc[frontier["ndf_floor"].idxmin()]
lib = pd.read_csv(p.DATA_PROCESSED / "ingredient_library.csv")
cottonseed = lib.loc[lib["ingredient"] == "Whole cottonseed"].iloc[0]

KEBREAB_INTERCEPT_SE = 1.2
KEBREAB_NDF_COEF_SE = 0.167

# ---- Shared draw: carbon price (once per iteration, applied to all levers) ----
carbon_price = rng.triangular(
    p.CARBON_PRICE_LOW_USD_PER_TON, p.CARBON_PRICE_MID_USD_PER_TON,
    np.mean(p.CARBON_PRICE_HIGH_RANGE_USD_PER_TON), N)

# ================= Lever A: dietary NDF reduction =================
abate_ghg_kg_A = bau["ghg_intensity"] - opt["ghg_intensity"]
abate_ton_yr_A = (abate_ghg_kg_A * FPCM * DAYS_PER_YEAR) / 1000.0
cost_delta_base_A = (opt["feed_cost_d"] - bau["feed_cost_d"]) * 365
price_shock = rng.uniform(0.8, 1.2, N)
cost_delta_A = cost_delta_base_A * price_shock
net_cost_A = cost_delta_A - abate_ton_yr_A * carbon_price
dollar_per_ton_A = net_cost_A / abate_ton_yr_A

# ================= Lever B: 3-NOP, on the Lever-A-optimized diet =================
# The main result reported in Table 3 applies the Kebreab et al. (2022)
# equation to the Lever-A-optimized diet (NDF = 33.67% DM), not the
# unmodified BAU ration: Levers B, C, and D share a common baseline (the
# Lever-A-optimized diet), representing each intervention's marginal
# cost-effectiveness when layered on top of an already-reformulated
# ration (Methods Sec. 2.3).
intercept = rng.normal(p.KEBREAB_INTERCEPT, KEBREAB_INTERCEPT_SE, N)
ndf_coef = rng.normal(p.KEBREAB_NDF_COEF, KEBREAB_NDF_COEF_SE, N)
diet_ndf_pct = opt["ndf"] * 100.0
# Dose is fixed at the meta-analysis reference dose (70.5 mg/kg DM), which
# makes the dose term vanish identically; the dose coefficient's sampling
# uncertainty is therefore excluded from this Monte Carlo by construction.
pct_change_B = intercept + ndf_coef * (diet_ndf_pct - p.KEBREAB_NDF_MEAN)
new_ghg_B = opt["ghg_intensity"] * (1.0 + pct_change_B / 100.0)
abate_ton_yr_B = np.clip((opt["ghg_intensity"] - new_ghg_B) * FPCM * DAYS_PER_YEAR / 1000.0, 1e-6, None)
nop_cost = rng.triangular(p.NOP_COST_USD_PER_COW_YEAR[0], np.mean(p.NOP_COST_USD_PER_COW_YEAR),
                            p.NOP_COST_INDEPENDENT_USD_PER_COW_YEAR, N)
net_cost_B = nop_cost - abate_ton_yr_B * carbon_price
dollar_per_ton_B = net_cost_B / abate_ton_yr_B

# ================= Lever C: rumen-available fat, primary estimate =================
baseline_fat_pct_dm = opt["fat"] * 100.0
increment_pct_dm = max(0.0, (p.RAEE_FAT_MAX * 100.0) - baseline_fat_pct_dm)
increment_kg_dm_day = (increment_pct_dm / 100.0) * opt["dmi"]
fat_effect = np.full(N, p.FAT_CH4_REDUCTION_PCT_PER_PCT_DM_MEAN)  # primary point
                                                                     # estimate, held
                                                                     # deterministic
pct_ch4_reduction_C = np.clip(fat_effect * increment_pct_dm, 0, 95)
new_ghg_C = opt["ghg_intensity"] * (1.0 - pct_ch4_reduction_C / 100.0)
abate_ton_yr_C = (opt["ghg_intensity"] - new_ghg_C) * FPCM * DAYS_PER_YEAR / 1000.0
baseline_avg_price = opt["feed_cost_d"] / opt["dmi"]
ingredient_cost_delta_C = increment_kg_dm_day * (cottonseed["price_usd_per_kg_dm"] - baseline_avg_price) * 365
baseline_fat_yield_kg_d = p.MILK * (p.FAT / 100.0)  # noqa: overridden below via module import
fat_yield_loss_kg_d = (p.MILK * (p.FAT / 100.0)) * (p.FAT_MILK_FAT_YIELD_LOSS_PCT / 100.0)
milk_loss_C = fat_yield_loss_kg_d * p.BUTTERFAT_PRICE_USD_PER_KG * 365
gross_cost_C = ingredient_cost_delta_C + milk_loss_C
net_cost_C = gross_cost_C - abate_ton_yr_C * carbon_price
dollar_per_ton_C = net_cost_C / abate_ton_yr_C

# ---- Lever C alternative higher-effect scenario (Table 5), not pooled ----
fat_effect_alt = np.full(N, p.FAT_CH4_REDUCTION_PCT_PER_PCT_DM_UPPER)
pct_ch4_reduction_C_alt = np.clip(fat_effect_alt * increment_pct_dm, 0, 95)
new_ghg_C_alt = opt["ghg_intensity"] * (1.0 - pct_ch4_reduction_C_alt / 100.0)
abate_ton_yr_C_alt = (opt["ghg_intensity"] - new_ghg_C_alt) * FPCM * DAYS_PER_YEAR / 1000.0
net_cost_C_alt = gross_cost_C - abate_ton_yr_C_alt * carbon_price
dollar_per_ton_C_alt = net_cost_C_alt / abate_ton_yr_C_alt

# ================= Lever D: replacement-rate reduction =================
ei_reduction_D = rng.triangular(p.REPLACEMENT_EI_REDUCTION_PCT_PER_10PT[0],
                                  np.mean(p.REPLACEMENT_EI_REDUCTION_PCT_PER_10PT),
                                  p.REPLACEMENT_EI_REDUCTION_PCT_PER_10PT[1], N)
new_ghg_D = opt["ghg_intensity"] * (1.0 - ei_reduction_D / 100.0)
abate_ton_yr_D = (opt["ghg_intensity"] - new_ghg_D) * FPCM * DAYS_PER_YEAR / 1000.0
heifer_cost = rng.triangular(p.HEIFER_REARING_COST_USD[0], np.mean(p.HEIFER_REARING_COST_USD),
                               p.HEIFER_REARING_COST_USD[1], N)
cost_savings_D = 0.10 * heifer_cost  # 10-percentage-point reduction scenario
net_cost_D = -cost_savings_D - abate_ton_yr_D * carbon_price
dollar_per_ton_D = net_cost_D / abate_ton_yr_D

# ================= Table 3: assemble, summarize, rank =================
levers = {
    "A - Dietary NDF reduction": dollar_per_ton_A,
    "B - 3-NOP (interaction-corrected)": dollar_per_ton_B,
    "C - Rumen-available fat (primary estimate)": dollar_per_ton_C,
    "D - Replacement rate reduction": dollar_per_ton_D,
}
abatements = {
    "A - Dietary NDF reduction": abate_ton_yr_A,
    "B - 3-NOP (interaction-corrected)": abate_ton_yr_B,
    "C - Rumen-available fat (primary estimate)": abate_ton_yr_C,
    "D - Replacement rate reduction": abate_ton_yr_D,
}
rank_matrix = np.array([levers[k] for k in levers]).argsort(axis=0).argsort(axis=0) + 1
lever_names = list(levers.keys())

rows = []
for i, name in enumerate(lever_names):
    vals = levers[name]
    ranks_i = rank_matrix[i]
    row = dict(
        lever=name,
        abatement_ton_co2e_cow_yr_median=np.median(abatements[name]),
        dollar_per_ton_median=np.median(vals),
        dollar_per_ton_p5=np.percentile(vals, 5),
        dollar_per_ton_p95=np.percentile(vals, 95),
    )
    for r in [1, 2, 3, 4]:
        row[f"pct_rank_{r}"] = 100.0 * np.mean(ranks_i == r)
    rows.append(row)

table3 = pd.DataFrame(rows).sort_values("dollar_per_ton_median").reset_index(drop=True)
table3.insert(0, "macc_rank", range(1, len(table3) + 1))

pd.set_option("display.width", 160)
print("TABLE 3 -- Farm-level marginal abatement cost comparison")
print(table3.round(1).to_string(index=False))

# ---- Verification against manuscript Table 3 ----
d_row = table3.loc[table3["lever"].str.startswith("D")].iloc[0]
a_row = table3.loc[table3["lever"].str.startswith("A")].iloc[0]
b_row = table3.loc[table3["lever"].str.startswith("B")].iloc[0]
c_row = table3.loc[table3["lever"].str.startswith("C")].iloc[0]
assert round(d_row["dollar_per_ton_median"], 1) == -1416.2, d_row["dollar_per_ton_median"]
assert round(a_row["dollar_per_ton_median"], 1) == -612.8, a_row["dollar_per_ton_median"]
assert round(b_row["dollar_per_ton_median"], 1) == 70.7, b_row["dollar_per_ton_median"]
assert round(c_row["dollar_per_ton_median"], 1) == 427.4, c_row["dollar_per_ton_median"]
assert list(table3["lever"].str[0]) == ["D", "A", "B", "C"]
print("\nVERIFIED: matches manuscript Table 3 (rank order D-A-B-C; all four medians).")

table3.to_csv(p.OUTPUT / "Table3_macc_comparison.csv", index=False)
print(f"\nSaved: {p.OUTPUT / 'Table3_macc_comparison.csv'}")

# ================= Table 5: Lever C sensitivity =================
table5 = pd.DataFrame([
    dict(scenario="Primary (used in Table 3)",
         coefficient_source="de Ondarza et al., 2024 (3.77%/point)",
         abatement_ton_co2e_cow_yr_median=np.median(abate_ton_yr_C),
         dollar_per_ton_median=np.median(dollar_per_ton_C),
         dollar_per_ton_p5=np.percentile(dollar_per_ton_C, 5),
         dollar_per_ton_p95=np.percentile(dollar_per_ton_C, 95)),
    dict(scenario="Alternative higher-effect",
         coefficient_source="Hristov et al., 2022 (19.5%/point)",
         abatement_ton_co2e_cow_yr_median=np.median(abate_ton_yr_C_alt),
         dollar_per_ton_median=np.median(dollar_per_ton_C_alt),
         dollar_per_ton_p5=np.percentile(dollar_per_ton_C_alt, 5),
         dollar_per_ton_p95=np.percentile(dollar_per_ton_C_alt, 95)),
])
print("\nTABLE 5 -- Lever C sensitivity")
print(table5.round(2).to_string(index=False))

assert round(table5.loc[0, "dollar_per_ton_median"], 1) == 427.4
assert round(table5.loc[0, "abatement_ton_co2e_cow_yr_median"], 3) == 0.331
assert round(table5.loc[1, "dollar_per_ton_median"], 1) == 58.7
assert round(table5.loc[1, "abatement_ton_co2e_cow_yr_median"], 3) == 1.712
print("VERIFIED: matches manuscript Table 5.")

table5.to_csv(p.OUTPUT / "Table5_leverC_sensitivity.csv", index=False)
print(f"\nSaved: {p.OUTPUT / 'Table5_leverC_sensitivity.csv'}")

# ================= National-scale scaling (Table 8) =================
# Continues the SAME random-number-generator stream used above (not a new
# rng instance), so that adoption-rate draws follow immediately after the
# biological/economic draws already made -- reproducing the manuscript's
# exact reported national-scale figures (Methods Sec. 2.8).
abatement_draws = {"A": abate_ton_yr_A, "B": abate_ton_yr_B, "C": abate_ton_yr_C, "D": abate_ton_yr_D}
national_mmt_draws = {}
for code in ["A", "B", "C", "D"]:
    lo, hi = p.ADOPTION_RATE_RANGE[code]
    pt = p.ADOPTION_RATE[code]
    adoption_draw = rng.triangular(lo, pt, hi, N)
    national_mmt_draws[code] = abatement_draws[code] * p.NASS_DAIRY_COW_INVENTORY_HEAD * adoption_draw / 1e6

national_total_mmt = sum(national_mmt_draws.values())
aggregate_median = np.median(national_total_mmt)
tier1_representable_mmt = np.median(national_mmt_draws["D"])
not_represented_pct = (aggregate_median - tier1_representable_mmt) / aggregate_median * 100

assert round(aggregate_median, 3) == 4.258, aggregate_median
assert round(not_represented_pct, 1) == 91.4, not_represented_pct
print(f"\nNational aggregate (median): {aggregate_median:.3f} MMT CO2e/yr; "
      f"{not_represented_pct:.1f}% not Tier-1-representable.")
print("VERIFIED: matches manuscript Sec. 3.4 (4.258 MMT total; 91.4% not represented).")

# ================= Save raw draws for Table 8, Figure 2, and text-value checks =================
np.savez(p.OUTPUT / "mc_raw_draws.npz",
          carbon_price=carbon_price,
          dollar_per_ton_A=dollar_per_ton_A, dollar_per_ton_B=dollar_per_ton_B,
          dollar_per_ton_C=dollar_per_ton_C, dollar_per_ton_D=dollar_per_ton_D,
          abate_ton_yr_A=abate_ton_yr_A, abate_ton_yr_B=abate_ton_yr_B,
          abate_ton_yr_C=abate_ton_yr_C, abate_ton_yr_D=abate_ton_yr_D,
          national_mmt_A=national_mmt_draws["A"], national_mmt_B=national_mmt_draws["B"],
          national_mmt_C=national_mmt_draws["C"], national_mmt_D=national_mmt_draws["D"],
          nop_cost=nop_cost, ei_reduction_D=ei_reduction_D,
          heifer_cost=heifer_cost, price_shock=price_shock,
          intercept=intercept, ndf_coef=ndf_coef)
print(f"Saved: {p.OUTPUT / 'mc_raw_draws.npz'}")
