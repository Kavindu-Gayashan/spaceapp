"""
Orbital Pulse - Space Biomedicine & Crew Physiology Engine
Simulates microgravity hemodynamic shifts, internal bleeding,
ECLSS oxygen/CO2 balances, trauma stabilization, and re-entry G-load limits.
"""

from typing import Dict, Any, List


class BiomedicineEngine:
    """Simulates crew vitals, microgravity trauma, and ECLSS life support."""

    @staticmethod
    def simulate_trauma_crisis(
        vance_vitals: Dict[str, Any],
        active_mitigations: List[str],
        power_allocated_medical_w: float,
        telemedicine_link_active: bool,
        fast_return_selected: bool,
        elapsed_seconds: float
    ) -> Dict[str, Any]:
        """
        Calculates Astronaut Vance's physiological status during the Level 4 Trauma Crisis:
        - Baseline: compound fracture + internal bleeding + approaching solar radiation
        - Pod activation requires +900W power
        - Ultrasound guidance requires active telemedicine comms or AI medical assist
        - Fast-return re-entry forces = 5.5G (fatal without anti-G suit & bleeding stabilized)
        """
        # Starting vitals
        heart_rate_bpm = vance_vitals.get("heart_rate_bpm", 125)
        blood_pressure_sys = vance_vitals.get("blood_pressure_sys", 85) # hypotensive due to bleeding
        blood_pressure_dia = vance_vitals.get("blood_pressure_dia", 55)
        blood_loss_ml = vance_vitals.get("blood_loss_ml", 650)
        oxygen_sat_percent = vance_vitals.get("oxygen_sat_percent", 91.0)
        eclss_o2_level_percent = vance_vitals.get("eclss_o2_level", 21.0)
        radiation_dose_msv = vance_vitals.get("radiation_dose_msv", 12.0)

        # Check conditions
        pod_powered = power_allocated_medical_w >= 850.0
        has_clotting_agent = "iv_clotting_agent" in active_mitigations or "trauma_pod" in active_mitigations
        has_ai_assist = "onboard_ai_assist" in active_mitigations or telemedicine_link_active
        has_anti_g_suit = "anti_g_countermeasure" in active_mitigations
        shelter_sealed = "radiation_storm_shelter" in active_mitigations

        # Physiological progression per minute of simulation
        dt_minutes = max(0.1, elapsed_seconds / 60.0)

        # Bleeding dynamics
        if pod_powered and has_clotting_agent and has_ai_assist:
            # Hemorrhage stabilized by robotic IV coagulant & localized compression
            bleeding_rate_ml_per_min = 0.5
            blood_loss_ml += int(bleeding_rate_ml_per_min * dt_minutes)
            heart_rate_bpm = max(75, heart_rate_bpm - int(6 * dt_minutes))
            blood_pressure_sys = min(118, blood_pressure_sys + int(8 * dt_minutes))
            blood_pressure_dia = min(78, blood_pressure_dia + int(5 * dt_minutes))
            oxygen_sat_percent = min(98.0, oxygen_sat_percent + 2.0 * dt_minutes)
            status_text = "Internal bleeding localized. Coagulation matrix holding. Vitals stabilizing."
            stabilized = True
        else:
            # Ongoing hemorrhage
            bleeding_rate_ml_per_min = 18.0
            blood_loss_ml += int(bleeding_rate_ml_per_min * dt_minutes)
            heart_rate_bpm = min(165, heart_rate_bpm + int(5 * dt_minutes))
            blood_pressure_sys = max(45, blood_pressure_sys - int(5 * dt_minutes))
            blood_pressure_dia = max(30, blood_pressure_dia - int(4 * dt_minutes))
            oxygen_sat_percent = max(70.0, oxygen_sat_percent - 1.5 * dt_minutes)
            status_text = "WARNING: Active arterial seepage. Tachycardia & progressive hemorrhagic shock!"
            stabilized = False

        # Re-entry G-Force check
        reentry_g_force = 5.5 if fast_return_selected else 1.2
        fatal_g_load = False
        if fast_return_selected:
            if not has_anti_g_suit and blood_loss_ml > 800:
                fatal_g_load = True
                status_text = "CATASTROPHIC: 5.5G Re-entry exceeded vascular structural threshold without anti-G suit! Patient lost."
            elif not stabilized:
                fatal_g_load = True
                status_text = "CATASTROPHIC: Re-entry acceleration triggered massive retroperitoneal rupture in unstabilized patient."

        # Radiation exposure
        if not shelter_sealed:
            radiation_dose_msv += 25.0 * dt_minutes
        else:
            radiation_dose_msv += 1.2 * dt_minutes

        # Surviving condition
        patient_survived = (blood_loss_ml < 1500) and (blood_pressure_sys > 50) and not fatal_g_load and (radiation_dose_msv < 250.0)

        # Health score (0-100)
        if not patient_survived:
            health_score = 0.0
        else:
            base_score = 100.0 - (blood_loss_ml / 20.0) - max(0, heart_rate_bpm - 75) * 0.3
            if stabilized:
                base_score += 15.0
            health_score = max(10.0, min(100.0, base_score))

        return {
            "heart_rate_bpm": heart_rate_bpm,
            "blood_pressure_sys": blood_pressure_sys,
            "blood_pressure_dia": blood_pressure_dia,
            "blood_loss_ml": blood_loss_ml,
            "oxygen_sat_percent": round(oxygen_sat_percent, 1),
            "radiation_dose_msv": round(radiation_dose_msv, 1),
            "reentry_g_force": reentry_g_force,
            "stabilized": stabilized,
            "patient_survived": patient_survived,
            "health_score": round(health_score, 1),
            "status_text": status_text,
            "pod_powered": pod_powered,
            "has_clotting_agent": has_clotting_agent,
            "has_ai_assist": has_ai_assist,
            "has_anti_g_suit": has_anti_g_suit,
            "shelter_sealed": shelter_sealed
        }
