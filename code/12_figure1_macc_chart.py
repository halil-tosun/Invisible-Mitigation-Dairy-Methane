"""
12_figure1_macc_chart.py -- Figure 1.

Marginal abatement cost comparison: ranks the four mitigation levers by
median $/ton CO2e (Table 3); bar width = national-scale abatement
potential (Table 8). Presented in a MACC-like stepped format for
familiarity, but the four levers have distinct baselines and mechanisms
(Table 4) rather than a single shared marginal-cost curve (Methods
Sec. 3.2).

Requires: 07_monte_carlo.py, 11_table8_national_scaling.py

Produces: figures/Figure1_MACC_stepped_chart.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import _paths as p

t3 = pd.read_csv(p.OUTPUT / "Table3_macc_comparison.csv")
t8 = pd.read_csv(p.OUTPUT / "Table8_national_scaling.csv")

# Map Table 8's lever labels onto Table 3's for a merge on lever identity (A/B/C/D)
t3["code"] = t3["lever"].str[0]
t8["code"] = t8["lever"].str[0]
merged = t3.merge(t8[["code", "achieved_median_MMT"]], on="code").sort_values("dollar_per_ton_median").reset_index(drop=True)

short_names = {
    "D": "D: Replacement\nrate", "A": "A: Dietary\nNDF",
    "B": "B: 3-NOP\n(interaction-corr.)", "C": "C: Fat\nsupplementation",
}
colors = {"A": "#4C72B0", "B": "#DD8452", "C": "#C44E52", "D": "#55A868"}

fig, ax = plt.subplots(figsize=(9, 6))
x_cursor = 0.0
lefts, widths, heights, labels, bar_colors = [], [], [], [], []
for _, row in merged.iterrows():
    width = row["achieved_median_MMT"]
    height = row["dollar_per_ton_median"]
    lefts.append(x_cursor)
    widths.append(width)
    heights.append(height)
    labels.append(short_names[row["code"]])
    bar_colors.append(colors[row["code"]])
    x_cursor += width

ax.bar(lefts, heights, width=widths, align="edge", color=bar_colors, edgecolor="black", linewidth=0.8)
label_offsets = {"A: Dietary\nNDF": 220, "D: Replacement\nrate": 0,
                  "B: 3-NOP\n(interaction-corr.)": 0, "C: Fat\nsupplementation": 0}
for left, width, height, label in zip(lefts, widths, heights, labels):
    extra = label_offsets.get(label, 0)
    va = "bottom" if height >= 0 else "top"
    ax.text(left + width / 2, height + (15 + extra if height >= 0 else -(15 + extra)),
            label, ha="center", va=va, fontsize=8.5)

ax.axhline(0, color="black", linewidth=1)
ax.set_xlabel("Cumulative national abatement potential (MMT CO2e/yr)\n"
              "(USDA NASS July 2026 dairy cow inventory x lever-specific adoption assumption)")
ax.set_ylabel("Net cost of abatement ($/ton CO2e)")
ax.set_title("Marginal Abatement Cost Comparison -- Enteric Methane Mitigation\n"
             "U.S. Dairy Production (national scale; median Monte Carlo estimates)")
ax.set_xlim(0, x_cursor * 1.05)
ymin, ymax = min(heights), max(heights)
yr = ymax - ymin
ax.set_ylim(ymin - 0.15 * yr, ymax + 0.15 * yr)
fig.tight_layout()

out_path = p.FIGURES / "Figure1_MACC_stepped_chart.png"
fig.savefig(out_path, dpi=150)
print(f"Saved: {out_path}")

# ---- Verification ----
assert list(merged["code"]) == ["D", "A", "B", "C"]
assert abs(x_cursor - 4.258) < 0.01, x_cursor
print("VERIFIED: bar order (D-A-B-C) and total width (4.258 MMT) match manuscript Figure 1.")
