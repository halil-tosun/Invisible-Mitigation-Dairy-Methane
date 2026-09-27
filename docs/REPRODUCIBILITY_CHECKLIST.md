# REPRODUCIBILITY CHECKLIST

## Internal-Consistency Verification Against the Manuscript

Every value below was checked against the corresponding value reported
in the manuscript. Every script in `code/` also contains its own
`assert` statements enforcing these same checks at runtime; `run_all.py`
stops immediately if any check fails.

| Manuscript value | Reported as | Verified by | Status |
|---|---|---|---|
| Table 1 | All Panel A/B parameters | `06_table1_baseline_and_carbon_price.py` | Pass |
| Table 2 | Nine-ingredient library, DM-basis attributes | `01_ingredient_library.py` | Pass |
| Table 3 | All four medians; rank order D-A-B-C | `07_monte_carlo.py` | Pass |
| Table 4 | Baseline/intervention/delta, all four levers | `08_table4_intervention_magnitude.py` | Pass |
| Table 5 | Primary (0.331 t, $427.4) vs. alternative (1.712 t, $58.7) | `07_monte_carlo.py` | Pass |
| Table 6 | All six cells (three carbon prices x two coefficients) | `09_table6_leverC_carbon_price_breakdown.py` | Pass |
| Table 7 | 122.1 vs. 138.0 kg CH4/head/yr; 13,870 vs. 10,250 kg milk/head/yr | `10_table7_mechanistic_vs_tier1.py` | Pass |
| Table 8 | All four levers; 4.258 MMT aggregate; 91.4% not represented | `11_table8_national_scaling.py` | Pass |
| Figure 1 | Bar order and total width (4.258 MMT) | `12_figure1_macc_chart.py` | Pass |
| Figure 2 | Lever D and Lever C medians | `13_figure2_mc_bands.py` | Pass |
| Figure 3 | 4.258 MMT total; 91.4% not Tier-1-representable | `14_figure3_accounting_invisibility.py` | Pass |
| Results Sec. 3.2 (naive vs. corrected) | -32.13% vs. -32.44%; $63.44 vs. $62.79/ton | `15_supplementary_text_values.py` | Pass |
| Results Sec. 3.2 (tornado coefficients) | -0.760, +0.583, +0.302, +0.032 | `15_supplementary_text_values.py` | Pass |

## Known, Documented Analytical Corrections

This section documents every substantive correction identified during
preparation of this package and its accompanying manuscript, per
open-science practice of disclosing analytical history rather than
presenting only a final, silently corrected version.

### 1. GWP100 value: wrong cell of the IPCC AR6 table

**Issue identified:** An earlier stage of this study used 27.9 kg
CO2e/kg CH4 as the 100-year global warming potential for methane,
taken from IPCC AR6 WG1 Table 7.SM.7. That value is the undifferentiated,
oxidation-unadjusted GWP100 for methane generically, not the
biogenic-specific value.

**Correction:** All methane-to-CO2e conversions use 27.0 kg CO2e/kg
CH4 (Forster et al., 2021, Table 7.15), which includes the
methane-oxidation-to-CO2 adjustment applicable to biogenic sources
(enteric fermentation is a biogenic methane source). This is the
scientifically appropriate value and is used throughout.

**Where implemented:** `code/_paths.py`, `GWP100_CH4`.

### 2. Lever C methane-response coefficient: degenerate Monte Carlo distribution

**Issue identified:** An earlier version of the Monte Carlo simulation
drew Lever C's methane-response coefficient from a triangular
distribution with minimum = mode = 3.77%/point (the primary point
estimate) and maximum = 19.5%/point (an independent, higher-effect
estimate from a different meta-analysis). Because the mode coincided
with the minimum, this distribution was strongly right-skewed; its
simulated median (8.36%/point) was more than double the primary point
estimate, producing a reported median abatement and cost that did not
represent the cited primary evidence.

**Correction:** The primary coefficient (3.77%/point; de Ondarza et
al., 2024) is held at its point-estimate value (not sampled) in the
main Monte Carlo simulation. The alternative higher-effect coefficient
(19.5%/point; Hristov et al., 2022) is evaluated as a separate,
explicitly labeled scenario (Table 5), not pooled into the main
distribution.

**Effect on reported results:** Lever C's reported median abatement
changed from 0.733 to 0.331 ton CO2e/cow/yr, and median net cost from
$177 to $427/ton CO2e. This changed Lever C's rank (still 4th/least
cost-effective in both versions, but the magnitude changed
substantially) and the national not-Tier-1-representable share (from
93.8% to 91.4% of the four-lever aggregate).

**Where implemented:** `code/07_monte_carlo.py`, Lever C block.

### 3. Common baseline for Levers B, C, and D: text-code inconsistency

**Issue identified:** An earlier draft of the manuscript's Methods
text stated that Lever B's methane-response calculation was applied to
the unmodified business-as-usual diet (NDF = 34.1%), "not the
Lever-A-optimized diet." This directly contradicted the code, which
had always applied the calculation to the Lever-A-optimized diet
(NDF = 33.67%) -- the code comment even labeled this
"interaction-corrected." Because the code's actual behavior was
intentional and correctly captures a real Lever A x B interaction (3-NOP
is more effective on lower-NDF diets), the text -- not the code -- was
the error.

**Correction:** The manuscript text was corrected to accurately state
that Levers B, C, and D share a common baseline (the Lever-A-optimized
diet), representing each intervention's marginal cost-effectiveness
when layered on top of an already-reformulated ration. No code or
reported-number changes were required; this was a documentation
correction only, but is recorded here because it was found only
through a line-by-line audit of code against text.

**Where implemented:** `code/07_monte_carlo.py`, Lever B/C/D blocks
(see comments); `docs/CODEBOOK.md`, "Levers B, C, D common baseline."

### 4. Citation year: Honan et al., 2021 vs. 2022

**Issue identified:** The manuscript and an earlier version of this
package cited the rumen-available fat ceiling source as "Honan et al.,
2021." Direct verification against the primary source (Animal
Production Science) confirmed the publication year is 2022, not 2021.

**Correction:** All citations updated to Honan et al. (2022). No
numeric values were affected (this was a citation-year error only).

**Where implemented:** `code/_paths.py`, `data/processed/` documentation
comments, and `docs/DATA_DESCRIPTION.md`.

### 5. Lever D baseline-replacement-rate citation: geographic mismatch

**Issue identified:** An earlier version of this package cited
"Talukder et al. (2025)" as the source for the 31% baseline
replacement rate described as a "northeastern U.S. benchmark." Direct
verification against the primary source found that Talukder et al.
(2025) reports on south-east Australian dairy herds, not the
northeastern United States; it was the wrong source for this specific
claim.

**Correction:** The 31% baseline (and northeastern U.S. framing) is
correctly attributed to USDA/NAHMS (2018), *Dairy 2014: Health and
Management Practices on U.S. Dairy Operations*, which directly reports
a 31.4% average cull rate for the northeastern United States. The
Talukder et al. (2025) citation was removed from this specific claim.

**Where implemented:** `code/_paths.py` (`REPLACEMENT_RATE_BAU`
comment), `08_table4_intervention_magnitude.py`.

### 6. Lever C fat-loss interpretation: milk-fat vs. overall milk yield

**Issue identified:** An earlier version of this analysis applied a
reported 6.0% reduction figure to overall milk yield (kg/d). The
primary source's abstract reports that milk fat percentage and milk
fat yield (kg/d) -- not overall milk yield -- are reduced by 7.8% and
6.0% respectively; the source does not report overall milk yield as
significantly affected.

**Correction:** The 6.0% figure is applied to milk-fat yield (kg
fat/d), valued at the butterfat component price, rather than to
overall milk yield valued at the whole-milk price.

**Where implemented:** `code/04_lever_c_fat.py`, `code/07_monte_carlo.py`.

## What This Package Does Not Claim

Consistent with the manuscript's own stated limitations:

- Carbon price is propagated as a single pooled Monte Carlo
  distribution across three heterogeneous market benchmarks, not as
  three separately evaluated scenarios. This is a disclosed
  simplification; Table 6 provides a deterministic, scenario-
  conditional alternative for Lever C specifically, but a fully
  scenario-conditional uncertainty architecture across all four levers
  was not implemented.
- Adoption-rate, biological-parameter, and economic-parameter
  uncertainty are combined within a single reported 90% uncertainty
  interval (Table 3, Table 8); these are conceptually distinct sources
  of uncertainty that this package's Monte Carlo framework does not
  separately decompose.
- National-scale estimates apply a lactating-cow abatement estimate to
  the full milk-cow inventory (which includes a non-lactating
  fraction), which may modestly overstate national abatement to an
  extent not quantified precisely in this package.
- Lever D's classification as Tier-1-representable (Table 8, Figure 3)
  is a structural/qualitative classification, not a verified
  one-to-one demographic decomposition of the specific reported
  tonnage into a documented replacement-heifer headcount change.
- This package does not simulate within-farm joint adoption of
  multiple levers on the same animals; the four levers' national-scale
  results are independently scaled scenario potentials, not a joint
  national forecast, and should not be summed to infer the outcome of
  concurrent adoption at the farm level.
