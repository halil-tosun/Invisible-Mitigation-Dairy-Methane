# Invisible Mitigation: Why Default Methane Accounting Cannot See What Dairy Farmers Do

Reproducibility package for a study formally demonstrating that the
IPCC Tier 1 national greenhouse gas inventory method -- which
calculates livestock methane as the product of animal population and a
diet-invariant default emission factor -- is structurally unable to
register farm-level, diet-mediated enteric methane mitigation,
independent of that mitigation's biological reality or economic merit.
The argument is formalized and illustrated using a mechanistic
enteric-methane model combined with four candidate dairy-sector
mitigation interventions, parameterized with U.S. Holstein performance
and price data as a methodological testbed.

**Author:** Halil Tosun, ADA University, School of Agricultural and
Food Sciences, Department of Animal Science, Baku, Azerbaijan.
ORCID: [0000-0001-5117-0390](https://orcid.org/0000-0001-5117-0390)

## What This Repository Reproduces

Running the pipeline end-to-end reproduces every table and figure
reported in the manuscript:

| Output | Description | Script |
|---|---|---|
| Table 1 | Baseline animal, dietary, and carbon-price parameters | `06_table1_baseline_and_carbon_price.py` |
| Table 2 | Ingredient library (Lever A optimization / Lever C fat substitution) | `01_ingredient_library.py` |
| Table 3 | Farm-level marginal abatement cost comparison (Monte Carlo) | `07_monte_carlo.py` |
| Table 4 | Intervention magnitude (baseline vs. intervention), by lever | `08_table4_intervention_magnitude.py` |
| Table 5 | Lever C sensitivity: primary vs. alternative higher-effect coefficient | `07_monte_carlo.py` |
| Table 6 | Lever C deterministic point estimates by carbon-price benchmark | `09_table6_leverC_carbon_price_breakdown.py` |
| Table 7 | Mechanistic baseline vs. IPCC Tier 1 default (illustrative benchmark) | `10_table7_mechanistic_vs_tier1.py` |
| Table 8 | National-scale abatement potential and Tier 1 representation status | `11_table8_national_scaling.py` |
| Figure 1 | Marginal abatement cost comparison (stepped chart) | `12_figure1_macc_chart.py` |
| Figure 2 | Monte Carlo uncertainty distributions per lever | `13_figure2_mc_bands.py` |
| Figure 3 | Achieved vs. Tier-1-representable abatement, by lever | `14_figure3_accounting_invisibility.py` |

Script `15_supplementary_text_values.py` additionally verifies two
values reported directly in the manuscript's running text (Results
Sec. 3.2: the naive-additive vs. interaction-corrected comparison for
Lever B, and the tornado-sensitivity coefficients) that are not
presented as a standalone table or figure.

Every script contains internal `assert` statements checking its output
against the corresponding manuscript value; the pipeline stops
immediately if any value fails to reproduce.

## Quick Start

```bash
conda env create -f environment.yml
conda activate invisible-mitigation-repro
cd code
python run_all.py
```

or, without conda:

```bash
pip install -r requirements.txt
cd code
python run_all.py
```

Expected runtime: under 30 seconds on a standard laptop. See
`docs/Replication_Guide.md` for step-by-step instructions, how to run
individual scripts, and how to adapt this pipeline to a different
setting.

## Repository Structure

```
code/               Numbered analysis scripts (01-15) + shared config (_paths.py, _calc.py) + run_all.py
data/processed/      Ingredient library (author-curated input table; see docs/DATA_DESCRIPTION.md)
output/              Generated table CSVs (+ mc_raw_draws.npz, saved Monte Carlo draws)
figures/             Generated figure PNGs
docs/
  DATA_DESCRIPTION.md          Full parameter/source provenance for every input
  CODEBOOK.md                  Model equations and implementation notes
  REPRODUCIBILITY_CHECKLIST.md Verification results + documented analytical history
  Replication_Guide.md         Step-by-step usage and troubleshooting
```

## Data Source

This study does not use an external raw dataset: every input is either
a fixed animal/production parameter, a literature-derived coefficient,
or an author-curated ingredient-price table
(`data/processed/ingredient_library.csv`). Full provenance -- including
the primary literature source for every parameter -- is documented in
`docs/DATA_DESCRIPTION.md`.

## Scope Note

The quantitative magnitudes reproduced by this package (farm-level
cost-effectiveness, national-scale tonnage) are illustrative of U.S.
Holstein productivity, U.S. feed and carbon-market prices, and the U.S.
dairy herd, used as a methodological testbed. The United States itself
reports cattle enteric fermentation emissions under IPCC Tier 2
methodology, not Tier 1 (U.S. EPA, 2025); the accounting-invisibility
mechanism this study formalizes is general to any jurisdiction using
the Tier 1 formulation, but the specific dollar and tonnage magnitudes
are not direct empirical estimates for any actual Tier 1-reporting
country, whose animal performance, diet, and cost structures would
differ (manuscript Methods Sec. 2.1).

## License

Code and documentation in this repository are released under the MIT
License (see `LICENSE`).

## Citation

See `CITATION.cff` for citation metadata.
