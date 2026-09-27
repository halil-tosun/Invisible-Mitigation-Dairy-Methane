"""
10_table7_mechanistic_vs_tier1.py -- Table 7.

Illustrative benchmark comparison between this study's mechanistic,
diet-responsive baseline enteric CH4 estimate and the IPCC Tier 1
default emission factor for North American dairy cattle. Not a model
validation exercise: the two estimates apply to animals of different
reference productivity levels (Methods Sec. 2.7; Results Sec. 3.3).

Produces: output/Table7_mechanistic_vs_tier1.csv
"""
import pandas as pd
import _paths as p
from _calc import ECM

NDF_BAU_PCT = p.NASEM_MEAN_NDF * 100.0  # 34.1% DM

# ---- This study's mechanistic baseline (Niu et al., 2018; Eqs. 1-3) ----
ch4_mj_d = 13.3 + 0.118 * NDF_BAU_PCT - 0.130 * ECM + 2.20 * p.FAT - 1.71 * p.PROT_MILK + 0.00521 * p.BW
ch4_kg_d = ch4_mj_d / p.MJ_PER_KG_CH4
ch4_kg_head_yr_mechanistic = ch4_kg_d * 365
reference_milk_mechanistic = p.MILK * 365  # kg/head/yr, this study's representative cow

# ---- IPCC Tier 1 default (North America, dairy cattle) ----
# IPCC (2019 Refinement, Vol. 4, Ch. 10, Table 10.11), confirmed directly
# against the primary source.
TIER1_EF_NA = 138.0                # kg CH4/head/yr
TIER1_REFERENCE_MILK = 10250.0     # kg/head/yr, regional default assumption
TIER1_UNCERTAINTY_LOW = 0.30       # IPCC (2006), Sec. 10.3.4, verbatim: "unlikely
TIER1_UNCERTAINTY_HIGH = 0.50      # to be known more accurately than +30% and may
                                    # be uncertain to +50%"

diff_kg = TIER1_EF_NA - ch4_kg_head_yr_mechanistic
diff_pct = diff_kg / ch4_kg_head_yr_mechanistic * 100
milk_diff_kg = reference_milk_mechanistic - TIER1_REFERENCE_MILK
milk_diff_pct = milk_diff_kg / TIER1_REFERENCE_MILK * 100

plausible_30 = (TIER1_EF_NA * (1 - TIER1_UNCERTAINTY_LOW), TIER1_EF_NA * (1 + TIER1_UNCERTAINTY_LOW))
plausible_50 = (TIER1_EF_NA * (1 - TIER1_UNCERTAINTY_HIGH), TIER1_EF_NA * (1 + TIER1_UNCERTAINTY_HIGH))

table7 = pd.DataFrame([
    dict(parameter="Baseline enteric CH4 (kg/head/yr)",
         mechanistic_this_study=round(ch4_kg_head_yr_mechanistic, 1),
         ipcc_tier1_default=TIER1_EF_NA,
         difference=f"+{diff_kg:.1f} (+{diff_pct:.1f}%)"),
    dict(parameter="Reference milk production (kg/head/yr)",
         mechanistic_this_study=round(reference_milk_mechanistic),
         ipcc_tier1_default=round(TIER1_REFERENCE_MILK),
         difference=f"+{milk_diff_kg:.0f} (+{milk_diff_pct:.1f}%)"),
    dict(parameter="Stated uncertainty range", mechanistic_this_study="Deterministic point estimate",
         ipcc_tier1_default="+30% to +50%", difference="--"),
    dict(parameter="Plausible range at stated uncertainty (kg/head/yr)", mechanistic_this_study="n/a",
         ipcc_tier1_default=f"{plausible_30[0]:.1f}-{plausible_30[1]:.1f} (+/-30%); "
                             f"{plausible_50[0]:.1f}-{plausible_50[1]:.1f} (+/-50%)",
         difference="--"),
])
print(table7.to_string(index=False))

# ---- Verification against manuscript Table 7 ----
assert round(ch4_kg_head_yr_mechanistic, 1) == 122.1, ch4_kg_head_yr_mechanistic
assert round(reference_milk_mechanistic) == 13870, reference_milk_mechanistic
assert round(diff_kg, 1) == 15.9 and round(diff_pct, 1) == 13.0
assert round(milk_diff_kg) == 3620 and round(milk_diff_pct, 1) == 35.3
assert round(plausible_30[0], 1) == 96.6 and round(plausible_30[1], 1) == 179.4
assert round(plausible_50[0], 1) == 69.0 and round(plausible_50[1], 1) == 207.0
print("\nVERIFIED: matches manuscript Table 7 exactly.")

table7.to_csv(p.OUTPUT / "Table7_mechanistic_vs_tier1.csv", index=False)
print(f"\nSaved: {p.OUTPUT / 'Table7_mechanistic_vs_tier1.csv'}")
