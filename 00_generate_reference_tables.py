# ============================================================
# 00_generate_reference_tables.py
#
# One-time generation of small reference tables used by
# Notebook 02. These are *synthetic* but chosen to be
# plausible and literature-inspired:
#
#   - trial_phase_cost_factors.csv:
#       approximate relative cost by phase
#
#   - region_enrollment_multipliers.csv:
#       rough enrollment efficiency multipliers by region
#
# After generation, these files should be treated as
# fixed reference data (just like a warehouse dimension).
# ============================================================

from pathlib import Path
import pandas as pd

ref_dir = Path("data/external")
ref_dir.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 1) Phase-level cost factors
#    (relative multipliers, not absolute $$$)
# ------------------------------------------------------------
phase_cost_path = ref_dir / "trial_phase_cost_factors.csv"

if not phase_cost_path.exists():
    phase_rows = [
        # phase,             cost_multiplier
        ("Early Phase 1",    0.8),
        ("Phase 1",          1.0),
        ("Phase 1/Phase 2",  1.5),
        ("Phase 2",          2.0),
        ("Phase 2/Phase 3",  3.0),
        ("Phase 3",          4.0),
        ("Phase 4",          2.5),
        ("N/A",              1.0),
        ("None",             1.0),
    ]
    df_phase = pd.DataFrame(phase_rows, columns=["phase", "cost_multiplier"])
    df_phase.to_csv(phase_cost_path, index=False)
    print(f"Created {phase_cost_path} with {len(df_phase)} rows.")
else:
    print(f"{phase_cost_path} already exists; not overwriting.")

# ------------------------------------------------------------
# 2) Region-level enrollment multipliers
#    (baseline = 1.0, others relative to that)
# ------------------------------------------------------------
region_mult_path = ref_dir / "region_enrollment_multipliers.csv"

if not region_mult_path.exists():
    region_rows = [
        # region_label,              enrollment_multiplier
        ("North America",           1.00),
        ("Western Europe",          0.95),
        ("Eastern Europe",          1.05),
        ("Asia-Pacific",            1.10),
        ("Latin America",           0.90),
        ("Middle East & Africa",    0.85),
        ("Global / Multi-Region",   1.00),
    ]
    df_region = pd.DataFrame(region_rows, columns=["region_label", "enrollment_multiplier"])
    df_region.to_csv(region_mult_path, index=False)
    print(f"Created {region_mult_path} with {len(df_region)} rows.")
else:
    print(f"{region_mult_path} already exists; not overwriting.")

print("Reference table generation complete.")
