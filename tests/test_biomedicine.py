"""
Unit tests for Space Biomedicine & Crew Physiology
Directly tests Level 4 Operation Lifeline Trauma Crisis dynamics.
"""

import pytest
from orbital_pulse.engine.biomedicine import BiomedicineEngine


def test_vance_trauma_stabilization():
    initial_vitals = {
        "heart_rate_bpm": 125,
        "blood_pressure_sys": 85,
        "blood_pressure_dia": 55,
        "blood_loss_ml": 650,
        "oxygen_sat_percent": 91.0,
        "radiation_dose_msv": 12.0
    }

    # Scenario: Trauma Pod fully powered (+950W), robotic coagulant active, AI assist active, no fast return
    res = BiomedicineEngine.simulate_trauma_crisis(
        vance_vitals=initial_vitals,
        active_mitigations=["trauma_pod", "iv_clotting_agent", "onboard_ai_assist"],
        power_allocated_medical_w=950.0,
        telemedicine_link_active=True,
        fast_return_selected=False,
        elapsed_seconds=120.0
    )

    assert res["stabilized"] is True
    assert res["patient_survived"] is True
    assert res["health_score"] > 50.0
    assert "Internal bleeding localized" in res["status_text"]


def test_vance_instant_burn_fatal_g_load():
    initial_vitals = {
        "heart_rate_bpm": 135,
        "blood_pressure_sys": 75,
        "blood_pressure_dia": 50,
        "blood_loss_ml": 850,
        "oxygen_sat_percent": 88.0,
        "radiation_dose_msv": 15.0
    }

    # Scenario: Fast-return selected (5.5G) WITHOUT anti-G suit and unpowered pod
    res = BiomedicineEngine.simulate_trauma_crisis(
        vance_vitals=initial_vitals,
        active_mitigations=[],
        power_allocated_medical_w=200.0,
        telemedicine_link_active=False,
        fast_return_selected=True,
        elapsed_seconds=60.0
    )

    assert res["stabilized"] is False
    assert res["patient_survived"] is False
    assert res["health_score"] == 0.0
    assert "CATASTROPHIC" in res["status_text"]
