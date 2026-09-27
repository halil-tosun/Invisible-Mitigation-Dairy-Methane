# DATA DESCRIPTION

## Overview

This study does not use an external raw panel dataset. Its inputs are:
(1) fixed animal/production assumptions representing a high-producing
U.S. Holstein cow, (2) an author-curated ingredient library used in the
Lever A diet optimization and Lever C fat substitution, and (3)
literature-derived coefficients and price parameters for each of the
four mitigation levers and the three carbon-price scenarios. All
constants are defined once, with full source citations, in
`code/_paths.py`.

## 1. Fixed animal/production assumptions (Table 1, Panel A)

| Parameter | Value | Source |
|---|---|---|
| Body weight | 650 kg | Representative lactating Holstein cow |
| Milk yield | 38.0 kg/d | Representative lactating Holstein cow |
| Milk fat | 3.8% | Representative lactating Holstein cow |
| Milk true protein | 3.1% | Representative lactating Holstein cow |
| Milk price | $20.70/cwt | USDA ERS, All Milk Price, June 2026 annual forecast |
| U.S. milk cow inventory | 9.65 million head | USDA NASS Cattle report, released July 24, 2026 |
| Methane GWP100 (biogenic) | 27.0 kg CO2e/kg CH4 | IPCC AR6 WG1, Forster et al. (2021), Table 7.15 |
| BAU dietary NDF (mean) | 34.1% DM | NASEM (2021), 34.1 +/- 4.6% DM |

## 2. Ingredient library (`data/processed/ingredient_library.csv`; Table 2)

Author-curated table of nine candidate dairy ration ingredients with
DM-basis NDF, ADF, CP, fat, NEL, and price attributes, used in Lever
A's least-cost diet optimization and Lever C's fat substitution.
Ingredient prices reflect the computational environment accompanying
this manuscript (dataset vintage disclosed in the manuscript's Table 2
footnote). DDGS, soybean hulls, and tallow are included in the library
but are not selected by the optimizer at any evaluated NDF floor.

## 3. Rumen-health and optimization constraints

| Constraint | Value | Source |
|---|---|---|
| Forage NDF floor | 19% DM | NRC (2001) / NASEM (2021) |
| Total dietary NDF floor | 25% DM | NRC (2001) |
| NFC ceiling | 40% DM | NRC (2001) |
| Rumen-available fat ceiling | 5.5% DM | Honan et al. (2022) |
| Crude protein range | 16.0-18.5% DM | NASEM (2021) |
| Forage inclusion range, single-forage cap, corn-grain cap, SBM cap | 35-65%, 45%, 40%, 20% | Author design choices for ration feasibility, not literature-derived (disclosed as such) |

## 4. Lever B: 3-nitrooxypropanol (3-NOP)

Kebreab, E., et al. (2022). Meta-analysis of the effects of 3-NOP dose
and dietary NDF on enteric methane emissions in dairy cattle. *Journal
of Dairy Science* 106:927-936. doi:10.3168/jds.2022-22211

CH4 intensity change (%) = -33.0 - 0.275(dose-70.5) + 0.723(NDF-32.9),
dose in mg/kg DM, NDF in % DM. Applied at the reference dose (70.5
mg/kg DM) to the Lever-A-optimized diet.

3-NOP net cost: $93-105/cow/yr (DSM-linked estimate) to $128.32/cow/yr
(independent/skeptical estimate, used as a sensitivity bound).

## 5. Lever C: rumen-available fat supplementation

- Primary methane-response coefficient: 3.77% CH4-intensity reduction
  per percentage-point increase in dietary fat (de Ondarza, M.B., de
  Souza, V.C., Kebreab, E., Tricarico, J.M., 2024. *Journal of Dairy
  Science* 107:8072-8083. doi:10.3168/jds.2023-24528; 35-study
  meta-analysis).
- Alternative higher-effect coefficient: 19.5%/point (Hristov, A.N.,
  Melgar, A., Wasson, D., Arndt, C., 2022. Symposium review: effective
  nutritional strategies to mitigate enteric methane in dairy cattle.
  *Journal of Dairy Science* 105:8543-8557. doi:10.3168/jds.2021-21398;
  multi-species meta-analysis).
- Milk-fat yield loss: 6.0% relative reduction (kg fat/d); milk-fat
  percentage loss: 7.8% relative reduction (de Ondarza et al., 2024;
  the same source does not report overall milk yield as significantly
  affected).
- Butterfat price: $3.5107/kg (USDA AMS Advanced Butterfat Pricing
  Factor, January 2026: $1.5921/lb).

## 6. Lever D: replacement-rate reduction

- Baseline (31%) and target (21%) replacement rate: USDA/NAHMS (2018).
  *Dairy 2014: Health and Management Practices on U.S. Dairy
  Operations.* USDA-APHIS-VS, National Animal Health Monitoring System
  (northeastern U.S. average cull rate).
- Emission-intensity reduction: 2.7-5.0% per 10-percentage-point
  replacement-rate reduction, triangulated from two independent
  European herd-simulation studies: Chen, L., Thorup, V.M., Ostergaard,
  S. (2026). Herd management strategies for greenhouse gas emission
  mitigation in dairy production: a simulation study. *Journal of Dairy
  Science* (in press). doi:10.3168/jds.2025-27083; and Sommerseth,
  J.K., et al. (2024). How increased heifer growth rate and reduced
  dairy cow replacement rate can improve farm economy and reduce
  greenhouse gas emissions. *Animal* 18:101294.
  doi:10.1016/j.animal.2024.101294. No U.S.-specific coefficient was
  identified in the literature (geographic-transferability limitation).
- Heifer-rearing cost: $1,594-1,919 (dry-lot to confinement range;
  Hawkins, A., Burdine, K.H., Amaral-Phillips, D.M., Costa, J.H.C.,
  2020. *Frontiers in Veterinary Science* 7:625.
  doi:10.3389/fvets.2020.00625; birth-to-calving).

## 7. Carbon-price scenarios (Table 1, Panel B)

| Scenario | Price | Source |
|---|---|---|
| Low | $6.34/ton CO2e | Ecosystem Marketplace, State of the Voluntary Carbon Market, 2025 |
| Mid | $30.00/ton CO2e | First verified dairy carbon transaction, quoted via Agri-Pulse |
| High | $45-60/ton CO2e | General premium/ICVCM-screened corporate market ceiling (not livestock-specific) |

## 8. IPCC Tier 1 reference values (Table 7)

- North American dairy cattle default: 138.0 kg CH4/head/yr, at a
  reference milk production of 10,250 kg/head/yr (IPCC 2019
  Refinement, Vol. 4, Ch. 10, Table 10.11).
- Stated uncertainty: +30% to +50% (IPCC 2006, Sec. 10.3.4).

## 9. National-scale adoption-rate assumptions (Table 8)

Illustrative, expert-judgment adoption-rate point estimates and ranges
for each lever (Methods Sec. 2.8), following USDA/ICF (2023)'s own
methodology for practice-adoption-rate estimation. Not survey-derived
rates; see `code/_paths.py` (`ADOPTION_RATE`, `ADOPTION_RATE_RANGE`)
for exact values.
