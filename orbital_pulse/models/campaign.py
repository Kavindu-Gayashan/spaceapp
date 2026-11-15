"""
Orbital Pulse - 5-Level Progressive Campaign Scenarios (CML 1 to CML 5)
Directly implements Section 4 and Section 7 of the Master Project Proposal.
"""

from typing import Dict, Any, List

CAMPAIGN_LEVELS: Dict[int, Dict[str, Any]] = {
    1: {
        "level": 1,
        "name": "Operation Terra-Pulse",
        "tier": "Easy",
        "cml": "CML 1 – Cadet",
        "target_orbit": "Low Earth Orbit / Sun-Synchronous Orbit (550 km)",
        "objective": "6U CubeSat for Landslide Mineral & Moisture Mapping & Stem-Cell Bio-Testing",
        "story": (
            "Severe monsoon rains threaten mountain valleys with catastrophic mudslides, while an international "
            "biomedical consortium needs to evaluate microgravity cellular repair mechanisms on human stem cells. "
            "Operating on a strict $2.5M rideshare allocation, your team must engineer a 6U CubeSat that balances "
            "a power-hungry 37°C incubator heater against a 35-minute orbital night without blowing the 12 kg dispenser limit."
        ),
        "trade_offs_summary": "CubeSat mass limits (12 kg), 35m eclipse battery drain, SWIR camera vs 37°C incubator, UHF vs S-Band data rate.",
        "max_mass_kg": 12.0,
        "budget_cap_m": 2.5,
        "sun_distance_au": 1.0,
        "t_orbit_min": 95.0,
        "t_eclipse_min": 35.0,
        "t_contact_hours_per_day": 2.5,
        "base_bus_mass_kg": 2.2,
        "base_bus_cost_m": 0.2,
        "base_idle_power_w": 3.0,
        "target_cryo_temp_k": None,
        "req_delta_v_m_s": 0.0,
        "nasa_mission_match": {
            "missions": ["NASA EMIT (Earth Surface Mineral Dust Source Investigation)", "NASA BioSentinel CubeSat"],
            "heritage_url": "https://www.nasa.gov/mission/emit/",
            "real_world_context": (
                "Like your Terra-Pulse spacecraft, NASA EMIT uses advanced imaging spectroscopy from orbit to study "
                "surface mineralogy and natural hazards, while NASA BioSentinel launched a 6U CubeSat beyond LEO with "
                "an autonomous microfluidic card and 37°C bio-incubator to assess living biological response to deep space."
            )
        },
        "urspace_tutorials": ["tut_cubesat_sso", "tut_cell_life_space"],
        "crisis_event": {
            "title": "Orbital Eclipse Thermal Emergency",
            "trigger_step": "simulation_orbit_2",
            "narrative": "Spacecraft has entered Earth's shadow! Ambient chassis temp plunging to -65°C. Cell incubator heater drawing 22W. Battery discharging rapidly!",
            "options": [
                {
                    "id": "opt_shed_avionics",
                    "label": "Load-Shed Non-Critical Avionics & Keep Cells at 37°C",
                    "effect": {"power_saved_w": 8.0, "science_mod": 1.0, "bio_mod": 1.0, "success": True},
                    "explanation": "Shedding auxiliary sensors protects battery reserve while keeping stem cells fully viable."
                },
                {
                    "id": "opt_hibernate_heater",
                    "label": "Reduce Bio-Incubator Heater to 22°C (Conserve Power)",
                    "effect": {"power_saved_w": 14.0, "science_mod": 0.7, "bio_mod": 0.3, "success": False},
                    "explanation": "Cells undergo thermal shock and metabolic arrest. Bio-science yield permanently degraded!"
                }
            ]
        }
    },
    2: {
        "level": 2,
        "name": "Operation Exo-Beacon",
        "tier": "Easy-Medium",
        "cml": "CML 2 – Specialist",
        "target_orbit": "Sun-Earth Lagrange Point 2 (L2, 1.5M km)",
        "objective": "Cryogenic Space Telescope for Exoplanet Biosignatures & Asteroid Mineralogy",
        "story": (
            "Promoted to deep-space astrophysics, your team is tasked with designing an observatory stationed at Sun-Earth L2. "
            "To detect methane, oxygen, and water vapor in exoplanet atmospheres, the mid-infrared detector must be shielded from "
            "solar and Earth heat and actively cooled to -230°C (40 K). Any thermal leakage blinds the telescope."
        ),
        "trade_offs_summary": "Cryocooling (-230°C / 40 K), 5-layer Kapton sunshield mass, high-precision reaction wheel pointing, and Ka-Band deep space dish.",
        "max_mass_kg": 180.0,
        "budget_cap_m": 7.5,
        "sun_distance_au": 1.01,
        "t_orbit_min": 1440.0, # Halo orbit around L2
        "t_eclipse_min": 0.0,    # Halo orbit avoids Earth shadow
        "t_contact_hours_per_day": 8.0,
        "base_bus_mass_kg": 25.0,
        "base_bus_cost_m": 1.0,
        "base_idle_power_w": 25.0,
        "target_cryo_temp_k": 40.0, # Requires cryocooler
        "req_delta_v_m_s": 0.0,
        "nasa_mission_match": {
            "missions": ["James Webb Space Telescope (JWST)", "Near-Earth Object (NEO) Surveyor"],
            "heritage_url": "https://webb.nasa.gov/",
            "real_world_context": (
                "Operating at Sun-Earth L2, NASA's JWST uses a tennis-court-sized 5-layer Kapton sunshield to cool its "
                "infrared instruments down to 40 K and an active pulse-tube cryocooler for MIRI at 7 K, while Ka-band downlinks "
                "gigabytes of spectral biosignature data daily."
            )
        },
        "urspace_tutorials": ["tut_lagrange_l2", "tut_cryo_thermal"],
        "crisis_event": {
            "title": "Sunshield Micro-Tear & Thermal Bleed",
            "trigger_step": "simulation_orbit_2",
            "narrative": "Thermal sensors detect infrared detector warming to 58 K due to a pinhole solar shield puncture! Background noise saturating exoplanet spectrometers!",
            "options": [
                {
                    "id": "opt_boost_cryo",
                    "label": "Overclock Pulse-Tube Cryocooler (+30W Draw) & Reorient Solar Attitude",
                    "effect": {"temp_drop_k": 20.0, "power_draw_increase_w": 30.0, "success": True},
                    "explanation": "Active cryocooler compensation restores detector to 38 K and saves optical observation run."
                },
                {
                    "id": "opt_ignore_thermal",
                    "label": "Continue Imaging Without Attitude Correction",
                    "effect": {"temp_drop_k": 0.0, "science_mod": 0.15, "success": False},
                    "explanation": "Thermal photon noise overwhelms exoplanet spectral lines. Biosignature survey ruined."
                }
            ]
        }
    },
    3: {
        "level": 3,
        "name": "Operation Lunar-Vein",
        "tier": "Medium",
        "cml": "CML 3 – Lead",
        "target_orbit": "Lunar South Pole (Shackleton Crater Floor, -200°C)",
        "objective": "Crater Water-Ice Rotary Core Drilling & In-Situ Oxygen Production Lander (ISRU)",
        "story": (
            "Sunlight never touches the floor of Shackleton Crater. Temperatures hover near -200°C, and abrasive electrostatically "
            "charged lunar dust destroys unprotected actuators. Solar panels are completely useless on the crater floor. Your "
            "robotic prospecting lander must rely on nuclear power (MMRTG), route waste heat to prevent frozen drill bits, and "
            "communicate over the 4 km crater rim via a halo relay satellite."
        ),
        "trade_offs_summary": "Permanent shadow nuclear power (MMRTG), loop heat pipe thermal routing, percussive core drill, electrostatic dust seals, relay CubeSat.",
        "max_mass_kg": 350.0,
        "budget_cap_m": 12.0,
        "sun_distance_au": 1.0,
        "t_orbit_min": 708.0, # Lunar day/night cycle
        "t_eclipse_min": 708.0, # Permanent shadow inside crater!
        "t_contact_hours_per_day": 6.0,
        "base_bus_mass_kg": 65.0,
        "base_bus_cost_m": 2.0,
        "base_idle_power_w": 35.0,
        "target_cryo_temp_k": None,
        "req_delta_v_m_s": 0.0,
        "nasa_mission_match": {
            "missions": ["NASA VIPER (Volatiles Investigating Polar Exploration Rover)", "PRIME-1 Lunar Drill (TRIDENT)"],
            "heritage_url": "https://www.nasa.gov/mission/viper/",
            "real_world_context": (
                "NASA's VIPER rover and PRIME-1 lander were engineered specifically to drill 1 meter into lunar cryogenic permafrost "
                "at the South Pole to map water-ice deposits and demonstrate thermal volatile extraction for future Artemis base life-support."
            )
        },
        "urspace_tutorials": ["tut_isru_drilling", "tut_relay_orbits"],
        "crisis_event": {
            "title": "Abrasive Regolith Gearbox Binding",
            "trigger_step": "simulation_orbit_2",
            "narrative": "Drill depth reached 0.8 meters, but sharp volcanic glass dust has penetrated secondary drive seals! Motor torque spiking by 300%!",
            "options": [
                {
                    "id": "opt_pulse_electrostatic",
                    "label": "Fire High-Voltage Electrostatic Dust Repulsion & Reverse Percussive Pulse",
                    "effect": {"drill_cleared": True, "power_draw_w": 25.0, "success": True},
                    "explanation": "Electrostatic charge differential lifts jagged regolith particles clear of mechanical teeth."
                },
                {
                    "id": "opt_force_torque",
                    "label": "Max Out Motor Current to Force Rotation",
                    "effect": {"drill_cleared": False, "motor_burnt": True, "success": False},
                    "explanation": "Drive shaft shears under extreme friction load. Core drill permanently immobilized."
                }
            ]
        }
    },
    4: {
        "level": 4,
        "name": "Operation Lifeline (The Crew Injury Crisis)",
        "tier": "Medium-Hard",
        "cml": "CML 4 – Commander",
        "target_orbit": "Lunar Near-Rectilinear Halo Orbit (NRHO, Crewed Outpost)",
        "objective": "Mid-Mission Crisis: Lunar Spacewalk Crew Trauma & Solar Radiation Storm Survival",
        "story": (
            "Disaster strikes the Lunar Gateway outpost in NRHO orbit! During a spacewalk to inspect sample collection hardware, "
            "a hypervelocity micrometeoroid shower strikes Specialist Alex Vance. His suit cuff is depressurized, fracturing "
            "his forearm and causing acute internal abdominal hemorrhage. Concurrently, NOAA Deep Space monitors detect an "
            "X-class Solar Proton Event (SPE) arriving in 45 minutes! Your Mission Control squad must coordinate emergency "
            "trauma stabilization, prioritize +900W power during lunar shadow, transmit live ultrasound telemedicine over Ka-Band, "
            "and decide whether to execute a 5.5G high-speed Earth return or stabilize in zero-G."
        ),
        "trade_offs_summary": "Zero-G fracture/bleed stabilization, +900W medical pod power drain during lunar shadow, ultrasound telemetry bandwidth, abort delta-V vs 5.5G re-entry trauma.",
        "max_mass_kg": 1500.0,
        "budget_cap_m": 22.0,
        "sun_distance_au": 1.0,
        "t_orbit_min": 10080.0, # 7-day NRHO orbital period
        "t_eclipse_min": 90.0,   # Lunar shadow passage
        "t_contact_hours_per_day": 12.0,
        "base_bus_mass_kg": 400.0,
        "base_bus_cost_m": 5.0,
        "base_idle_power_w": 220.0,
        "target_cryo_temp_k": None,
        "req_delta_v_m_s": 1150.0, # Required delta-V for fast Earth return
        "nasa_mission_match": {
            "missions": ["NASA Artemis Lunar Gateway", "Orion Crew Survival Systems & Exploration Medical Capability (ExMC)"],
            "heritage_url": "https://www.nasa.gov/gateway",
            "real_world_context": (
                "NASA's Exploration Medical Capability (ExMC) team and Artemis Gateway design life support and autonomous "
                "medical decision systems to manage severe trauma, internal bleeding, and radiation storms when 400,000 km "
                "from Earth hospitals with multi-second communication lags."
            )
        },
        "urspace_tutorials": ["tut_microg_trauma", "tut_eclss_loops", "tut_fast_return_gload"],
        "crisis_event": {
            "title": "CRITICAL TRAUMA VOTE: Emergency Burn vs Zero-G Hemostasis",
            "trigger_step": "simulation_crisis_decision",
            "narrative": (
                "Specialist Vance is hypotensive (BP 75/45) and tachycardic (HR 135 bpm). Dr. Rostova reports: "
                "'Trauma Pod draws +900W. Entering lunar eclipse in 10 minutes. If Flight fires the main engine for a "
                "72-hour fast-return, the 5.5G re-entry deceleration will cause fatal arterial blow-out unless he is "
                "fully stabilized with robotic coagulants and an active anti-G pressure suit!'"
            ),
            "options": [
                {
                    "id": "opt_stabilize_then_abort",
                    "label": "Stabilize Hemorrhage First (Shed Ovens, Route 100% Battery to Medical Bay & Lock Ka-Band)",
                    "effect": {"stabilization": True, "safe_return": True, "vance_survives": True, "success": True},
                    "explanation": "Masterful trade-off management! Power shedding kept the trauma pod running, coagulants halted internal bleeding, and Vance survived re-entry."
                },
                {
                    "id": "opt_instant_burn_no_power_cut",
                    "label": "Immediate 72-Hour Earth Burn Without Power Load-Shedding",
                    "effect": {"stabilization": False, "safe_return": False, "vance_survives": False, "success": False},
                    "explanation": "Batteries died 30 minutes into eclipse! The medical bay failed, and 5.5G re-entry caused catastrophic cardiovascular collapse."
                }
            ]
        }
    },
    5: {
        "level": 5,
        "name": "Operation Star-Forge",
        "tier": "Hard / Boss Level",
        "cml": "CML 5 – Architect",
        "target_orbit": "Deep-Space Metallic Asteroid Psyche Encounter (2.2 AU)",
        "objective": "Crewed & Robotic Asteroid Anchoring, Volatile Prospecting & Earth Re-entry Sample Return",
        "story": (
            "The crowning test of systems engineering: a 14-month deep-space expedition to a M-type metallic asteroid at 2.2 AU. "
            "At this distance, the Inverse-Square Law reduces solar power by over 75% ((1/2.2)^2 ≈ 0.206). Microgravity is so weak "
            "that core drills push the spacecraft backwards into space without anchoring harpoons. Long-duration cosmic rays and "
            "zero-G muscle atrophy threaten the crew, while a 36-minute round-trip light delay prevents real-time Earth intervention. "
            "Players must synchronize a nuclear fission reactor, ion propulsion, artificial gravity centrifuge, and autonomous AI."
        ),
        "trade_offs_summary": "14-month crew health, micro-G anchoring harpoons, 1/r^2 solar drop (75% loss), Kilopower fission reactor, ion thruster delta-V, 36m light delay.",
        "max_mass_kg": 3200.0,
        "budget_cap_m": 45.0,
        "sun_distance_au": 2.2,
        "t_orbit_min": 20160.0, # Deep space interplanetary transit
        "t_eclipse_min": 0.0,
        "t_contact_hours_per_day": 4.0,
        "base_bus_mass_kg": 950.0,
        "base_bus_cost_m": 12.0,
        "base_idle_power_w": 500.0,
        "target_cryo_temp_k": None,
        "req_delta_v_m_s": 4200.0,
        "nasa_mission_match": {
            "missions": ["NASA Psyche Mission", "OSIRIS-REx Asteroid Sample Return", "Deep Space Transport Concepts"],
            "heritage_url": "https://www.jpl.nasa.gov/missions/psyche",
            "real_world_context": (
                "NASA's Psyche mission uses high-efficiency Hall-effect solar electric propulsion to travel 2.2 AU to explore "
                "a metal-rich world, testing Deep Space Optical Communications (DSOC) laser tech, while OSIRIS-REx perfected "
                "touch-and-go sampling in microgravity and survived 12 km/s Earth atmospheric re-entry."
            )
        },
        "urspace_tutorials": ["tut_inverse_square_solar", "tut_microg_anchoring", "tut_light_time_autonomy"],
        "crisis_event": {
            "title": "Anchoring Recoil in Zero-G & 36-Minute Comms Blackout",
            "trigger_step": "simulation_orbit_2",
            "narrative": (
                "During asteroid touchdown, contact sensors detect the spacecraft rebounding off the nickel-iron crust at 0.12 m/s. "
                "Earth is 18 light-minutes away; commands cannot arrive in time! Autonomous Flight Computer triggers emergency subroutine."
            ),
            "options": [
                {
                    "id": "opt_fire_harpoons_rcs",
                    "label": "Autonomous Pyrotechnic Anchoring Harpoon Deployment & Downward RCS Pulse",
                    "effect": {"firmly_anchored": True, "drilling_authorized": True, "success": True},
                    "explanation": "Titanium barbed harpoons penetrate regolith fissures while cold-gas RCS counter-thrusts, securing a solid mechanical anchor."
                },
                {
                    "id": "opt_wait_earth_command",
                    "label": "Delay Maneuver and Await Telemetry Confirmation from Earth",
                    "effect": {"firmly_anchored": False, "drilling_authorized": False, "success": False},
                    "explanation": "The 36-minute round-trip delay is too slow! The lander bounces into an uncontrolled tumble away from the asteroid."
                }
            ]
        }
    }
}
