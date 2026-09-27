"""
09_table6_leverC_carbon_price_breakdown.py -- Table 6.

Lever C deterministic point-estimate net cost at each of the three
carbon-price benchmarks (Table 1, Panel B), for both the primary and
alternative higher-effect methane-response coefficients. Holds all
other parameters at their point-estimate values; not part of Table 5's
pooled-distribution Monte Carlo (Methods Sec. 2.4).

Requires: 04_lever_c_fat.py

Produces: output/Table6_leverC_carbon_price_breakdown.csv
"""
import pandas as pd
import _paths as p

lever_c = pd.read_csv(p.OUTPUT / "LeverC_fat_results.csv")

scenario_map = {"low": "Low ($6.34/ton)", "mid": "Mid ($30.00/ton)", "high": "High ($52.5/ton)"}
effect_map = {"primary (3.77%/pt)": "primary_usd_per_ton",
              "alternative higher-effect (19.5%/pt)": "alt_higher_effect_usd_per_ton"}

rows = []
for cp_key, cp_label in scenario_map.items():
    primary = lever_c.query("effect_estimate == 'primary (3.77%/pt)' and carbon_price_scenario == @cp_key").iloc[0]
    alt = lever_c.query("effect_estimate == 'alternative higher-effect (19.5%/pt)' and carbon_price_scenario == @cp_key").iloc[0]
    rows.append(dict(
        carbon_price_benchmark=cp_label,
        primary_usd_per_ton=round(primary["net_dollar_per_ton_co2e"], 1),
        alt_higher_effect_usd_per_ton=round(alt["net_dollar_per_ton_co2e"], 1),
    ))

table6 = pd.DataFrame(rows)
print(table6.to_string(index=False))

# ---- Verification against manuscript Table 6 ----
assert table6.loc[0, "primary_usd_per_ton"] == 450.7
assert table6.loc[1, "primary_usd_per_ton"] == 427.1
assert table6.loc[2, "primary_usd_per_ton"] == 404.6
assert table6.loc[0, "alt_higher_effect_usd_per_ton"] == 82.0
assert table6.loc[1, "alt_higher_effect_usd_per_ton"] == 58.4
assert table6.loc[2, "alt_higher_effect_usd_per_ton"] == 35.9
print("\nVERIFIED: matches manuscript Table 6 (all six cells).")

table6.to_csv(p.OUTPUT / "Table6_leverC_carbon_price_breakdown.csv", index=False)
print(f"\nSaved: {p.OUTPUT / 'Table6_leverC_carbon_price_breakdown.csv'}")
