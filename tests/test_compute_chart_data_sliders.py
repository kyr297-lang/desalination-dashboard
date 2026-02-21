"""
tests/test_compute_chart_data_sliders.py
=========================================
Tests for the TDS and depth slider integration in compute_chart_data().

Verifies that:
  - Test A: tds_ppm=0, depth_m=0 produces baseline energy values (no offset at zero)
  - Test B: tds_ppm=950, depth_m=950 adds interpolated ro_kw to "Desalination" and
            pump_kw to "Water Extraction" for both mechanical and electrical systems
  - Test C: tds_ppm and depth_m default to 950 when omitted
  - Test D: backward-compatible — existing callers without tds_ppm/depth_m still work

Uses synthetic DataFrames only — does NOT read data.xlsx.
"""

import numpy as np
import pandas as pd
import pytest

from src.data.processing import compute_chart_data


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures — synthetic data dict
# ──────────────────────────────────────────────────────────────────────────────

def _make_equipment_df(rows: list[dict]) -> pd.DataFrame:
    """Build an equipment DataFrame from a list of dicts."""
    columns = ["name", "quantity", "cost_usd", "energy_kw", "land_area_m2", "lifespan_years"]
    return pd.DataFrame(rows, columns=columns)


def _make_tds_lookup() -> pd.DataFrame:
    """TDS lookup: tds_ppm=[0,100,...,1900], ro_energy_kw=[0,10,...,190]."""
    ppm = [i * 100 for i in range(20)]
    kw  = [i * 10  for i in range(20)]
    return pd.DataFrame({"tds_ppm": ppm, "ro_energy_kw": kw})


def _make_depth_lookup() -> pd.DataFrame:
    """Depth lookup: depth_m=[0,100,...,1900], pump_energy_kw=[0,10,...,190]."""
    depths = [i * 100 for i in range(20)]
    kw     = [i * 10  for i in range(20)]
    return pd.DataFrame({"depth_m": depths, "pump_energy_kw": kw})


def _make_battery_lookup() -> pd.DataFrame:
    """Minimal battery/tank lookup with 11 rows (fraction 0.0-1.0)."""
    fractions = [i * 0.1 for i in range(11)]
    # Simple linear total_cost: fraction * 100000
    costs = [f * 100_000 for f in fractions]
    return pd.DataFrame({
        "battery_fraction": fractions,
        "tank_fraction":    [1 - f for f in fractions],
        "battery_kwh":      [0.0] * 11,
        "tank_gal":         [0.0] * 11,
        "battery_cost":     costs,
        "tank_cost":        [0.0] * 11,
        "total_cost":       costs,
    })


@pytest.fixture()
def synthetic_data() -> dict:
    """Minimal data dict for testing compute_chart_data().

    - Mechanical: one "250kW aeromotor turbine " row with energy 500 kW
      (maps to "Water Extraction" stage in PROCESS_STAGES["mechanical"])
    - Electrical: one "Turbine" row with energy 600 kW
      (maps to "Water Extraction" stage in PROCESS_STAGES["electrical"])
    - Both have indefinite lifespan and minimal cost/land values
    - Battery lookup: 11 rows, linear cost
    - TDS lookup:   linear scale 0-190 kW over 0-1900 ppm
    - Depth lookup: linear scale 0-190 kW over 0-1900 m
    """
    mech = _make_equipment_df([
        {
            "name": "250kW aeromotor turbine ",
            "quantity": 1,
            "cost_usd": 100_000,
            "energy_kw": 500,
            "land_area_m2": 1000,
            "lifespan_years": "indefinite",
        }
    ])
    elec = _make_equipment_df([
        {
            "name": "Turbine",
            "quantity": 1,
            "cost_usd": 200_000,
            "energy_kw": 600,
            "land_area_m2": 2000,
            "lifespan_years": "indefinite",
        }
    ])
    misc = _make_equipment_df([])

    return {
        "mechanical":    mech,
        "electrical":    elec,
        "miscellaneous": misc,
        "battery_lookup": _make_battery_lookup(),
        "tds_lookup":    _make_tds_lookup(),
        "depth_lookup":  _make_depth_lookup(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Test A: zero TDS and depth produce no offset (baseline)
# ──────────────────────────────────────────────────────────────────────────────

class TestZeroOffset:
    """At tds_ppm=0 and depth_m=0, interpolated kW values are 0.0."""

    def test_mechanical_desalination_zero_tds(self, synthetic_data):
        """At TDS=0, no offset is added to Desalination stage."""
        cd = compute_chart_data(synthetic_data, tds_ppm=0, depth_m=0)
        mech_energy = cd["energy_breakdown"]["mechanical"]
        # "Desalination" key does not exist in the mechanical equipment rows
        # so it should only exist if ro_kw > 0. At tds=0, ro_kw=0, so
        # if the key exists it must be 0 (or it may be missing entirely).
        desalination_kw = mech_energy.get("Desalination", 0.0)
        assert desalination_kw == pytest.approx(0.0)

    def test_mechanical_water_extraction_zero_depth(self, synthetic_data):
        """At depth=0, pump_kw=0 so Water Extraction stage equals the base 500 kW."""
        cd = compute_chart_data(synthetic_data, tds_ppm=0, depth_m=0)
        mech_energy = cd["energy_breakdown"]["mechanical"]
        # "Water Extraction" stage has the turbine row (500 kW) plus pump_kw=0
        assert mech_energy.get("Water Extraction", 0.0) == pytest.approx(500.0)

    def test_electrical_desalination_zero_tds(self, synthetic_data):
        """At TDS=0, Desalination stage offset is 0 for electrical too."""
        cd = compute_chart_data(synthetic_data, tds_ppm=0, depth_m=0)
        elec_energy = cd["energy_breakdown"]["electrical"]
        desalination_kw = elec_energy.get("Desalination", 0.0)
        assert desalination_kw == pytest.approx(0.0)

    def test_electrical_water_extraction_zero_depth(self, synthetic_data):
        """At depth=0, pump_kw=0 so Water Extraction stage equals base 600 kW."""
        cd = compute_chart_data(synthetic_data, tds_ppm=0, depth_m=0)
        elec_energy = cd["energy_breakdown"]["electrical"]
        assert elec_energy.get("Water Extraction", 0.0) == pytest.approx(600.0)


# ──────────────────────────────────────────────────────────────────────────────
# Test B: midpoint TDS and depth add interpolated energy offsets
# ──────────────────────────────────────────────────────────────────────────────

class TestMidpointOffset:
    """At tds_ppm=950 and depth_m=950, interpolated offsets are 95.0 kW each."""

    def test_mechanical_desalination_midpoint(self, synthetic_data):
        """At TDS=950, ro_kw=95.0 is added to mechanical Desalination stage."""
        cd = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        mech_energy = cd["energy_breakdown"]["mechanical"]
        # Desalination: 0 (base) + 95 (ro offset) = 95.0
        assert mech_energy.get("Desalination", 0.0) == pytest.approx(95.0)

    def test_mechanical_water_extraction_midpoint(self, synthetic_data):
        """At depth=950, pump_kw=95.0 is added to mechanical Water Extraction."""
        cd = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        mech_energy = cd["energy_breakdown"]["mechanical"]
        # Water Extraction: 500 (turbine) + 95 (pump offset) = 595.0
        assert mech_energy.get("Water Extraction", 0.0) == pytest.approx(595.0)

    def test_electrical_desalination_midpoint(self, synthetic_data):
        """At TDS=950, ro_kw=95.0 is added to electrical Desalination stage."""
        cd = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        elec_energy = cd["energy_breakdown"]["electrical"]
        # Desalination: 0 (base, no electrical Desalination equipment in fixture) + 95 = 95.0
        assert elec_energy.get("Desalination", 0.0) == pytest.approx(95.0)

    def test_electrical_water_extraction_midpoint(self, synthetic_data):
        """At depth=950, pump_kw=95.0 is added to electrical Water Extraction."""
        cd = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        elec_energy = cd["energy_breakdown"]["electrical"]
        # Water Extraction: 600 (turbine) + 95 (pump offset) = 695.0
        assert elec_energy.get("Water Extraction", 0.0) == pytest.approx(695.0)


# ──────────────────────────────────────────────────────────────────────────────
# Test C: defaults are 950 when kwargs are omitted
# ──────────────────────────────────────────────────────────────────────────────

class TestDefaults:
    """tds_ppm and depth_m default to 950 when not passed."""

    def test_default_tds_equals_950(self, synthetic_data):
        """Calling with no tds_ppm/depth_m gives same result as tds_ppm=950, depth_m=950."""
        cd_default = compute_chart_data(synthetic_data)
        cd_explicit = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        # Compare Desalination in mechanical (most sensitive to TDS)
        assert (
            cd_default["energy_breakdown"]["mechanical"].get("Desalination", 0.0)
            == pytest.approx(
                cd_explicit["energy_breakdown"]["mechanical"].get("Desalination", 0.0)
            )
        )

    def test_default_depth_equals_950(self, synthetic_data):
        """Water Extraction stage with defaults matches explicit depth_m=950."""
        cd_default = compute_chart_data(synthetic_data)
        cd_explicit = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        assert (
            cd_default["energy_breakdown"]["mechanical"].get("Water Extraction", 0.0)
            == pytest.approx(
                cd_explicit["energy_breakdown"]["mechanical"].get("Water Extraction", 0.0)
            )
        )


# ──────────────────────────────────────────────────────────────────────────────
# Test D: backward-compatible — existing call signature still works
# ──────────────────────────────────────────────────────────────────────────────

class TestBackwardCompat:
    """Existing callers that do not pass tds_ppm / depth_m continue to work."""

    def test_call_without_new_kwargs(self, synthetic_data):
        """compute_chart_data(data, battery_fraction, years) returns a valid dict."""
        cd = compute_chart_data(synthetic_data, battery_fraction=0.5, years=10)
        assert "energy_breakdown" in cd
        assert "mechanical" in cd["energy_breakdown"]
        assert "electrical" in cd["energy_breakdown"]

    def test_return_keys_unchanged(self, synthetic_data):
        """Return dict still has all five expected top-level keys."""
        cd = compute_chart_data(synthetic_data)
        expected_keys = {"cost_over_time", "land_area", "turbine_count",
                         "energy_breakdown", "electrical_total_cost"}
        assert set(cd.keys()) == expected_keys
