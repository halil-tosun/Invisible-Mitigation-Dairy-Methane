"""
_paths.py -- Shared path configuration and constants for this repository.

Invisible Mitigation: Why Default Methane Accounting Cannot See What
Dairy Farmers Do (Tosun).

Not run directly. Imported by every numbered script in code/.
"""
from pathlib import Path

# ---- Repository-relative paths ----
ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "output"
FIGURES = ROOT / "figures"

for p in (DATA_PROCESSED, OUTPUT, FIGURES):
    p.mkdir(parents=True, exist_ok=True)

# ============================================================
# Fixed animal / production assumptions (Table 1, Panel A)
# ============================================================
BW = 650.0                     # body weight, kg
MILK = 38.0                    # milk yield, kg/d
FAT = 3.8                      # milk fat, %
PROT_MILK = 3.1                # milk true protein, %
NEM_COEF = 0.080                # NEmaintenance coefficient, Mcal/kg BW^0.75
NEL_PER_KG_MILK = 0.74          # NEl per kg milk, Mcal/kg
MILK_PRICE_CWT = 20.70          # USD/cwt. USDA ERS, All Milk Price, June 2026
                                 # annual forecast (Livestock, Dairy, and
                                 # Poultry Outlook). Reference/descriptive
                                 # parameter only -- milk price does not enter
                                 # the net-cost calculation for Levers A, B,
                                 # or D, and enters Lever C only through the
                                 # butterfat component price below (Methods
                                 # Sec. 2.3).
NASS_DAIRY_COW_INVENTORY_HEAD = 9_650_000  # USDA NASS Cattle report, released
                                             # July 24, 2026 (as-of July 1, 2026)

# Fixed per-cow daily supplement/premix cost, embedded in the feed-cost term
# of every lever's net-cost calculation (see _calc.py, feed_cost_d). This is
# an author-specified modeling assumption, held constant across BAU and all
# intervention scenarios, and therefore cancels out of every *change* in
# feed cost reported in the manuscript; it is not itemized as a separate
# row in Table 1 because it is not a lever-specific or literature-sourced
# parameter, but it is disclosed here in full for computational transparency.
PREMIX_USD_PER_COW_DAY = 0.55

# ============================================================
# Methane / GWP constants
# ============================================================
MJ_PER_KG_CH4 = 55.65           # gross energy value of methane (Brouwer, 1965)
GWP100_CH4 = 27.0               # 100-yr GWP, biogenic CH4, kg CO2e/kg CH4
                                 # (IPCC AR6 WG1, Forster et al., 2021, Table
                                 # 7.15). This is the methane-oxidation-to-CO2-
                                 # adjusted, biogenic-specific value, distinct
                                 # from the undifferentiated, oxidation-
                                 # unadjusted value (27.9) reported for
                                 # methane generically in AR6 Table 7.SM.7.
                                 # The biogenic-specific value (27.0) is the
                                 # scientifically appropriate choice for
                                 # enteric (biogenic) methane and is used
                                 # throughout (Methods Sec. 2.2).

# ============================================================
# Rumen health constraints (shared across Levers A and C)
# ============================================================
FORAGE_NDF_MIN = 0.19           # NRC (2001) / NASEM (2021), % DM
TOTAL_NDF_MIN = 0.25            # NRC (2001), % DM
NFC_MAX = 0.40                  # NRC (2001), % DM
RAEE_FAT_MAX = 0.055            # Lever C rumen-available fat ceiling, % DM
                                 # (Honan et al., 2022)

# ============================================================
# Optimization bounds (Lever A ration formulation; author design
# choices, not literature-derived -- disclosed as such in Methods
# Sec. 2.3 / Table 1 footnote)
# ============================================================
CP_MIN, CP_MAX = 0.160, 0.185   # NASEM (2021) dairy CP range, % DM
FORAGE_MIN, FORAGE_MAX = 0.35, 0.65
SINGLE_FORAGE_CAP = 0.45
CORNGRAIN_CAP = 0.40
SBM_CAP = 0.20

# ============================================================
# Lever A: Dietary NDF reduction
# ============================================================
# Nine candidate nominal NDF floors evaluated (Methods Sec. 2.3); the
# realized optimum converges to 33.67% DM at every floor from 28% to 32%
# DM, because the NFC ceiling binds before the nominal floor does.
NDF_FLOOR_POINTS = [0.28, 0.30, 0.32, 0.34, 0.341, 0.35, 0.36, 0.37, 0.372]
NASEM_MEAN_NDF = 0.341           # NASEM (2021) published U.S. lactating-cow
                                  # mean, 34.1 +/- 4.6% DM -- the BAU
                                  # reference point (Table 1, Panel A).

# ============================================================
# Lever B: 3-nitrooxypropanol (3-NOP)
# ============================================================
# Kebreab et al. (2022). J. Dairy Sci. 106:927-936.
# doi:10.3168/jds.2022-22211
# CH4 intensity change (%) = -33.0 - 0.275*(dose-70.5) + 0.723*(NDF-32.9)
# dose in mg/kg DM; NDF in % DM.
KEBREAB_INTERCEPT = -33.0
KEBREAB_DOSE_COEF = -0.275
KEBREAB_DOSE_MEAN = 70.5         # mg/kg DM
KEBREAB_NDF_COEF = 0.723
KEBREAB_NDF_MEAN = 32.9          # % DM
KEBREAB_VALID_DOSE_RANGE = (40.0, 130.0)   # mg/kg DM
KEBREAB_VALID_NDF_RANGE = (26.5, 43.5)     # % DM

NOP_COST_USD_PER_COW_YEAR = (93.0, 105.0)          # DSM-linked estimate
NOP_COST_INDEPENDENT_USD_PER_COW_YEAR = 128.32     # independent/skeptical
                                                     # estimate, used as a
                                                     # sensitivity bound

# ============================================================
# Lever C: Rumen-available fat supplementation
# ============================================================
# Scope limited to rumen-available (unprotected) fat sources; calcium-soap
# and hydrogenated (bypass) fat sources are excluded by mechanism (Methods
# Sec. 2.3).
FAT_CH4_REDUCTION_PCT_PER_PCT_DM_MEAN = 3.77     # primary point estimate
                                                   # (de Ondarza et al., 2024,
                                                   # 35-study meta-analysis)
FAT_CH4_REDUCTION_PCT_PER_PCT_DM_UPPER = 19.5    # alternative higher-effect
                                                   # estimate (Hristov et al.,
                                                   # 2022, multi-species
                                                   # meta-analysis); evaluated
                                                   # separately (Table 5,
                                                   # Table 6), not pooled into
                                                   # the primary Monte Carlo
                                                   # distribution.
FAT_MILK_FAT_PCT_LOSS_PCT = 7.8     # relative milk-fat PERCENTAGE reduction
                                      # (de Ondarza et al., 2024)
FAT_MILK_FAT_YIELD_LOSS_PCT = 6.0   # relative milk-fat YIELD (kg fat/d)
                                      # reduction (de Ondarza et al., 2024);
                                      # the same source does not report
                                      # overall milk yield (kg/d) as
                                      # significantly affected.
BUTTERFAT_PRICE_USD_PER_KG = 3.5107  # USDA AMS Advanced Butterfat Pricing
                                       # Factor, January 2026: $1.5921/lb.

# ============================================================
# Lever D: Replacement-rate reduction
# ============================================================
# Baseline (31%) and target (21%) replacement rate: USDA/NAHMS (2018),
# Dairy 2014: Health and Management Practices on U.S. Dairy Operations
# (northeastern U.S. average cull rate).
REPLACEMENT_RATE_BAU = 0.31
REPLACEMENT_RATE_TARGET = 0.21

# Emission-intensity reduction per 10-percentage-point replacement-rate
# reduction, triangulated from two independent European herd-simulation
# studies: Chen et al. (2026, Denmark) and Sommerseth et al. (2024,
# Norway). No U.S.-specific coefficient was identified in the literature
# (geographic-transferability limitation, disclosed in Methods Sec. 2.3).
REPLACEMENT_EI_REDUCTION_PCT_PER_10PT = (2.7, 5.0)

HEIFER_REARING_COST_USD = (1594.0, 1919.0)  # dry-lot to confinement range
                                              # (Hawkins et al., 2020),
                                              # birth-to-calving

# ============================================================
# Carbon price scenarios (Table 1, Panel B)
# ============================================================
CARBON_PRICE_LOW_USD_PER_TON = 6.34     # Ecosystem Marketplace SOVCM 2025
CARBON_PRICE_MID_USD_PER_TON = 30.0     # First verified dairy carbon
                                          # transaction, quoted via Agri-Pulse
CARBON_PRICE_HIGH_RANGE_USD_PER_TON = (45.0, 60.0)  # General premium/
                                                       # ICVCM-screened
                                                       # corporate market
                                                       # ceiling; not
                                                       # livestock-specific
                                                       # (disclosed limitation)

# ============================================================
# Monte Carlo specification
# ============================================================
MC_ITERATIONS = 10_000
MC_SEED = 42

# ============================================================
# National scaling (Table 8)
# ============================================================
# Lever-specific adoption-rate point estimates and ranges. Illustrative,
# expert-judgment assumptions following USDA/ICF (2023)'s own methodology
# for adoption-rate estimation (their published practice-adoption
# assumptions range 10-50%), not survey-derived rates (Methods Sec. 2.8).
ADOPTION_RATE = {
    "A": 0.60,  # dietary reformulation -- low-cost, no new infrastructure
    "B": 0.25,  # 3-NOP -- new technology, feeding-system/verification barriers
    "C": 0.40,  # fat supplementation -- already common practice on many farms
    "D": 0.30,  # reproductive/replacement management -- requires genetic/
                # breeding investment
}

# Adoption-rate uncertainty range (used to sample a triangular distribution
# in the Monte Carlo national-scaling calculation; Methods Sec. 2.8).
ADOPTION_RATE_RANGE = {
    "A": (0.50, 0.70),
    "B": (0.15, 0.35),
    "C": (0.30, 0.50),
    "D": (0.20, 0.40),
}
