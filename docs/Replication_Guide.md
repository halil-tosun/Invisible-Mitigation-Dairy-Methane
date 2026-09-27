# REPLICATION GUIDE

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

Expected runtime: under 30 seconds on a standard laptop. Every script
prints its results and its own internal verification checks;
`run_all.py` stops immediately if any check fails.

## Step-by-Step (running scripts individually)

All scripts read their inputs from `data/processed/` or `output/`
directly (via `_paths.py`), not from another script's in-memory state,
so scripts can be run individually provided their stated prerequisite
has been run at least once. Prerequisites:

| Script | Requires (must be run first) |
|---|---|
| `01_ingredient_library.py` | none |
| `02_lever_a_optimization.py` | `01` |
| `03_lever_b_3nop.py` | `02` |
| `04_lever_c_fat.py` | `02` |
| `05_lever_d_replacement.py` | `02` |
| `06_table1_baseline_and_carbon_price.py` | none |
| `07_monte_carlo.py` | `02` |
| `08_table4_intervention_magnitude.py` | `02` |
| `09_table6_leverC_carbon_price_breakdown.py` | `04` |
| `10_table7_mechanistic_vs_tier1.py` | none |
| `11_table8_national_scaling.py` | `07` |
| `12_figure1_macc_chart.py` | `07`, `11` |
| `13_figure2_mc_bands.py` | `07` |
| `14_figure3_accounting_invisibility.py` | `07` |
| `15_supplementary_text_values.py` | `03`, `07` |

## Adapting This Package to a Different Setting

To apply this pipeline to a different representative animal, a
different country's price data, or a different set of mitigation
levers:

1. **Update `code/_paths.py`'s fixed animal/production assumptions**
   (`BW`, `MILK`, `FAT`, `PROT_MILK`) and price parameters
   (`MILK_PRICE_CWT`, `BUTTERFAT_PRICE_USD_PER_KG`,
   `CARBON_PRICE_*`) to match your setting.
2. **Replace `data/processed/ingredient_library.csv`** with your own
   ingredient set and prices if adapting Lever A/C to a different
   ration context.
3. **Update the Tier 1 reference values** in
   `10_table7_mechanistic_vs_tier1.py` (`TIER1_EF_NA`,
   `TIER1_REFERENCE_MILK`) if working with a different region or
   productivity system (IPCC 2019 Refinement, Table 10.11 provides
   region-specific defaults).
4. **Update `REPLACEMENT_RATE_BAU`/`REPLACEMENT_RATE_TARGET` and the
   adoption-rate assumptions** (`ADOPTION_RATE`,
   `ADOPTION_RATE_RANGE`) in `_paths.py` if working with a different
   herd-demographic or adoption context.
5. **Re-verify all `assert` statements.** Every script's assertions
   check against *this* study's specific reported values; when
   adapting the pipeline to new data, remove or update these
   assertions to reflect your own results before treating a
   "no AssertionError" run as a validation of correctness.

## Common Issues

- **`ModuleNotFoundError` for `_paths`:** scripts must be run from
  inside the `code/` directory (`cd code` first), since `_paths.py` is
  imported as a local module, not an installed package.
- **`FileNotFoundError` for an intermediate CSV or `.npz` file:** run
  the prerequisite script listed in the table above first, or simply
  run `run_all.py`, which runs every script in the correct order.
- **Numerical Hessian or optimizer-convergence warnings in
  `02_lever_a_optimization.py`:** if you modify the ingredient library
  or constraints, check that the optimizer still converges to a
  feasible solution at every candidate NDF floor; an infeasible
  constraint set will produce a warning rather than a silent wrong
  answer.
- **A verification `assert` fails after modifying a script:** this is
  expected if you have changed an input parameter, coefficient, or
  constraint -- the assertions check against this study's specific
  reported values, not against a general correctness criterion. Update
  or remove the relevant assertion once you have confirmed your new
  result is intentional.
