"""
Unit tests for Systems Engineering & Gates Engine
Directly tests Section 6 equations and bottlenecks.
"""

import pytest
from orbital_pulse.engine.systems import SystemsEngine
from orbital_pulse.models.campaign import CAMPAIGN_LEVELS
from orbital_pulse.models.components import COMPONENTS_BY_STATION


def test_level_1_systems_evaluation():
    scenario = CAMPAIGN_LEVELS[1]

    # Select valid configuration
    st1 = next(c for c in COMPONENTS_BY_STATION["station_1"] if c["id"] == "lv_falcon_rideshare")
    st2 = next(c for c in COMPONENTS_BY_STATION["station_2"] if c["id"] == "pwr_deployable_wings")
    st3 = next(c for c in COMPONENTS_BY_STATION["station_3"] if c["id"] == "pay_swir_camera")
    st4 = next(c for c in COMPONENTS_BY_STATION["station_4"] if c["id"] == "comms_sband_patch")

    selected = {
        "station_1": st1,
        "station_2": st2,
        "station_3": st3,
        "station_4": st4
    }

    eval_res = SystemsEngine.evaluate_mission(scenario, selected)

    assert eval_res["mass_pass"] is True
    assert eval_res["budget_pass"] is True
    assert eval_res["data_pass"] is True
    assert eval_res["power_pass"] is True
    assert eval_res["all_passed"] is True
    assert eval_res["base_engineering_score"] > 0
    assert len(eval_res["bottlenecks"]) == 0


def test_mass_overrun_bottleneck():
    scenario = CAMPAIGN_LEVELS[1] # max mass 12 kg

    # Intentionally choose heavy hardware that exceeds 12 kg
    heavy_st2 = {"id": "heavy_test", "name": "Heavy Test", "mass_kg": 25.0, "cost_m": 0.5}

    selected = {
        "station_1": None,
        "station_2": heavy_st2,
        "station_3": None,
        "station_4": None
    }

    eval_res = SystemsEngine.evaluate_mission(scenario, selected)
    assert eval_res["mass_pass"] is False
    assert eval_res["all_passed"] is False
    assert any("Mass exceeded" in b["issue"] for b in eval_res["bottlenecks"])
