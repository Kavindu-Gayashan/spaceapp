"""
Orbital Pulse - Mission Control Characters & Dialogue Engine
Provides AI specialist dialogue bubbles, trade-off warnings, and crisis debates.
Directly implements Section 3.1, 3.2, and Section 4 sample transcripts.
"""

from typing import Dict, List, Any

CHARACTERS: Dict[str, Dict[str, Any]] = {
    "sterling": {
        "id": "sterling",
        "name": "Dir. Sarah Sterling",
        "station": "station_1",
        "title": "Mission & Budget Director (NASA MDL)",
        "color": "#e0a82e", # Gold
        "avatar": "🛰️",
        "quote": "Every gram of launch mass has a dollar tag. Let's make every single watt count."
    },
    "chen": {
        "id": "chen",
        "name": "Chief Eng. Marcus Chen",
        "station": "station_2",
        "title": "Platform & Energy Lead",
        "color": "#00f0ff", # Cyan
        "avatar": "⚡",
        "quote": "If your battery hits 100% depth of discharge during eclipse, your science is dead in the dark."
    },
    "rostova": {
        "id": "rostova",
        "name": "Dr. Elena Rostova",
        "station": "station_3",
        "title": "Payload & Bio-Systems Lead",
        "color": "#10b981", # Emerald
        "avatar": "🔬",
        "quote": "The data from these stem cells and drill samples will rewrite planetary geology. Guard them!"
    },
    "vance": {
        "id": "vance",
        "name": "Cmdr. Alex Vance",
        "station": "station_4",
        "title": "Flight & Comms Director",
        "color": "#f43f5e", # Rose
        "avatar": "🚀",
        "quote": "Orbital mechanics doesn't negotiate. Check your delta-V and keep that ground downlink locked."
    }
}

# Dynamic conversational responses triggered by component selection
TRADE_STUDY_DIALOGUES = {
    "pwr_deployable_wings": {
        "speaker": "chen",
        "message": "Excellent choice deploying solar wings! We jump from 18W to 65W, giving us enough margin to recharge the batteries before the next orbital night."
    },
    "pwr_body_panels": {
        "speaker": "chen",
        "message": "Careful! Body panels only generate 18W in direct sun. If the bio-incubator or radar turns on during eclipse, our batteries will be drained to 0%!"
    },
    "pay_bio_incubator": {
        "speaker": "rostova",
        "message": "The stem-cell microfluidic cartridge is active! Remember, these cells die if temperature drops below 32°C. We must keep the 22W heater running through eclipse."
    },
    "pay_swir_camera": {
        "speaker": "rostova",
        "message": "Short-wave infrared sensor calibrated. We'll map landslide moisture saturation with 30m resolution, but we need at least an S-band downlink to transmit the cubes."
    },
    "pay_mid_ir_spectrometer": {
        "speaker": "rostova",
        "message": "The mid-infrared spectrometer is online to search for ozone and methane biosignatures! But if detector temperature rises above 40K, thermal noise will wash out the signal!"
    },
    "therm_cryocooler_5layer": {
        "speaker": "chen",
        "message": "5-layer Kapton sunshield deployed and active Stirling cryocooler running! Detector temperature is dropping smoothly toward 38 Kelvin. Cold and silent."
    },
    "pay_lunar_drill_isru": {
        "speaker": "rostova",
        "message": "Rotary-percussive drill armed! We're targeting 1.5 meters into Shackleton crater's permafrost. Expect 0.15 kg of pure oxygen per hour once the sublimation oven hits 120°C."
    },
    "pwr_lunar_mmrtg": {
        "speaker": "chen",
        "message": "MMRTG nuclear generator initialized. 125 Watts of steady thermal and electric power, completely unaffected by the 350-hour lunar night. This is how we survive the dark."
    },
    "comms_uhf_dipole": {
        "speaker": "vance",
        "message": "UHF dipole deployed. We only have 64 kbps throughput. It will take 14 hours to downlink a single high-resolution image cube. I strongly recommend upgrading to S-Band."
    },
    "comms_sband_patch": {
        "speaker": "vance",
        "message": "S-Band patch array locked on ground stations! 2.5 Mbps pipe active. We can dump science data within our daily 2.5-hour contact window."
    },
    "comms_kaband_deepspace": {
        "speaker": "vance",
        "message": "Ka-Band deep space dish tracking Earth! 25 Mbps link established across 1.5 million kilometers. Ready to stream spectral data and high-res telemedicine video."
    },
    "comms_laser_dsoc": {
        "speaker": "vance",
        "message": "Deep Space Optical Laser locked onto Palomar Observatory! 150 Mbps downlink throughput achieved. Ground surgeons have crystal-clear 4K feed."
    },
    "prop_hydrazine_biprop": {
        "speaker": "vance",
        "message": "Hydrazine bipropellant tanks pressurized. 1,200 m/s delta-V in the tank—enough for emergency abort maneuvers or trans-Earth injection burns."
    },
    "avionics_ai_autonomous": {
        "speaker": "vance",
        "message": "Autonomous AI flight copilot online! When we face the 36-minute deep space comms blackout, the local neural core will handle station-keeping and emergency fault triage."
    },
    "lv_falcon_rideshare": {
        "speaker": "sterling",
        "message": "Falcon rideshare slot confirmed under $1M! Economical, but strict on mass—every gram over 12 kg means automatic launch dispenser rejection."
    },
    "lv_electron_dedicated": {
        "speaker": "sterling",
        "message": "Dedicated light booster gives us custom orbit injection parameters and up to 35 kg payload margin. Worth the modest cost increase."
    }
}
