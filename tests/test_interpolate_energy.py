"""
tests/test_interpolate_energy.py
=================================
Tests for interpolate_energy() in src/data/processing.py.

Uses synthetic DataFrames (no data.xlsx dependency) to verify:
  - Midpoint interpolation
  - Clamping below minimum (value < 0)
  - Clamping above maximum (value > 1900)
  - On-row exact lookup
  - Boundary minimum (value == 0)
  - Boundary maximum (value == 1900)
  - Return type is always float (not numpy scalar)
  - Symmetric behaviour for depth_lookup columns
"""

import pandas as pd
import pytest

from src.data.processing import interpolate_energy


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures — synthetic lookup DataFrames (20 rows, linear scale)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture()
def tds_df() -> pd.DataFrame:
    """TDS lookup: tds_ppm = [0, 100, ..., 1900], ro_energy_kw = [0, 10, ..., 190]."""
    ppm = [i * 100 for i in range(20)]      # 0, 100, ..., 1900
    kw  = [i * 10  for i in range(20)]      # 0,  10, ...,  190
    return pd.DataFrame({"tds_ppm": ppm, "ro_energy_kw": kw})


@pytest.fixture()
def depth_df() -> pd.DataFrame:
    """Depth lookup: depth_m = [0, 100, ..., 1900], pump_energy_kw = [0, 10, ..., 190]."""
    depths = [i * 100 for i in range(20)]
    kw     = [i * 10  for i in range(20)]
    return pd.DataFrame({"depth_m": depths, "pump_energy_kw": kw})


# ──────────────────────────────────────────────────────────────────────────────
# TDS lookup tests
# ──────────────────────────────────────────────────────────────────────────────

class TestInterpolateEnergyTDS:
    """Tests using the TDS lookup (tds_ppm / ro_energy_kw)."""

    def test_boundary_minimum(self, tds_df):
        """Value == 0 returns the first row's energy (0.0 kW)."""
        result = interpolate_energy(0, tds_df, "tds_ppm", "ro_energy_kw")
        assert result == pytest.approx(0.0)

    def test_boundary_maximum(self, tds_df):
        """Value == 1900 returns the last row's energy (190.0 kW)."""
        result = interpolate_energy(1900, tds_df, "tds_ppm", "ro_energy_kw")
        assert result == pytest.approx(190.0)

    def test_clamp_below_minimum(self, tds_df):
        """Value < 0 is clamped to the first row's output (same as value=0)."""
        result = interpolate_energy(-50, tds_df, "tds_ppm", "ro_energy_kw")
        assert result == pytest.approx(0.0)

    def test_clamp_above_maximum(self, tds_df):
        """Value > 1900 is clamped to the last row's output (same as value=1900)."""
        result = interpolate_energy(2000, tds_df, "tds_ppm", "ro_energy_kw")
        assert result == pytest.approx(190.0)

    def test_midpoint_interpolation(self, tds_df):
        """Value == 950 interpolates between row 9 (900 ppm, 90 kW) and row 10 (1000 ppm, 100 kW).

        At 950 ppm the midpoint is 95.0 kW.
        """
        result = interpolate_energy(950, tds_df, "tds_ppm", "ro_energy_kw")
        assert result == pytest.approx(95.0)

    def test_on_row_lookup(self, tds_df):
        """Value == 100 falls exactly on row 1, returning 10.0 kW with no interpolation."""
        result = interpolate_energy(100, tds_df, "tds_ppm", "ro_energy_kw")
        assert result == pytest.approx(10.0)

    def test_return_type_is_float(self, tds_df):
        """Return value is a Python float, not a numpy scalar."""
        result = interpolate_energy(500, tds_df, "tds_ppm", "ro_energy_kw")
        assert isinstance(result, float)


# ──────────────────────────────────────────────────────────────────────────────
# Depth lookup tests (symmetric behaviour)
# ──────────────────────────────────────────────────────────────────────────────

class TestInterpolateEnergyDepth:
    """Tests using the depth lookup (depth_m / pump_energy_kw)."""

    def test_boundary_minimum_depth(self, depth_df):
        """Depth == 0 returns 0.0 kW."""
        result = interpolate_energy(0, depth_df, "depth_m", "pump_energy_kw")
        assert result == pytest.approx(0.0)

    def test_boundary_maximum_depth(self, depth_df):
        """Depth == 1900 returns 190.0 kW."""
        result = interpolate_energy(1900, depth_df, "depth_m", "pump_energy_kw")
        assert result == pytest.approx(190.0)

    def test_midpoint_interpolation_depth(self, depth_df):
        """Depth == 950 interpolates to 95.0 kW (same linear scale)."""
        result = interpolate_energy(950, depth_df, "depth_m", "pump_energy_kw")
        assert result == pytest.approx(95.0)

    def test_clamp_above_maximum_depth(self, depth_df):
        """Depth above 1900 is clamped to 190.0 kW."""
        result = interpolate_energy(9999, depth_df, "depth_m", "pump_energy_kw")
        assert result == pytest.approx(190.0)

    def test_return_type_is_float_depth(self, depth_df):
        """Return type is Python float for depth lookup too."""
        result = interpolate_energy(700, depth_df, "depth_m", "pump_energy_kw")
        assert isinstance(result, float)
