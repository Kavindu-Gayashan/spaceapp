"""
Orbital Pulse - Physics & Orbital Mechanics Engine
Accurate astrodynamics, Keplerian orbits, solar flux attenuation,
eclipse calculations, and delta-V maneuvers.
"""

import math
import numpy as np
from typing import Dict, Any, Tuple

# Physical & Astrodynamical Constants
G = 6.67430e-11                  # Gravitational constant (m^3 kg^-1 s^-2)
M_EARTH = 5.9722e24              # Earth mass (kg)
R_EARTH = 6378.137               # Earth equatorial radius (km)
MU_EARTH = 3.986004418e14        # Earth gravitational parameter (m^3 s^-2)
MU_EARTH_KM = 398600.4418        # Earth gravitational parameter (km^3 s^-2)

M_MOON = 7.342e22                # Moon mass (kg)
R_MOON = 1737.4                  # Moon radius (km)
MU_MOON_KM = 4902.800066         # Moon gravitational parameter (km^3 s^-2)

SOLAR_CONSTANT_1AU = 1361.0      # Solar constant at 1 AU (W/m^2)
SIGMA_SB = 5.670374419e-8        # Stefan-Boltzmann constant (W m^-2 K^-4)
SPEED_OF_LIGHT = 299792458.0     # Speed of light (m/s)
AU_KM = 149597870.7              # 1 Astronomical Unit in km


class OrbitalPhysics:
    """Calculates orbital geometry, eclipse durations, velocities, and link budgets."""

    @staticmethod
    def get_orbit_parameters(altitude_km: float, body: str = "earth") -> Dict[str, float]:
        """Calculates orbital period, velocity, and eclipse fraction for a circular orbit."""
        if body.lower() == "moon":
            r_body = R_MOON
            mu = MU_MOON_KM
        else:
            r_body = R_EARTH
            mu = MU_EARTH_KM

        r_orbit = r_body + altitude_km
        # Orbital speed (km/s): v = sqrt(mu / r)
        v_orbit = math.sqrt(mu / r_orbit)
        # Orbital period (seconds): T = 2 * pi * sqrt(r^3 / mu)
        period_sec = 2.0 * math.pi * math.sqrt((r_orbit ** 3) / mu)

        # Eclipse fraction for circular orbit (geometric cylinder shadow model)
        # theta = arcsin(R_body / r_orbit)
        # eclipse duration = period * (2 * theta) / (2 * pi)
        ratio = min(1.0, max(0.0, r_body / r_orbit))
        theta = math.asin(ratio)
        eclipse_fraction = theta / math.pi
        t_eclipse = period_sec * eclipse_fraction
        t_sun = period_sec - t_eclipse

        return {
            "r_orbit_km": r_orbit,
            "v_orbit_km_s": round(v_orbit, 3),
            "period_sec": round(period_sec, 1),
            "period_min": round(period_sec / 60.0, 1),
            "eclipse_fraction": round(eclipse_fraction, 3),
            "t_eclipse_min": round(t_eclipse / 60.0, 1),
            "t_sun_min": round(t_sun / 60.0, 1),
        }

    @staticmethod
    def solar_flux_at_distance(distance_au: float) -> float:
        """
        Calculates solar irradiance (W/m^2) using the Inverse-Square Law:
        Flux(r) = Solar_Constant / r^2
        """
        if distance_au <= 0:
            return 0.0
        return SOLAR_CONSTANT_1AU / (distance_au ** 2)

    @staticmethod
    def calculate_hohmann_transfer(r1_km: float, r2_km: float, mu: float = MU_EARTH_KM) -> Dict[str, float]:
        """Calculates Hohmann transfer delta-V between two circular orbits."""
        a_transfer = (r1_km + r2_km) / 2.0
        v1 = math.sqrt(mu / r1_km)
        v2 = math.sqrt(mu / r2_km)

        # Delta-V at departure
        v_trans_dep = math.sqrt(mu * (2.0 / r1_km - 1.0 / a_transfer))
        delta_v1 = abs(v_trans_dep - v1)

        # Delta-V at arrival
        v_trans_arr = math.sqrt(mu * (2.0 / r2_km - 1.0 / a_transfer))
        delta_v2 = abs(v2 - v_trans_arr)

        total_delta_v = delta_v1 + delta_v2
        t_transfer = math.pi * math.sqrt((a_transfer ** 3) / mu)

        return {
            "delta_v1_km_s": round(delta_v1, 3),
            "delta_v2_km_s": round(delta_v2, 3),
            "total_delta_v_km_s": round(total_delta_v, 3),
            "transfer_time_hours": round(t_transfer / 3600.0, 2),
        }

    @staticmethod
    def thermal_equilibrium_temp(
        absorbed_solar_power_w: float,
        internal_dissipation_w: float,
        emissivity: float,
        radiating_area_m2: float
    ) -> float:
        """
        Calculates equilibrium temperature (in Kelvin):
        T_eq = ((Q_solar + Q_internal) / (epsilon * sigma * A))^(1/4)
        """
        if emissivity <= 0 or radiating_area_m2 <= 0:
            return 999.0
        q_total = max(0.0, absorbed_solar_power_w + internal_dissipation_w)
        temp_k = (q_total / (emissivity * SIGMA_SB * radiating_area_m2)) ** 0.25
        return round(temp_k, 2)

    @staticmethod
    def rf_link_budget(
        transmit_power_w: float,
        gain_tx_dbi: float,
        carrier_freq_ghz: float,
        distance_km: float,
        gain_rx_dbi: float = 45.0, # Standard DSN 34m/70m dish gain
        system_temp_k: float = 135.0
    ) -> Dict[str, float]:
        """
        Free Space Path Loss (FSPL) and signal-to-noise ratio margin.
        FSPL (dB) = 20*log10(d) + 20*log10(f) + 92.45
        (where d is in km, f is in GHz)
        """
        if distance_km <= 0:
            return {"fspl_db": 0.0, "snr_margin_db": 99.0, "achievable_rate_mbps": 1000.0}

        fspl_db = 20.0 * math.log10(distance_km) + 20.0 * math.log10(carrier_freq_ghz) + 92.45
        p_tx_dbw = 10.0 * math.log10(max(0.1, transmit_power_w))
        eirp_dbw = p_tx_dbw + gain_tx_dbi

        # Received Power Pr = EIRP + Gr - FSPL
        p_rx_dbw = eirp_dbw + gain_rx_dbi - fspl_db

        # Thermal noise power N = k * T * B (in dBW/Hz)
        k_boltzmann_db = -228.6
        n0_dbw_per_hz = k_boltzmann_db + 10.0 * math.log10(system_temp_k)

        # Carrier-to-noise density C/N0 = Pr - N0
        c_n0_db_hz = p_rx_dbw - n0_dbw_per_hz

        # For a target Bit Error Rate (BER 1e-6, Eb/N0 req ~ 10 dB)
        # Max data rate R (bps) = 10^((C/N0 - Eb/N0_req) / 10)
        req_eb_n0 = 10.0
        max_rate_log = (c_n0_db_hz - req_eb_n0) / 10.0
        max_rate_bps = 10.0 ** max_rate_log if max_rate_log > 0 else 100.0
        rate_mbps = min(500.0, max_rate_bps / 1.0e6)

        return {
            "fspl_db": round(fspl_db, 1),
            "eirp_dbw": round(eirp_dbw, 1),
            "received_power_dbw": round(p_rx_dbw, 1),
            "achievable_rate_mbps": round(rate_mbps, 3)
        }
