"""
Orbital Pulse - Systems Engineering & Trade-Off Engine
Calculates real-time mass margins, power grids, battery depth-of-discharge (DoD),
thermal control limits, and onboard buffer overflow risks.
Directly implements Section 6 of the Master Project Proposal.
"""

from typing import Dict, List, Any, Optional
import math


class SystemsEngine:
    """Evaluates multi-domain spacecraft system constraints and trade-offs."""

    @staticmethod
    def evaluate_mission(
        scenario_config: Dict[str, Any],
        selected_components: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes systems evaluation against scenario limits:
        - Mass & Launch Vehicle Compatibility Gate
        - Orbital Energy & Eclipse Battery Balance
        - Thermal limits & cryocooling
        - Data Generation vs Downlink Bottleneck
        - Crew Life Support & Biomedical Safety Margin
        - Financial Budget Limit
        """
        # Base constraints from scenario
        max_mass_kg = scenario_config.get("max_mass_kg", 500.0)
        budget_cap_m = scenario_config.get("budget_cap_m", 10.0)
        sun_distance_au = scenario_config.get("sun_distance_au", 1.0)
        t_orbit_min = scenario_config.get("t_orbit_min", 95.0)
        t_eclipse_min = scenario_config.get("t_eclipse_min", 35.0)
        t_sun_min = max(1.0, t_orbit_min - t_eclipse_min)
        t_contact_hours = scenario_config.get("t_contact_hours_per_day", 4.0)

        # Aggregate component contributions
        total_mass = scenario_config.get("base_bus_mass_kg", 0.0)
        total_cost_m = scenario_config.get("base_bus_cost_m", 0.0)
        solar_generation_1au_w = 0.0
        rtg_power_w = 0.0
        battery_capacity_wh = scenario_config.get("base_bus_battery_wh", 30.0)
        battery_max_dod = 0.70  # Standard 70% depth of discharge limit
        power_draw_day_w = scenario_config.get("base_idle_power_w", 5.0)
        power_draw_eclipse_w = scenario_config.get("base_idle_power_w", 5.0)
        cooling_capability_k = 300.0 # Standard ambient baseline
        heat_load_w = 10.0

        daily_data_gen_gb = 0.0
        downlink_rate_mbps = 0.1
        onboard_storage_gb = 16.0

        propellant_delta_v_m_s = 0.0
        req_delta_v_m_s = scenario_config.get("req_delta_v_m_s", 0.0)

        # Bio & Science yields
        science_yield_pts = 0.0
        bio_health_pts = 100.0
        active_mitigations = []

        # Iterate selected components across all 4 stations
        for station, comp in selected_components.items():
            if not comp or not isinstance(comp, dict):
                continue

            total_mass += comp.get("mass_kg", 0.0)
            total_cost_m += comp.get("cost_m", 0.0)

            # Power Generation
            if comp.get("type") == "solar":
                solar_generation_1au_w += comp.get("power_gen_w", 0.0)
            elif comp.get("type") == "rtg":
                rtg_power_w += comp.get("power_gen_w", 0.0)
            elif comp.get("type") == "battery":
                battery_capacity_wh += comp.get("battery_capacity_wh", 0.0)
                if "max_dod" in comp:
                    battery_max_dod = comp.get("max_dod", 0.70)

            # Power Consumption
            p_day = comp.get("power_draw_day_w", comp.get("power_draw_w", 0.0))
            p_ecl = comp.get("power_draw_eclipse_w", comp.get("power_draw_w", 0.0))
            power_draw_day_w += p_day
            power_draw_eclipse_w += p_ecl

            # Thermal
            if "min_temp_k" in comp:
                cooling_capability_k = min(cooling_capability_k, comp.get("min_temp_k"))
            heat_load_w += comp.get("heat_load_w", 0.0)

            # Data
            daily_data_gen_gb += comp.get("data_gen_gb_per_day", 0.0)
            if "downlink_rate_mbps" in comp:
                downlink_rate_mbps = max(downlink_rate_mbps, comp.get("downlink_rate_mbps", 0.1))
            if "storage_gb" in comp:
                onboard_storage_gb += comp.get("storage_gb", 0.0)

            # Propulsion
            propellant_delta_v_m_s += comp.get("delta_v_m_s", 0.0)

            # Science / Bio
            science_yield_pts += comp.get("science_pts", 0.0)
            if "bio_health_pts" in comp:
                bio_health_pts = min(100.0, bio_health_pts + comp.get("bio_health_pts", 0.0))

            if comp.get("mitigation_tag"):
                active_mitigations.append(comp.get("mitigation_tag"))

        # Equation 2: Orbital Energy & Solar Flux
        # P_solar = (P_solar, 1AU / r^2)
        actual_solar_gen_w = solar_generation_1au_w / (sun_distance_au ** 2) if sun_distance_au > 0 else 0.0
        charge_efficiency = 0.85
        t_sun_hours = t_sun_min / 60.0
        t_eclipse_hours = t_eclipse_min / 60.0
        t_orbit_hours = t_orbit_min / 60.0

        # Daylight energy produced (Wh)
        energy_gen_daylight_wh = (actual_solar_gen_w * charge_efficiency * t_sun_hours) + (rtg_power_w * t_sun_hours)
        # Daylight energy consumed (Wh)
        energy_consumed_day_wh = power_draw_day_w * t_sun_hours
        # Net energy available for charging
        net_recharge_wh = max(0.0, energy_gen_daylight_wh - energy_consumed_day_wh)

        # Eclipse energy demand (Wh)
        # Net draw during eclipse accounting for RTG (if RTG present)
        net_eclipse_power_draw_w = max(0.0, power_draw_eclipse_w - rtg_power_w)
        energy_consumed_eclipse_wh = net_eclipse_power_draw_w * t_eclipse_hours

        # Battery Depth of Discharge during eclipse:
        # DoD = energy_consumed_eclipse / battery_capacity
        if battery_capacity_wh > 0:
            actual_dod = energy_consumed_eclipse_wh / battery_capacity_wh
        else:
            actual_dod = 1.0 if energy_consumed_eclipse_wh > 0 else 0.0

        battery_dod_percent = min(150.0, round(actual_dod * 100.0, 1))
        power_deficit = (energy_consumed_eclipse_wh > (battery_capacity_wh * battery_max_dod)) or (actual_solar_gen_w + rtg_power_w < power_draw_day_w)

        # Equation 3: Data Generation vs Downlink Bottleneck
        # Daily downlink capacity (Gigabytes) = Rate(Mbps) * Contact_Hours * 3600 / 8 / 1000
        daily_downlink_cap_gb = (downlink_rate_mbps * 1e6 * (t_contact_hours * 3600.0)) / (8.0 * 1e9)
        daily_downlink_cap_gb = round(daily_downlink_cap_gb, 2)
        data_overflow_gb = max(0.0, daily_data_gen_gb - daily_downlink_cap_gb)
        buffer_overflow_risk = data_overflow_gb > onboard_storage_gb

        # Check Critical Gates
        mass_pass = total_mass <= max_mass_kg
        budget_pass = total_cost_m <= budget_cap_m
        power_pass = not power_deficit and actual_dod <= battery_max_dod
        data_pass = not buffer_overflow_risk
        delta_v_pass = propellant_delta_v_m_s >= req_delta_v_m_s if req_delta_v_m_s > 0 else True

        # Thermal check (if mission requires cryogenic cooling e.g. Level 2 JWST L2 at 40K)
        target_temp_k = scenario_config.get("target_cryo_temp_k", None)
        thermal_pass = True
        if target_temp_k is not None:
            thermal_pass = cooling_capability_k <= target_temp_k

        # Overall engineering viability
        all_passed = mass_pass and budget_pass and power_pass and data_pass and delta_v_pass and thermal_pass

        # Diagnostic Bottleneck detection (for the 5-Hint diagnostic system)
        bottlenecks = []
        if not mass_pass:
            bottlenecks.append({
                "subsystem": "Mechanical / Structure",
                "issue": f"Mass exceeded: {round(total_mass, 2)} kg exceeds {max_mass_kg} kg limit by {round(total_mass - max_mass_kg, 2)} kg.",
                "remedy": "Swap to lightweight composite structures or optimize payload mass."
            })
        if not budget_pass:
            bottlenecks.append({
                "subsystem": "Mission & Budget Lead",
                "issue": f"Budget overrun: ${round(total_cost_m, 2)}M exceeds ${budget_cap_m}M cap.",
                "remedy": "Select cost-effective commercial off-the-shelf (COTS) components or rideshare options."
            })
        if not power_pass:
            bottlenecks.append({
                "subsystem": "Platform & Energy",
                "issue": f"Eclipse Battery DoD reached {battery_dod_percent}% (Limit: {int(battery_max_dod * 100)}%) or solar insufficient.",
                "remedy": "Increase battery capacity, deploy larger solar wings, or load-shed non-critical systems during eclipse."
            })
        if not data_pass:
            bottlenecks.append({
                "subsystem": "Flight & Comms",
                "issue": f"Data buffer overflow: generating {daily_data_gen_gb} GB/day but only downlinking {daily_downlink_cap_gb} GB.",
                "remedy": "Upgrade antenna from UHF to S-Band/Ka-Band/Laser DSOC or expand onboard solid-state storage."
            })
        if not thermal_pass:
            bottlenecks.append({
                "subsystem": "Thermal Control",
                "issue": f"Operating temperature {cooling_capability_k} K exceeds sensor requirement {target_temp_k} K.",
                "remedy": "Equip 5-layer sunshields and active Stirling cryocoolers."
            })
        if not delta_v_pass:
            bottlenecks.append({
                "subsystem": "Flight Dynamics / Propulsion",
                "issue": f"Delta-V deficit: {propellant_delta_v_m_s} m/s provided vs {req_delta_v_m_s} m/s required for orbital transfer.",
                "remedy": "Add high-Isp electric ion thruster or monopropellant hydrazine tanks."
            })

        # Calculate 6-Axis Radar Metrics (0 to 100 scale for visual radar chart)
        # 1. Mass Margin: 100 if mass is right at 80% of limit, decays if over or too heavy
        mass_score = max(0.0, min(100.0, 100.0 - ((total_mass / max_mass_kg - 0.75) * 120.0))) if max_mass_kg > 0 else 50.0
        if total_mass > max_mass_kg:
            mass_score = max(5.0, 50.0 - (total_mass - max_mass_kg) * 5.0)

        # 2. Power Margin
        power_margin_score = max(0.0, min(100.0, 100.0 - (actual_dod * 100.0)))

        # 3. Budget Efficiency
        budget_score = max(0.0, min(100.0, (1.0 - (total_cost_m / budget_cap_m)) * 100.0 + 30.0)) if budget_cap_m > 0 else 50.0
        if total_cost_m > budget_cap_m:
            budget_score = 10.0

        # 4. Data Link Reliability
        if daily_data_gen_gb > 0:
            link_ratio = daily_downlink_cap_gb / daily_data_gen_gb
            data_link_score = min(100.0, link_ratio * 75.0)
        else:
            data_link_score = 80.0

        # 5. Thermal & Structural Integrity
        thermal_score = 90.0 if thermal_pass else 25.0

        # 6. Crew Bio-Health / Mission Science Yield
        bio_yield_score = max(10.0, min(100.0, (science_yield_pts * 0.5) + (bio_health_pts * 0.5)))

        radar_metrics = {
            "mass_margin": round(mass_score, 1),
            "power_margin": round(power_margin_score, 1),
            "budget_efficiency": round(budget_score, 1),
            "data_link": round(data_link_score, 1),
            "thermal_integrity": round(thermal_score, 1),
            "bio_yield": round(bio_yield_score, 1),
        }

        # Base Engineering Score (0 - 1000 pts) matching Section 5.3:
        # Science/Resource Yield (30%), Crew Bio-Health & Safety Margin (30%),
        # Budget Efficiency (20%), and Power/Data Balance (20%)
        comp_science = min(300.0, science_yield_pts * 3.0)
        comp_bio = min(300.0, bio_health_pts * 3.0)
        comp_budget = min(200.0, budget_score * 2.0)
        comp_power_data = min(200.0, (power_margin_score * 0.5 + data_link_score * 0.5) * 2.0)
        base_engineering_score = round(comp_science + comp_bio + comp_budget + comp_power_data, 1)

        return {
            "total_mass_kg": round(total_mass, 2),
            "max_mass_kg": max_mass_kg,
            "mass_pass": mass_pass,
            "total_cost_m": round(total_cost_m, 2),
            "budget_cap_m": budget_cap_m,
            "budget_pass": budget_pass,
            "solar_gen_w": round(actual_solar_gen_w, 1),
            "rtg_power_w": round(rtg_power_w, 1),
            "power_draw_day_w": round(power_draw_day_w, 1),
            "power_draw_eclipse_w": round(power_draw_eclipse_w, 1),
            "battery_capacity_wh": round(battery_capacity_wh, 1),
            "battery_dod_percent": battery_dod_percent,
            "battery_max_dod_percent": int(battery_max_dod * 100),
            "power_pass": power_pass,
            "daily_data_gen_gb": round(daily_data_gen_gb, 2),
            "daily_downlink_cap_gb": round(daily_downlink_cap_gb, 2),
            "downlink_rate_mbps": round(downlink_rate_mbps, 2),
            "data_pass": data_pass,
            "propellant_delta_v_m_s": propellant_delta_v_m_s,
            "req_delta_v_m_s": req_delta_v_m_s,
            "delta_v_pass": delta_v_pass,
            "cooling_capability_k": cooling_capability_k,
            "thermal_pass": thermal_pass,
            "science_yield_pts": science_yield_pts,
            "bio_health_pts": bio_health_pts,
            "all_passed": all_passed,
            "bottlenecks": bottlenecks,
            "radar_metrics": radar_metrics,
            "base_engineering_score": base_engineering_score,
            "active_mitigations": active_mitigations,
        }
