# CODEBOOK

## Model Equations

**Eq. 1 -- Enteric methane production (Niu et al., 2018)**

```
CH4 (MJ/d) = 13.3 + 0.118*NDF - 0.130*ECM + 2.20*FAT - 1.71*PROTEIN + 0.00521*BW
```

NDF is dietary neutral detergent fiber (% DM); ECM is energy-corrected
milk yield (kg/d); FAT and PROTEIN are milk fat and true protein
content (%, held constant across all scenarios); BW is body weight
(kg). Implemented in `code/_calc.py`, `diet_stats()`.

**Eq. 2 -- Energy-corrected milk (Tyrrell and Reid, 1965)**

```
ECM (kg/d) = 0.327*MILK + 12.95*(MILK*FAT/100) + 7.2*(MILK*PROTEIN/100)
```

**Eq. 3 -- Methane mass (Brouwer, 1965)**

```
CH4 (kg/d) = CH4(MJ/d) / 55.65
```

**Eq. 4 -- 3-NOP interaction-adjusted CH4 response (Kebreab et al., 2022)**

```
Delta CH4 intensity (%) = -33.0 - 0.275*(dose-70.5) + 0.723*(NDF-32.9)
```

Implemented in `code/_calc.py`, `kebreab_3nop_ch4_intensity_change_pct()`.

**Eq. 5 -- IPCC Tier 1 total emissions**

```
E_Tier1(T) = N(T) x EF_Tier1(region, productivity system)
```

EF_Tier1 is a fixed table value (IPCC 2019 Refinement, Table 10.11),
not a function of diet composition.

**Eq. 6 -- Mechanistic total emissions**

```
E_mechanistic = f(NDF, FAT, PROTEIN, BW, MILK)
```

**Eq. 7 -- National-scale abatement**

```
National abatement (MMT CO2e/yr) = [N_herd x Adoption_rate x Per-cow abatement (ton CO2e/cow/yr)] / 1,000,000
```

## Diet-Level Economics

- Dry matter intake: `DMI (kg/d) = (NEmaintenance + NElactation) / Diet NEL density`,
  where `NEmaintenance = 0.080 * BW^0.75` and `NElactation = MILK * 0.74`.
- Feed cost: `feed_cost_d = DMI * weighted ingredient price + premix ($0.55/cow/d, fixed)`.
- Income over feed cost: `IOFC = milk revenue - feed cost`.
- NFC (% DM) approximated as `100 - NDF - CP - FAT - 7.5` (typical ash
  assumption, NRC 2001).

Because milk revenue is constant across candidate diets (milk yield and
composition are held fixed across all scenarios), IOFC-maximization at
each NDF floor is equivalent to feed-cost minimization; the resulting
ranking of diets by cost is therefore independent of the milk-price
assumption.

## Lever Construction

**Lever A (dietary NDF reduction).** Constrained nonlinear optimization
(SciPy SLSQP, `scipy.optimize.minimize`) identifies, at each of nine
candidate NDF floors (28-37.2% DM), the least-cost combination of five
ingredients (two forages + corn grain + soybean meal + one additional
forage) subject to the rumen-health constraints in
`docs/DATA_DESCRIPTION.md`, Section 3. Implemented in
`02_lever_a_optimization.py`.

**Levers B, C, D common baseline.** Levers B, C, and D all use the
Lever-A-optimized diet (not the unmodified business-as-usual ration) as
their baseline, representing each intervention's marginal
cost-effectiveness when layered on top of an already-reformulated
ration. This is a deliberate design choice: because Eq. 4's NDF term
means 3-NOP is more effective on lower-NDF diets, applying it after
Lever A's diet change captures a real Lever A x B interaction rather
than treating the four levers as independent, non-interacting
alternatives to BAU.

**Lever B (3-NOP).** Applied at the reference meta-analytic dose (70.5
mg/kg DM) to the Lever-A-optimized diet. Because the dose term in Eq. 4
is expressed relative to this same reference dose, evaluating at
Dose = 70.5 makes that term vanish identically, regardless of the dose
coefficient's value; the dose coefficient's sampling uncertainty is
therefore excluded from the Monte Carlo simulation and from the
tornado-sensitivity analysis by construction, not because it was tested
and found negligible. Implemented in `03_lever_b_3nop.py`.

**Lever C (rumen-available fat).** Whole cottonseed represents the
rumen-available (unprotected) fat source; calcium-soap and hydrogenated
(bypass) fat sources are excluded by mechanism. Fat inclusion is
increased from the Lever-A-optimized diet's fat content to the 5.5% DM
rumen-health ceiling. Cost combines (i) the ingredient cost delta from
substituting whole cottonseed, and (ii) a milk-fat component revenue
loss (not overall milk-yield loss). Implemented in `04_lever_c_fat.py`.

**Lever D (replacement-rate reduction).** A 10-percentage-point
reduction in replacement rate (31% to 21%), evaluated using a
literature-derived emission-intensity reduction coefficient applied to
the lactating-cow enteric CH4 intensity metric, alongside avoided
heifer-rearing cost. This lever's abatement estimate is not derived
from an explicit demographic (animal-count) model -- a distinction
that matters for the Tier 1 accounting classification (Methods Sec.
2.5). Implemented in `05_lever_d_replacement.py`.

## Monte Carlo Specification

10,000 iterations, fixed seed = 42 (NumPy `Generator` API).
Distributional choices:

- **Normal**, using reported standard errors: Kebreab et al. (2022)
  intercept (SE = 1.2) and NDF coefficient (SE = 0.167).
- **Triangular** (min/mode/max), for parameters reported only as a
  literature range: carbon price, 3-NOP net cost, Lever D
  emission-intensity reduction and heifer-rearing cost, adoption
  rates, and Lever A's ingredient-price shock (+/-20%, a lighter-weight
  proxy for full re-optimization at each draw).
- Carbon price is drawn once per iteration and applied identically to
  all four levers (correct correlation structure: all levers face the
  same market price in a given draw). This pools three heterogeneous
  market benchmarks into a single triangular distribution, a disclosed
  simplification (see `docs/REPRODUCIBILITY_CHECKLIST.md`); Table 6
  provides a scenario-conditional deterministic alternative for Lever
  C specifically.
- Lever C's methane-response coefficient is held at its primary point
  estimate (not sampled) in the main simulation; the alternative
  higher-effect coefficient is evaluated as a separate, parallel
  calculation (Table 5), not pooled into the same distribution.
- Adoption-rate draws (Table 8) continue the same random-number-
  generator stream used for the biological/economic draws (Table 3),
  in the same script (`07_monte_carlo.py`), so that the national-scale
  results are bit-for-bit consistent with the farm-level results rather
  than independently re-simulated.

## Tier 1 Accounting Classification (Methods Sec. 2.5)

Levers A, B, and C act by changing diet composition. Because Tier 1's
emission factor (Eq. 5) is not a function of diet, these levers'
abatement is classified as not represented under Tier 1, regardless of
biological magnitude or economic merit. Lever D acts by changing herd
replacement rate -- a population-level (activity-data) change that
Tier 1's population-count-based total-emissions equation would, in
principle, register at any tier. This is a structural, qualitative
classification, not a verified one-to-one demographic decomposition of
Lever D's specific reported tonnage (disclosed limitation).
