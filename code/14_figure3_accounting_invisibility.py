"""
14_figure3_accounting_invisibility.py -- Figure 3.

National enteric CH4 abatement potential achieved (mechanistic model)
vs. Tier-1-representable under the IPCC Tier 1 emission-factor equation
(Eq. 5), by lever.

Classification rule (Methods Sec. 2.5): Levers A, B, C change diet
composition; Tier 1's emission factor is fixed per region/productivity
system and is not a function of diet, so their Tier 1-representable
share is 0. Lever D changes herd demography (replacement rate), which
Tier 1's population-count-based total-emissions equation would, in
principle, register at any tier, so its Tier 1-representable share is
treated as 100% (a structural classification, not a verified
quantitative decomposition; Methods Sec. 2.5 limitation).

Requires: 11_table8_national_scaling.py

Produces: figures/Figure3_accounting_invisibility.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import _paths as p

# Computed from the unrounded Monte Carlo national-scaling draws directly
# (not from Table 8's CSV, whose values are rounded to three decimals for
# display; using the CSV here would compound rounding error into the
# reported 91.4% figure).
draws = np.load(p.OUTPUT / "mc_raw_draws.npz")
order = ["A", "B", "C", "D"]

short_names = {
    "A": "A: Dietary NDF\nreduction", "B": "B: 3-NOP",
    "C": "C: Fat\nsupplementation", "D": "D: Replacement\nrate reduction",
}
tier1_reportable_fraction = {"A": 0.0, "B": 0.0, "C": 0.0, "D": 1.0}

achieved = np.array([np.median(draws[f"national_mmt_{code}"]) for code in order])
reportable = np.array([achieved[i] * tier1_reportable_fraction[code] for i, code in enumerate(order)])
invisible = achieved - reportable
labels = [short_names[code] for code in order]
x = np.arange(len(labels))
width = 0.55

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.bar(x, reportable, width, label="Tier 1-representable (structural classification)",
       color="#55A868", edgecolor="black", linewidth=0.8)
ax.bar(x, invisible, width, bottom=reportable, label="Not Tier 1-representable",
       color="#C44E52", edgecolor="black", linewidth=0.8, hatch="///")

for i, (r, inv, tot) in enumerate(zip(reportable, invisible, achieved)):
    ax.text(i, tot + 0.12, f"{tot:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    if inv > 0.02:
        ax.text(i, r + inv / 2, f"{inv:.2f}", ha="center", va="center", fontsize=8, color="white")
    if r > 0.02:
        ax.text(i, r / 2, f"{r:.2f}", ha="center", va="center", fontsize=8, color="white")

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel("National abatement potential (MMT CO$_2$e yr$^{-1}$)", fontsize=10)
ax.set_title("Achieved vs. Tier-1-representable enteric CH$_4$ abatement, by lever\n"
             "(median estimates; U.S. dairy herd, illustrative of Tier-1-reporting jurisdictions)",
             fontsize=10)
ax.legend(loc="upper right", fontsize=8.5, framealpha=0.95)
ax.spines[["top", "right"]].set_visible(False)

total_achieved = achieved.sum()
total_reportable = reportable.sum()
pct_invisible = 100 * (total_achieved - total_reportable) / total_achieved
fig.text(0.5, -0.02,
          f"Total: {total_achieved:.2f} MMT CO$_2$e yr$^{{-1}}$ achieved; "
          f"{total_reportable:.2f} MMT ({100-pct_invisible:.1f}%) Tier 1-representable; "
          f"{total_achieved - total_reportable:.2f} MMT ({pct_invisible:.1f}%) not Tier 1-representable.",
          ha="center", fontsize=9, style="italic")

plt.tight_layout()
out_path = p.FIGURES / "Figure3_accounting_invisibility.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Total achieved: {total_achieved:.3f} MMT CO2e/yr")
print(f"Total Tier-1-reportable: {total_reportable:.3f} MMT CO2e/yr ({100-pct_invisible:.1f}%)")
print(f"Total not Tier-1-representable: {total_achieved - total_reportable:.3f} MMT CO2e/yr ({pct_invisible:.1f}%)")
print(f"Saved: {out_path}")

# ---- Verification against manuscript Sec. 3.4 / Table 8 ----
assert round(total_achieved, 3) == 4.258, total_achieved
assert round(pct_invisible, 1) == 91.4, pct_invisible
print("VERIFIED: matches manuscript Sec. 3.4 (4.258 MMT total; 91.4% not represented).")
