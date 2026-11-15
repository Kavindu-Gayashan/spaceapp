"""
Orbital Pulse - Spacecraft Components Catalog
Component definitions across all 4 Mission Control Stations and 5 CML Campaign Levels.
"""

from typing import Dict, List, Any

# Component database organized by Station
# Station 1: Mission & Launch / Budget
# Station 2: Platform & Energy (Power, Thermal, Chassis)
# Station 3: Payload & Bio-Systems (Instruments, Life Support, Drills)
# Station 4: Flight & Comms (Propulsion, Avionics, Downlink)

COMPONENTS_BY_STATION: Dict[str, List[Dict[str, Any]]] = {
    "station_1": [
        # Mission & Budget Lead
        {
            "id": "lv_falcon_rideshare",
            "name": "Commercial Rideshare Dispenser",
            "category": "Launch Vehicle",
            "levels": [1],
            "cost_m": 0.8,
            "mass_kg": 0.0,
            "max_payload_mass_kg": 14.0,
            "description": "Standard 6U CubeSat deployer slot on Falcon 9 SSO rideshare. Strict 12 kg limit.",
            "unlocked_by": None
        },
        {
            "id": "lv_electron_dedicated",
            "name": "Light Dedicated Booster (Curie)",
            "category": "Launch Vehicle",
            "levels": [1, 2],
            "cost_m": 2.2,
            "mass_kg": 0.0,
            "max_payload_mass_kg": 35.0,
            "description": "Dedicated orbital insertion allows flexible inclination and higher mass margin.",
            "unlocked_by": None
        },
        {
            "id": "lv_heavy_deepspace",
            "name": "Heavy Deep-Space Lifter (Vulcan/Centaur)",
            "category": "Launch Vehicle",
            "levels": [2, 3],
            "cost_m": 4.5,
            "mass_kg": 0.0,
            "max_payload_mass_kg": 650.0,
            "description": "High C3 injection energy capable of reaching Sun-Earth L2 and Trans-Lunar Injection (TLI).",
            "unlocked_by": None
        },
        {
            "id": "lv_sls_artemis",
            "name": "Super-Heavy Crew Transporter (SLS Block 1B)",
            "category": "Launch Vehicle",
            "levels": [4, 5],
            "cost_m": 12.0,
            "mass_kg": 0.0,
            "max_payload_mass_kg": 3500.0,
            "description": "Human-rated super-heavy lifter carrying Orion capsule & Deep Space logistics modules.",
            "unlocked_by": None
        },
        {
            "id": "mission_profile_extended",
            "name": "Extended Mission Assurance Tier",
            "category": "Mission Assurance",
            "levels": [1, 2, 3, 4, 5],
            "cost_m": 0.4,
            "mass_kg": 0.0,
            "science_pts": 25.0,
            "description": "Triple redundancy checks and NASA MDL certified safety envelopes.",
            "unlocked_by": None
        }
    ],
    "station_2": [
        # Platform & Energy Lead
        {
            "id": "pwr_body_panels",
            "name": "Body-Mounted GaAs Solar Cells",
            "category": "Power Generation",
            "type": "solar",
            "levels": [1],
            "cost_m": 0.2,
            "mass_kg": 0.8,
            "power_gen_w": 18.0,
            "description": "Fixed triple-junction cells on 6U chassis. Generates 18W in direct sun, zero during eclipse.",
            "unlocked_by": None
        },
        {
            "id": "pwr_deployable_wings",
            "name": "Deployable Articulated Solar Wings",
            "category": "Power Generation",
            "type": "solar",
            "levels": [1, 2],
            "cost_m": 0.5,
            "mass_kg": 2.2,
            "power_gen_w": 65.0,
            "description": "Spring-loaded unfolding solar arrays with single-axis sun tracking. Generates 65W.",
            "unlocked_by": None
        },
        {
            "id": "pwr_lunar_mmrtg",
            "name": "Next-Gen Plutonium MMRTG",
            "category": "Power Generation",
            "type": "rtg",
            "levels": [3, 4, 5],
            "cost_m": 3.2,
            "mass_kg": 38.0,
            "power_gen_w": 125.0,
            "description": "Multi-Mission Radioisotope Thermoelectric Generator. Continuous 125W day and night in shadow.",
            "unlocked_by": None
        },
        {
            "id": "pwr_fission_kilopower",
            "name": "Kilopower Stirling Fission Reactor (10 kWe)",
            "category": "Power Generation",
            "type": "rtg",
            "levels": [5],
            "cost_m": 8.0,
            "mass_kg": 180.0,
            "power_gen_w": 8500.0,
            "description": "Enriched uranium compact reactor powering electric ion thrusters at 2.2 AU deep space.",
            "unlocked_by": None
        },
        {
            "id": "bat_cubesat_liion",
            "name": "6U CubeSat Li-Ion Battery Pack (40 Wh)",
            "category": "Energy Storage",
            "type": "battery",
            "levels": [1],
            "cost_m": 0.15,
            "mass_kg": 1.1,
            "battery_capacity_wh": 40.0,
            "max_dod": 0.70,
            "description": "Compact cells providing 40 Wh. Sufficient for basic avionics; tight for active thermal loads.",
            "unlocked_by": None
        },
        {
            "id": "bat_highcap_liion",
            "name": "Deep-Cycle Space Battery Bank (180 Wh)",
            "category": "Energy Storage",
            "type": "battery",
            "levels": [1, 2, 3],
            "cost_m": 0.45,
            "mass_kg": 3.2,
            "battery_capacity_wh": 180.0,
            "max_dod": 0.75,
            "description": "Deep-cycle automotive-grade space-rated lithium battery pack to survive 35m shadow.",
            "unlocked_by": None
        },
        {
            "id": "bat_crew_ups",
            "name": "High-Capacity Lunar Habitat Bus Battery (2.5 kWh)",
            "category": "Energy Storage",
            "type": "battery",
            "levels": [4, 5],
            "cost_m": 1.5,
            "mass_kg": 45.0,
            "battery_capacity_wh": 2500.0,
            "max_dod": 0.85,
            "description": "Critical power reserve powering medical bay, airlock repressurization and life support.",
            "unlocked_by": None
        },
        {
            "id": "therm_cryocooler_5layer",
            "name": "5-Layer Kapton Sunshield + Pulse Tube Cryocooler",
            "category": "Thermal Systems",
            "levels": [2],
            "cost_m": 2.1,
            "mass_kg": 42.0,
            "power_draw_w": 55.0,
            "min_temp_k": 38.0,
            "mitigation_tag": "cryo_cooled",
            "description": "Shields IR sensor from Sun/Earth heat and cools detector to 38 K (-235°C). JWST-grade.",
            "unlocked_by": None
        },
        {
            "id": "therm_loop_heatpipes",
            "name": "Loop Heat Pipes + Electrostatic Dust Shields",
            "category": "Thermal & Dust",
            "levels": [3],
            "cost_m": 0.9,
            "mass_kg": 8.5,
            "power_draw_w": 12.0,
            "mitigation_tag": "lunar_dust_sealed",
            "description": "Routes MMRTG waste heat to warm drill motors; electrostatic curtain repels abrasive lunar dust.",
            "unlocked_by": None
        },
        {
            "id": "mech_centrifuge_waterwall",
            "name": "Artificial Gravity Centrifuge & Water-Wall Radiation Shield",
            "category": "Chassis & Habitat",
            "levels": [5],
            "cost_m": 5.5,
            "mass_kg": 320.0,
            "power_draw_w": 120.0,
            "mitigation_tag": "artificial_gravity",
            "bio_health_pts": 35.0,
            "description": "0.4G rotating module prevents crew bone demineralization and 10cm water jacket blocks GCR cosmic rays.",
            "unlocked_by": None
        }
    ],
    "station_3": [
        # Payload & Bio-Systems Lead
        {
            "id": "pay_swir_camera",
            "name": "Short-Wave Infrared (SWIR) Mineral & Moisture Imager",
            "category": "Scientific Remote Sensing",
            "levels": [1],
            "cost_m": 0.55,
            "mass_kg": 2.1,
            "power_draw_day_w": 14.0,
            "power_draw_eclipse_w": 0.0,
            "data_gen_gb_per_day": 3.2,
            "science_pts": 45.0,
            "description": "Hyperspectral SWIR sensor tuned to 1.4-2.5 µm to detect clay soil water saturation & landslide hazard.",
            "unlocked_by": None
        },
        {
            "id": "pay_bio_incubator",
            "name": "Pressurized 37°C Micro-Bio Stem-Cell Incubator",
            "category": "Space Biomedicine",
            "levels": [1],
            "cost_m": 0.85,
            "mass_kg": 3.4,
            "power_draw_day_w": 16.0,
            "power_draw_eclipse_w": 22.0, # Must heat during freezing eclipse!
            "data_gen_gb_per_day": 1.5,
            "science_pts": 50.0,
            "bio_health_pts": 30.0,
            "mitigation_tag": "cell_viability_preserved",
            "description": "Microfluidic bio-cartridge culturing human stem cells with automated fluorescent microscopy. NASA BioSentinel heritage.",
            "unlocked_by": None
        },
        {
            "id": "pay_mid_ir_spectrometer",
            "name": "Mid-Infrared Grating Spectrometer & Beryllium Primary Mirror",
            "category": "Optical Astronomy",
            "levels": [2],
            "cost_m": 3.8,
            "mass_kg": 75.0,
            "power_draw_day_w": 40.0,
            "power_draw_eclipse_w": 40.0,
            "data_gen_gb_per_day": 12.0,
            "science_pts": 85.0,
            "requires_tag": "cryo_cooled",
            "description": "Exoplanet biosignature scanner (detects O3, CH4, H2O, CO2). Blinded by thermal noise unless cooled below 40K.",
            "unlocked_by": None
        },
        {
            "id": "pay_lunar_drill_isru",
            "name": "1.5m Rotary-Percussive Core Drill & Thermal Volatile Reactor (ISRU)",
            "category": "Subsurface Extraction",
            "levels": [3],
            "cost_m": 3.4,
            "mass_kg": 58.0,
            "power_draw_day_w": 95.0,
            "power_draw_eclipse_w": 95.0,
            "data_gen_gb_per_day": 4.0,
            "science_pts": 90.0,
            "mitigation_tag": "isru_active",
            "description": "NASA PRIME-1 / VIPER drill hammering into cryogenic permafrost to vaporize and capture 0.15 kg O2/hr.",
            "unlocked_by": None
        },
        {
            "id": "bio_trauma_pod_eclss",
            "name": "Pressurized Trauma Stabilization Pod + Robotic IV Clotting Injector",
            "category": "Emergency Biomedicine",
            "levels": [4],
            "cost_m": 2.8,
            "mass_kg": 85.0,
            "power_draw_day_w": 900.0,
            "power_draw_eclipse_w": 900.0,
            "data_gen_gb_per_day": 8.0,
            "mitigation_tag": "trauma_pod",
            "bio_health_pts": 50.0,
            "description": "Emergency microgravity intensive care capsule with ultrasound diagnostics and automated synthetic platelet infusion.",
            "unlocked_by": None
        },
        {
            "id": "bio_anti_g_suit",
            "name": "Active Pneumatic Anti-G Countermeasure Flight Suit",
            "category": "Emergency Biomedicine",
            "levels": [4],
            "cost_m": 0.4,
            "mass_kg": 6.5,
            "power_draw_day_w": 15.0,
            "power_draw_eclipse_w": 15.0,
            "mitigation_tag": "anti_g_countermeasure",
            "bio_health_pts": 25.0,
            "description": "Dynamic compression cuffs preventing vascular collapse and blood pooling during high-G (5.5G) Earth re-entry.",
            "unlocked_by": None
        },
        {
            "id": "pay_asteroid_harpoon_libs",
            "name": "Pyrotechnic Microgravity Anchoring Harpoon + LIBS Laser Core Rig",
            "category": "Asteroid Prospecting",
            "levels": [5],
            "cost_m": 4.1,
            "mass_kg": 64.0,
            "power_draw_day_w": 110.0,
            "power_draw_eclipse_w": 110.0,
            "data_gen_gb_per_day": 15.0,
            "science_pts": 95.0,
            "mitigation_tag": "asteroid_anchored",
            "description": "Fires explosive titanium flukes to tether spacecraft to metallic asteroid in micro-G while laser extracts volatiles.",
            "unlocked_by": None
        }
    ],
    "station_4": [
        # Flight & Comms Lead
        {
            "id": "comms_uhf_dipole",
            "name": "Omnidirectional UHF Dipole Antenna",
            "category": "Communications",
            "levels": [1],
            "cost_m": 0.08,
            "mass_kg": 0.35,
            "downlink_rate_mbps": 0.064, # 64 kbps
            "power_draw_w": 2.0,
            "description": "Basic beacon transmitter. Low data throughput; easily bottlenecks hyperspectral imagery.",
            "unlocked_by": None
        },
        {
            "id": "comms_sband_patch",
            "name": "Direct-to-Earth S-Band Patch Antenna Array",
            "category": "Communications",
            "levels": [1, 2],
            "cost_m": 0.25,
            "mass_kg": 1.2,
            "downlink_rate_mbps": 2.5,
            "power_draw_w": 8.0,
            "description": "2.5 Mbps downlink. Ample bandwidth for SWIR terrain maps and high-res bio-microscopy.",
            "unlocked_by": None
        },
        {
            "id": "comms_kaband_deepspace",
            "name": "High-Gain Ka-Band Deep Space Parabolic Reflector (1.2m)",
            "category": "Communications",
            "levels": [2, 3, 4],
            "cost_m": 1.4,
            "mass_kg": 18.0,
            "downlink_rate_mbps": 25.0,
            "power_draw_w": 45.0,
            "description": "Essential for 1.5M km JWST data streaming, lunar crater relays, and live 3D telemedicine ultrasound.",
            "unlocked_by": None
        },
        {
            "id": "comms_laser_dsoc",
            "name": "Deep Space Optical Laser Comms (DSOC) Terminal",
            "category": "Communications",
            "levels": [4, 5],
            "cost_m": 3.6,
            "mass_kg": 28.0,
            "downlink_rate_mbps": 150.0,
            "power_draw_w": 65.0,
            "mitigation_tag": "laser_telemed_active",
            "description": "NASA DSOC flight demo heritage. Ultra-high rate optical beam transmitting HD ultrasound & 4K asteroid maps.",
            "unlocked_by": None
        },
        {
            "id": "comms_lunar_relay_cubesat",
            "name": "Deployable Lunar Halo Relay CubeSat",
            "category": "Orbital Relay",
            "levels": [3],
            "cost_m": 0.95,
            "mass_kg": 11.5,
            "downlink_rate_mbps": 15.0,
            "power_draw_w": 18.0,
            "mitigation_tag": "crater_relay_linked",
            "description": "Orbits above Shackleton Crater rim, relaying drill telemetry to Earth DSN ground stations.",
            "unlocked_by": None
        },
        {
            "id": "prop_cold_gas_rcs",
            "name": "Cold-Gas Reaction Control Thrusters (3U Module)",
            "category": "Propulsion",
            "levels": [1],
            "cost_m": 0.25,
            "mass_kg": 1.8,
            "delta_v_m_s": 35.0,
            "power_draw_w": 1.5,
            "description": "Provides precise attitude detumbling and 35 m/s delta-V for CubeSat orbit raising.",
            "unlocked_by": None
        },
        {
            "id": "prop_hydrazine_biprop",
            "name": "High-Thrust Monopropellant Hydrazine Stage",
            "category": "Propulsion",
            "levels": [3, 4],
            "cost_m": 1.8,
            "mass_kg": 65.0,
            "delta_v_m_s": 1200.0,
            "power_draw_w": 10.0,
            "mitigation_tag": "abort_burn_capable",
            "description": "Delivers the critical 1,150 m/s delta-V needed for a 72-hour emergency fast-return from lunar NRHO to Earth.",
            "unlocked_by": None
        },
        {
            "id": "prop_next_ion_electric",
            "name": "NEXT-C Dual Ion Thruster (Xenon Hall Effect)",
            "category": "Propulsion",
            "levels": [5],
            "cost_m": 4.2,
            "mass_kg": 72.0,
            "delta_v_m_s": 4500.0,
            "power_draw_w": 2500.0,
            "description": "Ultra-high specific impulse (4,200s Isp) engine capable of reaching 2.2 AU asteroid and returning samples.",
            "unlocked_by": None
        },
        {
            "id": "avionics_ai_autonomous",
            "name": "Radiation-Hardened Autonomous Flight Computer & AI Copilot",
            "category": "Avionics & AI",
            "levels": [2, 3, 4, 5],
            "cost_m": 1.6,
            "mass_kg": 6.2,
            "power_draw_w": 28.0,
            "mitigation_tag": "onboard_ai_assist",
            "description": "Executes local navigation, fault containment, and emergency medical diagnostic triage during radio blackouts.",
            "unlocked_by": None
        }
    ]
}
