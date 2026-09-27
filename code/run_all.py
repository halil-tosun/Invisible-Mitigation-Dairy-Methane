"""
run_all.py -- Runs the complete analytical pipeline in order, from a
clean state.

Invisible Mitigation: Why Default Methane Accounting Cannot See What
Dairy Farmers Do (Tosun).

Reproduces every table and figure reported in the manuscript:
    Table 1  -- 06_table1_baseline_and_carbon_price.py
    Table 2  -- 01_ingredient_library.py (validates data/processed/ingredient_library.csv)
    Table 3  -- 07_monte_carlo.py
    Table 4  -- 08_table4_intervention_magnitude.py
    Table 5  -- 07_monte_carlo.py
    Table 6  -- 09_table6_leverC_carbon_price_breakdown.py
    Table 7  -- 10_table7_mechanistic_vs_tier1.py
    Table 8  -- 11_table8_national_scaling.py
    Figure 1 -- 12_figure1_macc_chart.py
    Figure 2 -- 13_figure2_mc_bands.py
    Figure 3 -- 14_figure3_accounting_invisibility.py

Script 15 verifies two additional values reported directly in the
manuscript's running text (Results Sec. 3.2) that are not presented as
a standalone table or figure.

Every script contains its own internal `assert` statements checking its
output against the manuscript's reported values; this script stops
immediately if any check fails, rather than silently continuing with a
mismatched output.

Expected runtime: under 30 seconds on a standard laptop.
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

SCRIPTS = [
    "01_ingredient_library.py",
    "02_lever_a_optimization.py",
    "03_lever_b_3nop.py",
    "04_lever_c_fat.py",
    "05_lever_d_replacement.py",
    "06_table1_baseline_and_carbon_price.py",
    "07_monte_carlo.py",
    "08_table4_intervention_magnitude.py",
    "09_table6_leverC_carbon_price_breakdown.py",
    "10_table7_mechanistic_vs_tier1.py",
    "11_table8_national_scaling.py",
    "12_figure1_macc_chart.py",
    "13_figure2_mc_bands.py",
    "14_figure3_accounting_invisibility.py",
    "15_supplementary_text_values.py",
]

if __name__ == "__main__":
    failures = []
    t0 = time.time()
    for script in SCRIPTS:
        print(f"\n{'=' * 70}\nRunning {script}\n{'=' * 70}")
        result = subprocess.run([sys.executable, str(HERE / script)], cwd=str(HERE))
        if result.returncode != 0:
            failures.append(script)
            print(f"\nFAILED at {script} (exit code {result.returncode}). Stopping.")
            break

    elapsed = time.time() - t0
    print(f"\n{'#' * 70}")
    if failures:
        print(f"PIPELINE FAILED at: {failures[0]}")
    else:
        print(f"PIPELINE COMPLETE. All {len(SCRIPTS)} scripts ran successfully in {elapsed:.1f}s.")
        print("Every internal verification assertion passed against the")
        print("manuscript's reported values.")
    print(f"{'#' * 70}")
    sys.exit(1 if failures else 0)
