# ORBITAL PULSE
### A Story-Driven, Multidisciplinary Space Mission Design & Crisis Simulation Game
**NASA Space Apps Challenge 2026 — Space Mission Design Game**

---

## 🚀 Overview

**ORBITAL PULSE** transforms complex aerospace systems engineering into a visually captivating, conversation-driven interactive simulation game modeled directly after **NASA's Mission Design Lab (MDL)** and **JPL's Concept Maturity Levels (CML 1–5)**.

Supporting **1-Player (Solo Commander)**, **2-Player (Dual Command)**, and **4-Player (Full Mission Squad)** modes connected over real-time WebSockets, players step into the shoes of mission controllers balancing competing trade-offs across mass, power grids, thermal stability, orbital mechanics, communications bandwidth, and crew biomedicine.

---

## 🌟 Key Features

1. **Adaptive 1-Player, 2-Player, and 4-Player Modes**:
   - **1-Player Mode (Solo Commander)**: 1 Human Player + 3 AI Mission Specialists engaging in interactive branching dialogues, trade-off warnings, and proposed solutions.
   - **2-Player Mode (Dual Command)**:
     - *Player 1 (Platform & Flight Director)*: Chassis structure, thermal loops, power grids, orbit, and launch vehicle.
     - *Player 2 (Payload, Bio-Support & Comms Director)*: Science instruments, life support, avionics, and ground links.
   - **4-Player Mode (Full Mission Squad)**: Live 4-digit room code (`NASA`, `LUNA`, `7429`) syncing Station 1 (Budget), Station 2 (Platform & Energy), Station 3 (Payload & Bio), and Station 4 (Flight & Comms).

2. **5-Level Progressive Campaign (CML 1 to CML 5)**:
   - **Level 1 (Easy – CML 1: Cadet)**: *Operation Terra-Pulse* — 6U CubeSat in Low Earth Orbit (SSO 550 km) balancing a SWIR landslide imager and a 37°C stem-cell micro-bio incubator during a 35-minute orbital shadow.
   - **Level 2 (Easy-Med – CML 2: Specialist)**: *Operation Exo-Beacon* — Deep-space cryogenic observatory at Sun-Earth L2 (1.5M km) requiring 5-layer Kapton sunshields and active cryocoolers (-230°C / 40 K) to detect exoplanet biosignatures.
   - **Level 3 (Medium – CML 3: Lead)**: *Operation Lunar-Vein* — Robotic landing rig inside Shackleton Crater (-200°C permanent shadow) utilizing a nuclear MMRTG battery, loop heat pipes, and a rotary-percussive drill for ISRU oxygen/water extraction.
   - **Level 4 (Med-Hard – CML 4: Commander)**: *Operation Lifeline (The Crew Injury Crisis)* — Stationed at the Lunar Gateway in NRHO orbit, an EVA micrometeoroid strike punctures Astronaut Vance's cuff, causing forearm fracture and internal bleeding. Squad coordinates a +900W medical pod power surge during lunar eclipse, live ultrasound telemedicine, and trade-off between zero-G stabilization vs 5.5G emergency Earth re-entry!
   - **Level 5 (Hard/Boss – CML 5: Architect)**: *Operation Star-Forge* — 14-month deep-space expedition to a metallic asteroid at 2.2 AU overcoming 75% solar flux drop with Kilopower fission, ion thrusters, microgravity anchoring harpoons, and 36-minute light delay.

3. **"Urspace Guide" — On-Demand Interactive Micro-Tutorials**:
   - Glowing badge opens 20-second bite-sized tutorials with **interactive mathematical sliders** (CubeSat form factors, Lagrange points, ISRU ovens, microgravity hemodynamics, inverse-square solar flux).
   - Unlocking modules awards **Mastery XP**.
   - **Fairness Safeguard**: Opening any guide automatically freezes the mission clock for up to 45 seconds on first viewing!

4. **5-Hint Diagnostic System & "Astro-Calculus" Refill Terminal**:
   - Players start with 5 Diagnostic Hints to highlight subsystem bottlenecks.
   - Refill terminal pauses the main mission clock for a 90-second calculus challenge. Solving real-world math problems grants **+1 Hint Refill** and **+75 Bonus Points**!
     1. *Calculus Derivative*: Instantaneous power drain $|dE/dt|$ of quadratic eclipse battery curve.
     2. *Calculus Maxima*: Apogee optimization $dh/dt = 0$ for a sounding probe.
     3. *Calculus Integral*: Definite integral $\int r(t)dt$ of ion thruster xenon consumption.
     4. *Deep-Space Solar Flux*: Inverse-Square Law scaling $P \propto 1/r^2$.
     5. *Biomedical Life Support*: ECLSS oxygen mass balance integration.

5. **Glassmorphic Mission Control Deck UI**:
   - **Center Stage**: Interactive **3D Spacecraft Builder & Orbital Globe** using Three.js WebGL (solar wings deploy, drills mount, transitioning into interactive orbital globe with day/night terminator).
   - **Right Sidebar**: Live **6-Axis Trade-Off Radar** (Mass Margin, Power Balance, Budget Efficiency, Data Downlink, Thermal/Cryo, Bio/Science) and neon vital gauges.
   - **Bottom Dock**: Animated character conversation hub (Dr. Elena Rostova, Cmdr. Alex Vance, Chief Eng. Marcus Chen, Dir. Sarah Sterling) with audio telemetry cues via Web Audio API.
   - **Post-Mission Forensic Debrief**: Root-cause post-mortem analysis, CML certificate rating, score equation breakdown, and **Real NASA Mission Match** cards.

6. **Fair-Play Time-Weighted Scoring Formula**:
   $$S_{\text{final}} = \text{Survival} \times \left[ S_{\text{engineering}} \times \left( 1 + 0.25 \times \frac{t_{\text{station, max}} - t_{\text{player}}}{t_{\text{station, max}}} + 0.25 \times \frac{T_{\max} - T_{\text{team}}}{T_{\max}} \right) + 50 \times H_{\text{left}} + 75 \times N_{\text{puzzles}} \right]$$
   - 50/50 individual vs team speed split.
   - Grace overtime window (multiplier smoothly decays to 1.0x instead of abrupt mission failure).

---

## 🛠️ Technology Stack

- **Backend Engine**: Python 3.10+ / Python 3.14
- **Web & Multiplayer**: FastAPI, Uvicorn, WebSockets (real-time state broadcast & crisis voting)
- **Physics & Math Engine**: NumPy, SciPy (Keplerian orbits, FSPL link budgets, Stefan-Boltzmann thermal equilibrium, inverse-square irradiance)
- **Frontend & Visualizations**:
  - Dark-mode glassmorphic CSS3 with blur backdrops and neon telemetry gauges
  - Three.js WebGL for real-time 3D modular spacecraft assembly and rotating orbital globes
  - SVG dynamic polygon rendering for the 6-Axis Trade-Off Radar chart
  - Web Audio API for procedural sound synthesis (beeps, alarms, thrusters, telemetry chimes)

---

## 📦 Installation & Quick Start

### 1. Clone & Enter Directory
```bash
cd /home/kavindu/Documents/nasa
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Orbital Pulse
```bash
python3 main.py --port 8080
```
Then open your browser at **`http://localhost:8080`**.

### 4. Run Unit Tests
```bash
PYTHONPATH=. pytest -v tests/
```

---

## 🛰️ Alignment with Official NASA Challenge Resources

- **NASA Mission Design Lab (MDL) & Concept Maturity Levels (CML 1–5)**: Powers the 5 campaign tiers and trade-off negotiations.
- **NASA EMIT & BioSentinel**: Direct heritage for Level 1 SWIR imaging and 37°C stem-cell microgravity incubators.
- **James Webb Space Telescope (JWST) & NEO Surveyor**: Direct heritage for Level 2 L2 halo orbit and 40 K cryogenic cooling.
- **NASA VIPER & PRIME-1 (TRIDENT Drill)**: Direct heritage for Level 3 rotary-percussive drilling and volatile sublimation ISRU in lunar South Pole craters.
- **Artemis Lunar Gateway, Orion & ExMC**: Direct heritage for Level 4 microgravity trauma management, ECLSS life-support loops, and atmospheric re-entry G-limits.
- **NASA Psyche & OSIRIS-REx**: Direct heritage for Level 5 asteroid prospecting, microgravity anchoring harpoons, and Deep Space Optical Communications (DSOC).
