"""
Unit tests for Orbital Physics & Systems Calculations
"""

import pytest
from orbital_pulse.engine.physics import OrbitalPhysics


def test_leo_orbital_parameters():
    # 550 km circular orbit around Earth
    params = OrbitalPhysics.get_orbit_parameters(altitude_km=550.0, body="earth")
    assert 90.0 < params["period_min"] < 100.0
    assert 7.0 < params["v_orbit_km_s"] < 8.0
    assert 0.30 < params["eclipse_fraction"] < 0.40
    assert 30.0 < params["t_eclipse_min"] < 40.0


def test_inverse_square_solar_flux():
    # Solar flux at 1 AU should be ~1361 W/m^2
    flux_1au = OrbitalPhysics.solar_flux_at_distance(1.0)
    assert abs(flux_1au - 1361.0) < 1.0

    # At 2 AU it should be 1361 / 4 = 340.25 W/m^2
    flux_2au = OrbitalPhysics.solar_flux_at_distance(2.0)
    assert abs(flux_2au - (1361.0 / 4.0)) < 1.0

    # At 2.2 AU (Asteroid Belt in Level 5)
    flux_2_2au = OrbitalPhysics.solar_flux_at_distance(2.2)
    assert abs(flux_2_2au - (1361.0 / (2.2 ** 2))) < 1.0


def test_hohmann_transfer():
    # Transfer from 500 km LEO to 35,786 km GEO
    r1 = 6378.137 + 500.0
    r2 = 6378.137 + 35786.0
    transfer = OrbitalPhysics.calculate_hohmann_transfer(r1, r2)
    assert 3.5 < transfer["total_delta_v_km_s"] < 4.2
    assert 5.0 < transfer["transfer_time_hours"] < 5.5


def test_link_budget():
    # 25W Ka-Band from L2 (1.5M km)
    link = OrbitalPhysics.rf_link_budget(
        transmit_power_w=25.0,
        gain_tx_dbi=38.0,
        carrier_freq_ghz=32.0,
        distance_km=1500000.0
    )
    assert link["fspl_db"] > 200.0
    assert link["achievable_rate_mbps"] > 0.0
