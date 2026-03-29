"""
tests/test_compute_chart_data_sliders.py
=========================================
Tests for the TDS and depth slider integration in compute_chart_data().

Verifies that:
  - Test A: tds_ppm=0, depth_m=0 produces baseline energy values (SUBSYSTEM_POWER constants, no offset)
  - Test B: tds_ppm=950, depth_m=950 adds interpolated ro_kw to "RO Desalination" and
            pump_kw to "Groundwater Extraction" for both mechanical and electrical systems
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
    columns = ["name", "quantity", "cost_usd", "lifespan_years"]
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

    - Mechanical: one "1 MW Aeromotor Turbine" row (4-column schema)
    - Electrical: one "1.5 MW Turbine (GE Vernova 1.5sle)" row (4-column schema)
    - Hybrid: empty DataFrame (4-column schema)
    - Battery lookup: 11 rows, linear cost
    - TDS lookup:   linear scale 0-190 kW over 0-1900 ppm
    - Depth lookup: linear scale 0-190 kW over 0-1900 m

    Energy values come from SUBSYSTEM_POWER constants in src/config.py,
    not from equipment rows — the 4-column schema has no energy_kw column.
    """
    mech = _make_equipment_df([
        {
            "name": "1 MW Aeromotor Turbine",
            "quantity": 1,
            "cost_usd": 100_000,
            "lifespan_years": "indefinite",
        }
    ])
    elec = _make_equipment_df([
        {
            "name": "1.5\u202fMW Turbine (GE Vernova 1.5sle)",
            "quantity": 1,
            "cost_usd": 1_000_000,
            "lifespan_years": "indefinite",
        }
    ])
    hybrid = _make_equipment_df([])

    return {
        "mechanical":     mech,
        "electrical":     elec,
        "hybrid":         hybrid,
        "battery_lookup": _make_battery_lookup(),
        "tds_lookup":     _make_tds_lookup(),
        "depth_lookup":   _make_depth_lookup(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Test A: zero TDS and depth produce base SUBSYSTEM_POWER values (no offset)
# ──────────────────────────────────────────────────────────────────────────────

class TestZeroOffset:
    """At tds_ppm=0 and depth_m=0, interpolated kW values are 0.0, so energy
    equals the SUBSYSTEM_POWER base constants exactly."""

    def test_mechanical_ro_desalination_zero_tds(self, synthetic_data):
        """At TDS=0, no offset added; RO Desalination equals SUBSYSTEM_POWER base 311.49."""
        cd = compute_chart_data(synthetic_data, tds_ppm=0, depth_m=0)
        mech_energy = cd["energy_breakdown"]["mechanical"]
        # Base RO Desalination from SUBSYSTEM_POWER: 311.49, no TDS offset at 0
        assert mech_energy["RO Desalination"] == pytest.approx(311.49)

    def test_mechanical_groundwater_zero_depth(self, synthetic_data):
        """At depth=0, no offset added; Groundwater Extraction equals SUBSYSTEM_POWER base 172.9."""
        cd = compute_chart_data(synthetic_data, tds_ppm=0, depth_m=0)
        mech_energy = cd["energy_breakdown"]["mechanical"]
        # Base Groundwater Extraction from SUBSYSTEM_POWER: 172.9, no depth offset at 0
        assert mech_energy["Groundwater Extraction"] == pytest.approx(172.9)

    def test_electrical_ro_desalination_zero_tds(self, synthetic_data):
        """At TDS=0, RO Desalination offset is 0 for electrical too."""
        cd = compute_chart_data(synthetic_data, tds_ppm=0, depth_m=0)
        elec_energy = cd["energy_breakdown"]["electrical"]
        assert elec_energy["RO Desalination"] == pytest.approx(311.49)

    def test_electrical_groundwater_zero_depth(self, synthetic_data):
        """At depth=0, Groundwater Extraction offset is 0 for electrical too."""
        cd = compute_chart_data(synthetic_data, tds_ppm=0, depth_m=0)
        elec_energy = cd["energy_breakdown"]["electrical"]
        assert elec_energy["Groundwater Extraction"] == pytest.approx(172.9)


# ──────────────────────────────────────────────────────────────────────────────
# Test B: midpoint TDS and depth add interpolated energy offsets
# ──────────────────────────────────────────────────────────────────────────────

class TestMidpointOffset:
    """At tds_ppm=950 and depth_m=950, interpolated offsets are 95.0 kW each."""

    def test_mechanical_ro_desalination_midpoint(self, synthetic_data):
        """At TDS=950, ro_kw=95.0 is added to mechanical RO Desalination stage."""
        cd = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        mech_energy = cd["energy_breakdown"]["mechanical"]
        # RO Desalination: 311.49 (base) + 95.0 (TDS offset) = 406.49
        assert mech_energy["RO Desalination"] == pytest.approx(406.49)

    def test_mechanical_groundwater_midpoint(self, synthetic_data):
        """At depth=950, pump_kw=95.0 is added to mechanical Groundwater Extraction."""
        cd = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        mech_energy = cd["energy_breakdown"]["mechanical"]
        # Groundwater Extraction: 172.9 (base) + 95.0 (depth offset) = 267.9
        assert mech_energy["Groundwater Extraction"] == pytest.approx(267.9)

    def test_electrical_ro_desalination_midpoint(self, synthetic_data):
        """At TDS=950, ro_kw=95.0 is added to electrical RO Desalination stage."""
        cd = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        elec_energy = cd["energy_breakdown"]["electrical"]
        assert elec_energy["RO Desalination"] == pytest.approx(406.49)

    def test_electrical_groundwater_midpoint(self, synthetic_data):
        """At depth=950, pump_kw=95.0 is added to electrical Groundwater Extraction."""
        cd = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        elec_energy = cd["energy_breakdown"]["electrical"]
        assert elec_energy["Groundwater Extraction"] == pytest.approx(267.9)


# ──────────────────────────────────────────────────────────────────────────────
# Test C: defaults are 950 when kwargs are omitted
# ──────────────────────────────────────────────────────────────────────────────

class TestDefaults:
    """tds_ppm and depth_m default to 950 when not passed."""

    def test_default_tds_equals_950(self, synthetic_data):
        """Calling with no tds_ppm/depth_m gives same result as tds_ppm=950, depth_m=950."""
        cd_default = compute_chart_data(synthetic_data)
        cd_explicit = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        # Compare RO Desalination in mechanical (most sensitive to TDS)
        assert (
            cd_default["energy_breakdown"]["mechanical"]["RO Desalination"]
            == pytest.approx(
                cd_explicit["energy_breakdown"]["mechanical"]["RO Desalination"]
            )
        )

    def test_default_depth_equals_950(self, synthetic_data):
        """Groundwater Extraction stage with defaults matches explicit depth_m=950."""
        cd_default = compute_chart_data(synthetic_data)
        cd_explicit = compute_chart_data(synthetic_data, tds_ppm=950, depth_m=950)
        assert (
            cd_default["energy_breakdown"]["mechanical"]["Groundwater Extraction"]
            == pytest.approx(
                cd_explicit["energy_breakdown"]["mechanical"]["Groundwater Extraction"]
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
        """Return dict has exactly three expected top-level keys."""
        cd = compute_chart_data(synthetic_data)
        expected_keys = {"cost_over_time", "energy_breakdown", "electrical_total_cost"}
        assert set(cd.keys()) == expected_keys
