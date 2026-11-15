"""
Orbital Pulse - Urspace Guide: Interactive On-Demand Micro-Tutorial System
Directly implements Section 3.4 of the Master Project Proposal.
"""

from typing import Dict, List, Any

URSPACE_TUTORIALS: Dict[str, Dict[str, Any]] = {
    "tut_cubesat_sso": {
        "id": "tut_cubesat_sso",
        "title": "CubeSat Form Factors (1U–12U) & Sun-Synchronous Orbits",
        "subtitle": "How standardized nanospacecraft deliver high science on low rideshare budgets",
        "read_time": "25 seconds",
        "mastery_xp": 100,
        "content_markdown": (
            "### 1. The CubeSat Standard (1U = 10×10×10 cm, ~1.33 kg)\n"
            "CubeSats are built from modular units. A **6U CubeSat** (like NASA BioSentinel and EMIT) provides "
            "~12 kg payload capacity. Body panels only offer ~0.06 m² of solar exposure (generating ~15–20W), which is "
            "insufficient if running continuous 37°C thermal heaters during the 35-minute orbital shadow.\n\n"
            "### 2. Sun-Synchronous Orbit (SSO)\n"
            "An SSO orbit has an inclination of ~97.5°, where Earth's oblateness (J2 perturbation) causes the orbital plane "
            "to precess at exactly 360° per year—matching Earth's revolution around the Sun. This provides consistent lighting "
            "angles for multispectral imaging."
        ),
        "slider_interactive": {
            "label": "Form Factor Size (U)",
            "min": 1,
            "max": 12,
            "default": 6,
            "step": 1,
            "unit": "U",
            "calculation_js": "return { mass_kg: (val * 1.8).toFixed(1), solar_area_cm2: (val * 100), max_power_w: (val * 8.5).toFixed(0) };",
            "display_template": "Mass: {mass_kg} kg | Solar Area: {solar_area_cm2} cm² | Peak Power: {max_power_w} W"
        },
        "key_takeaway": "Always deploy solar wings and calculate shadow battery drain when operating biological incubators!"
    },
    "tut_cell_life_space": {
        "id": "tut_cell_life_space",
        "title": "Keeping Cells Alive in Microgravity & Cold Space",
        "subtitle": "Microfluidics, temperature regulation, and cosmic radiation counters",
        "read_time": "20 seconds",
        "mastery_xp": 100,
        "content_markdown": (
            "### 1. Thermal Homeostasis at 37°C\n"
            "Human stem cells undergo rapid apoptosis (programmed cell death) if temperature drops below 32°C or spikes above 40°C. "
            "In deep space, radiation cooling drops spacecraft temperatures to -65°C during eclipse. Electric heaters must maintain "
            "closed-loop PID control powered by deep-cycle batteries.\n\n"
            "### 2. Fluid Dynamics Without Gravity\n"
            "In zero-G, capillary action replaces buoyancy and hydrostatic pressure. Automated microfluidic cassettes use positive-displacement "
            "piezo pumps to supply glucose reagents and buffer solutions without creating destructive air bubbles."
        ),
        "slider_interactive": {
            "label": "Heater Power in Eclipse (Watts)",
            "min": 0,
            "max": 30,
            "default": 18,
            "step": 1,
            "unit": "W",
            "calculation_js": "return { temp_c: (15 + (val * 1.2)).toFixed(1), cell_health: Math.min(100, Math.max(0, 100 - Math.abs(37 - (15 + (val * 1.2))) * 7)).toFixed(0) };",
            "display_template": "Incubator Temp: {temp_c} °C | Cell Viability: {cell_health} %"
        },
        "key_takeaway": "Never shed power from the bio-incubator during orbital eclipse!"
    },
    "tut_lagrange_l2": {
        "id": "tut_lagrange_l2",
        "title": "Lagrange Points (L1/L2) & Infrared Cryogenics",
        "subtitle": "Station-keeping in deep space and cooling down to 40 Kelvin (-233°C)",
        "read_time": "30 seconds",
        "mastery_xp": 125,
        "content_markdown": (
            "### 1. Why Sun-Earth L2?\n"
            "Located 1.5 million kilometers behind Earth along the Sun-Earth line, L2 allows a spacecraft to stay aligned "
            "such that the Sun, Earth, and Moon are always in the same direction. A single multi-layer sunshield can block all three.\n\n"
            "### 2. Thermal Cryogenics & Mid-IR Biosignatures\n"
            "Infrared light detects thermal emissions of molecules like water, methane, and ozone. However, any warm component "
            "on the telescope emits infrared light that blinds the camera. JWST requires passive Kapton sunshields to reach 40 K, "
            "and active helium pulse-tube cryocoolers to reach 7 Kelvin."
        ),
        "slider_interactive": {
            "label": "Sunshield Kapton Layers",
            "min": 1,
            "max": 5,
            "default": 5,
            "step": 1,
            "unit": "layers",
            "calculation_js": "var temps = [240, 180, 110, 65, 38]; return { cold_temp_k: temps[val-1], snr_db: ((6-val)*-6 + 32).toFixed(1) };",
            "display_template": "Detector Cold-Side: {cold_temp_k} K | Infrared Signal-to-Noise: +{snr_db} dB"
        },
        "key_takeaway": "Equip 5-layer sunshields and active cryocoolers to detect exoplanet atmospheric biosignatures."
    },
    "tut_cryo_thermal": {
        "id": "tut_cryo_thermal",
        "title": "Cryogenic Cooling Loops & Heat Pipe Rejection",
        "subtitle": "Moving heat away from sensors without mechanical vibrations",
        "read_time": "20 seconds",
        "mastery_xp": 100,
        "content_markdown": (
            "Pulse-tube cryocoolers compress and expand helium gas without moving pistons in the cold head, eliminating mechanical "
            "jitter that would blur sub-arcsecond telescope pointing. Heat rejected from the compressor must be carried to exterior "
            "radiators facing deep space via ammonia or ethane loop heat pipes."
        ),
        "slider_interactive": {
            "label": "Cryocooler Electrical Power (W)",
            "min": 10,
            "max": 100,
            "default": 55,
            "step": 5,
            "unit": "W",
            "calculation_js": "return { detector_k: Math.max(6, 120 - val * 1.5).toFixed(1), radiator_heat_w: (val * 1.3).toFixed(1) };",
            "display_template": "Detector Temp: {detector_k} K | Radiator Heat Load: {radiator_heat_w} W"
        },
        "key_takeaway": "Cryocoolers require dedicated radiator mass to shed rejected heat!"
    },
    "tut_isru_drilling": {
        "id": "tut_isru_drilling",
        "title": "In-Situ Resource Utilization (ISRU) & Rotary Drilling",
        "subtitle": "Harvesting water and oxygen from cryogenic lunar permafrost",
        "read_time": "25 seconds",
        "mastery_xp": 125,
        "content_markdown": (
            "### 1. Water Ice in Permanent Shadow Regions (PSRs)\n"
            "Deep craters at the Lunar South Pole like Shackleton are shielded from sunlight and have remained below 100 K (-173°C) "
            "for billions of years. Water ice mixed with regolith is as hard as granite.\n\n"
            "### 2. Rotary-Percussive Drilling & Sublimation Ovens\n"
            "A standard rotary drill bit will bind or shatter. Rotary-percussive hammers deliver 1,000 impacts/minute to fracture the icy soil. "
            "Once regolith cuttings enter the sealed ISRU oven, waste heat warms the chamber to +150°C, causing ice to sublimate into water vapor, "
            "which is condensed and electrolyzed into liquid oxygen (O₂) and hydrogen (H₂) fuel."
        ),
        "slider_interactive": {
            "label": "ISRU Oven Chamber Temperature (°C)",
            "min": -50,
            "max": 250,
            "default": 120,
            "step": 10,
            "unit": "°C",
            "calculation_js": "var rate = val <= 0 ? 0 : Math.min(0.25, (val / 100) * 0.12); return { o2_rate_kg_hr: rate.toFixed(2), power_draw_w: (val > 0 ? 50 + val * 0.4 : 10).toFixed(0) };",
            "display_template": "Oxygen Extraction Rate: {o2_rate_kg_hr} kg/hr | Heater Power: {power_draw_w} W"
        },
        "key_takeaway": "Subsurface drills require nuclear isotope (MMRTG) power and waste heat routing in dark craters."
    },
    "tut_relay_orbits": {
        "id": "tut_relay_orbits",
        "title": "Lunar Halo Orbits & Over-the-Rim Relay Communications",
        "subtitle": "Overcoming terrain line-of-sight blockage in 4-km deep craters",
        "read_time": "20 seconds",
        "mastery_xp": 100,
        "content_markdown": (
            "Direct-to-Earth radio communication fails inside deep polar craters because the tall crater rims block line-of-sight to Earth. "
            "A small relay satellite placed in an Earth-Moon L2 southern halo orbit maintains permanent direct view of both the crater floor "
            "and Earth ground antennas."
        ),
        "slider_interactive": {
            "label": "Relay Satellite Elevation Angle (°)",
            "min": 0,
            "max": 90,
            "default": 45,
            "step": 5,
            "unit": "deg",
            "calculation_js": "var los = val >= 15; return { line_of_sight: los ? 'LOCKED' : 'BLOCKED BY CRATER RIM', downlink_mbps: los ? 25 : 0 };",
            "display_template": "Optical/RF Link: {line_of_sight} | Downlink Speed: {downlink_mbps} Mbps"
        },
        "key_takeaway": "Always deploy an orbital relay when prospecting permanently shadowed craters!"
    },
    "tut_microg_trauma": {
        "id": "tut_microg_trauma",
        "title": "Zero-Gravity Trauma Physiology & Microvascular Bleeding",
        "subtitle": "Managing traumatic compound fractures and hemorrhage in weightlessness",
        "read_time": "30 seconds",
        "mastery_xp": 150,
        "content_markdown": (
            "### 1. Hemodynamic Shift in Microgravity\n"
            "Without gravity pulling blood toward the feet, 1.5 to 2 liters of fluid shifts cephalad (toward the head and torso). "
            "Central venous pressure increases, and standard gravity-fed IV bags and blood drainage lines cannot function—they require "
            "active mechanical infusion.\n\n"
            "### 2. Internal Bleeding Danger\n"
            "In zero-G, blood does not pool in dependent cavities; instead, it disperses along fascial planes. Internal hemorrhaging "
            "leads to rapid hemodynamic instability. Synthetic prothrombin/clotting agents and pressurized trauma garments are required "
            "immediately to induce hemostasis before any acceleration forces are applied."
        ),
        "slider_interactive": {
            "label": "Synthetic Clotting Infusion Rate (mL/min)",
            "min": 0,
            "max": 10,
            "default": 4,
            "step": 1,
            "unit": "mL/min",
            "calculation_js": "return { bleed_rate_ml_min: Math.max(1, 20 - val * 4.5).toFixed(1), thrombus_time_min: Math.max(2, 25 - val * 4).toFixed(0) };",
            "display_template": "Bleed Rate: {bleed_rate_ml_min} mL/min | Time to Hemostasis: {thrombus_time_min} mins"
        },
        "key_takeaway": "Stabilize blood loss and pressure in zero-G prior to firing high-thrust engines!"
    },
    "tut_eclss_loops": {
        "id": "tut_eclss_loops",
        "title": "ECLSS Life Support Loops: Oxygen & CO2 Scrubbing",
        "subtitle": "Sustaining crew metabolism during orbital trauma and high metabolic stress",
        "read_time": "20 seconds",
        "mastery_xp": 100,
        "content_markdown": (
            "An injured astronaut breathing rapidly under trauma consumes up to 1.2 kg of oxygen per day and generates excess CO₂. "
            "ECLSS uses amine beds or CDRA (Carbon Dioxide Removal Assembly) along with Sabatier reactors and oxygen generation assemblies (OGA). "
            "Medical bay activation requires dedicated oxygen flow and scrubbers."
        ),
        "slider_interactive": {
            "label": "ECLSS O₂ Partial Pressure (kPa)",
            "min": 10,
            "max": 35,
            "default": 21,
            "step": 1,
            "unit": "kPa",
            "calculation_js": "var norm = Math.abs(val - 21.3); return { o2_sat_pct: Math.min(100, 99 - norm * 2.5).toFixed(1), hypoxia_risk: val < 16 ? 'HIGH HYPOXIA' : (val > 28 ? 'HYPEROXIA RISK' : 'NOMINAL') };",
            "display_template": "Blood O₂ Saturation: {o2_sat_pct} % | Physiological Status: {hypoxia_risk}"
        },
        "key_takeaway": "Maintain 21 kPa partial pressure O₂ to support injured crew respiration."
    },
    "tut_fast_return_gload": {
        "id": "tut_fast_return_gload",
        "title": "Fast-Return Δv vs. Atmospheric Re-entry G-Forces",
        "subtitle": "The life-or-death trade-off between transit speed and human tolerance",
        "read_time": "25 seconds",
        "mastery_xp": 150,
        "content_markdown": (
            "### 1. The Fast-Return Trajectory\n"
            "A standard lunar return takes 5–7 days with low delta-V. To return in 72 hours requires burning an extra ~1,150 m/s Δv. "
            "However, arriving at Earth at steep hyperbolic velocity (>11.2 km/s) requires a steep atmospheric entry corridor.\n\n"
            "### 2. The 5.5G Re-entry Deceleration Spike\n"
            "Decelerating from 11 km/s induces up to 5.5 Gs of deceleration (+Gx chest-to-back or +Gz head-to-toe). In a patient with "
            "internal bleeding, 5.5 Gs creates hydrostatic pressures that rupture newly formed blood clots and causes fatal cardiovascular collapse "
            "unless an active anti-G countermeasure suit is pressurized and the hemorrhage is stabilized."
        ),
        "slider_interactive": {
            "label": "Return Duration (Hours)",
            "min": 48,
            "max": 144,
            "default": 72,
            "step": 6,
            "unit": "hrs",
            "calculation_js": "var g = Math.max(1.2, (180 / val) * 2.2).toFixed(1); var dv = Math.round(180000 / val); return { peak_g: g, req_dv_m_s: dv };",
            "display_template": "Peak Re-entry Deceleration: {peak_g} G | Required Return Δv: {req_dv_m_s} m/s"
        },
        "key_takeaway": "Equip anti-G countermeasure suits before executing high-thrust fast-return burns!"
    },
    "tut_inverse_square_solar": {
        "id": "tut_inverse_square_solar",
        "title": "The Inverse-Square Law & Deep Space Fission Power",
        "subtitle": "Why solar arrays wither at 2.2 AU and compact nuclear reactors take over",
        "read_time": "25 seconds",
        "mastery_xp": 125,
        "content_markdown": (
            "Solar radiation spreads spherically as it travels away from the Sun. Light intensity drops with the square of the distance: "
            "**I(r) = I₀ / r²**.\n\n"
            "At 1 AU (Earth), solar flux is 1,361 W/m².\n"
            "At 2.2 AU (Metallic Asteroid Belt), flux drops to: 1,361 / (2.2)² = 281 W/m² (a **79% reduction!**).\n\n"
            "To produce 10 kW for electric ion thrusters would require over 180 m² of fragile solar panels. Therefore, deep space missions "
            "rely on compact Stirling fission reactors (such as NASA's Kilopower) providing continuous megawatts regardless of distance."
        ),
        "slider_interactive": {
            "label": "Distance from Sun (AU)",
            "min": 0.5,
            "max": 5.0,
            "default": 2.2,
            "step": 0.1,
            "unit": "AU",
            "calculation_js": "var flux = (1361 / (val * val)).toFixed(0); var pct = ((flux / 1361) * 100).toFixed(1); return { solar_flux_w_m2: flux, solar_output_pct: pct };",
            "display_template": "Solar Flux: {solar_flux_w_m2} W/m² | Solar Array Output: {solar_output_pct} % of Earth"
        },
        "key_takeaway": "Switch from solar to compact nuclear fission when designing missions beyond 2.0 AU."
    },
    "tut_microg_anchoring": {
        "id": "tut_microg_anchoring",
        "title": "Microgravity Asteroid Anchoring & Recoil Dynamics",
        "subtitle": "Newton's Third Law when drilling into bodies with almost zero gravity",
        "read_time": "25 seconds",
        "mastery_xp": 125,
        "content_markdown": (
            "Small asteroids (like 16 Psyche or Bennu) have surface gravity less than 0.0001 m/s² (10,000 times weaker than Earth). "
            "By Newton's Third Law, if a core drill exerts 50 Newtons of downward drilling force, the spacecraft will immediately push "
            "itself up and off the surface into deep space! Spacecraft must fire pyrotechnic anchoring harpoons into the metal-silicate crust "
            "to tension cables and clamp the drill down."
        ),
        "slider_interactive": {
            "label": "Drilling Thrust Force (N)",
            "min": 10,
            "max": 100,
            "default": 50,
            "step": 5,
            "unit": "N",
            "calculation_js": "return { tension_required_n: (val * 1.4).toFixed(0), lift_off_risk: val > 20 ? 'RECOIL EJECTION WITHOUT HARPOONS' : 'VERY SLOW PENETRATION' };",
            "display_template": "Cable Tension Required: {tension_required_n} N | Recoil State: {lift_off_risk}"
        },
        "key_takeaway": "Always deploy anchoring harpoons before initiating robotic or crewed surface sampling."
    },
    "tut_light_time_autonomy": {
        "id": "tut_light_time_autonomy",
        "title": "Autonomous Operations Under Light-Time Delay",
        "subtitle": "Why 36-minute radio lags require onboard AI decision making",
        "read_time": "20 seconds",
        "mastery_xp": 125,
        "content_markdown": (
            "At 2.2 AU, radio signals traveling at the speed of light take 18.3 minutes to reach Earth, and another 18.3 minutes "
            "for a command to return (a **36.6-minute round trip**). If a thruster fails or an anchoring cable snaps, the spacecraft cannot "
            "wait for human joystick control. Radiation-hardened onboard AI must detect anomalies, run closed-loop triage, and fire RCS countermeasures "
            "in milliseconds."
        ),
        "slider_interactive": {
            "label": "Distance to Earth (AU)",
            "min": 0.1,
            "max": 3.0,
            "default": 2.2,
            "step": 0.1,
            "unit": "AU",
            "calculation_js": "var one_way_m = (val * 8.317).toFixed(1); var rt_m = (val * 16.634).toFixed(1); return { one_way_min: one_way_m, round_trip_min: rt_m };",
            "display_template": "One-Way Delay: {one_way_min} mins | Round-Trip Delay: {round_trip_min} mins"
        },
        "key_takeaway": "Equip radiation-hardened autonomous flight computers for all deep-space targets."
    }
}
