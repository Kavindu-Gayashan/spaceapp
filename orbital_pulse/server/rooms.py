"""
Orbital Pulse - Multiplayer Room Manager & Real-Time Synchronization Engine
Supports 1-Player (Solo Commander), 2-Player (Dual Command), and 4-Player (Full Mission Squad).
Handles 4-digit room codes, station locks, shared pools, and live crisis votes.
Directly implements Section 3.1 and Section 9.
"""

import time
import random
import string
import asyncio
from typing import Dict, List, Any, Optional
from fastapi import WebSocket

from orbital_pulse.models.campaign import CAMPAIGN_LEVELS
from orbital_pulse.models.components import COMPONENTS_BY_STATION
from orbital_pulse.engine.systems import SystemsEngine
from orbital_pulse.engine.scoring import ScoringEngine, TARGET_CLOCKS
from orbital_pulse.engine.biomedicine import BiomedicineEngine
from orbital_pulse.models.characters import CHARACTERS, TRADE_STUDY_DIALOGUES


class GameRoom:
    """Represents a synchronized multiplayer or solo mission room."""

    def __init__(self, room_code: str, host_name: str, mode: str = "1P", level: int = 1):
        self.room_code = room_code.upper()
        self.host_name = host_name
        self.mode = mode.upper() # "1P", "2P", "4P"
        self.level = level
        self.created_at = time.time()
        self.connections: Dict[str, WebSocket] = {} # player_id -> WebSocket
        self.players: Dict[str, Dict[str, Any]] = {}     # player_id -> metadata

        # Station Ownership mapping
        # In 1P: player owns all 4 stations (station_1 .. station_4)
        # In 2P: Player 1 owns station_1 & station_2 (Platform & Flight), Player 2 owns station_3 & station_4
        # In 4P: 1 player per station
        self.station_owners: Dict[str, str] = {
            "station_1": None,
            "station_2": None,
            "station_3": None,
            "station_4": None
        }

        # Game State
        self.status = "lobby" # lobby, designing, simulating, debrief
        self.selected_components: Dict[str, Dict[str, Any]] = {
            "station_1": None,
            "station_2": None,
            "station_3": None,
            "station_4": None
        }

        # Timer & Clocks
        self.t_start: Optional[float] = None
        self.t_frozen_total: float = 0.0
        self.frozen_until: Optional[float] = None
        self.station_done_times: Dict[str, float] = {} # station -> seconds taken
        self.player_done_times: Dict[str, float] = {}  # player_id -> seconds taken

        # Hints & Puzzles
        self.unused_hints: int = 5
        self.solved_puzzles: int = 0
        self.mastery_xp: int = 0
        self.completed_tutorials: List[str] = []

        # Active Crisis & Voting
        self.active_crisis: Optional[Dict[str, Any]] = None
        self.crisis_votes: Dict[str, str] = {} # player_id -> option_id

        # Chat / Dialogue Log
        self.dialogue_log: List[Dict[str, Any]] = []

        # Vitals for Level 4 Crew Trauma Crisis
        self.vance_vitals = {
            "heart_rate_bpm": 125,
            "blood_pressure_sys": 85,
            "blood_pressure_dia": 55,
            "blood_loss_ml": 650,
            "oxygen_sat_percent": 91.0,
            "radiation_dose_msv": 12.0
        }

        # Simulation telemetry state
        self.simulation_step = 0
        self.sim_active = False
        self.last_systems_eval: Dict[str, Any] = {}

    def get_scenario(self) -> Dict[str, Any]:
        return CAMPAIGN_LEVELS.get(self.level, CAMPAIGN_LEVELS[1])

    def assign_stations_for_mode(self):
        """Assigns station ownership based on connected players and game mode."""
        player_ids = list(self.players.keys())
        if not player_ids:
            return

        if self.mode == "1P":
            solo_id = player_ids[0]
            for st in ["station_1", "station_2", "station_3", "station_4"]:
                self.station_owners[st] = solo_id
                self.players[solo_id]["stations"] = ["station_1", "station_2", "station_3", "station_4"]
                self.players[solo_id]["role"] = "Solo Commander (All Stations)"

        elif self.mode == "2P":
            p1 = player_ids[0]
            p2 = player_ids[1] if len(player_ids) > 1 else None
            self.station_owners["station_1"] = p1
            self.station_owners["station_2"] = p1
            self.players[p1]["stations"] = ["station_1", "station_2"]
            self.players[p1]["role"] = "Platform & Flight Director"

            if p2:
                self.station_owners["station_3"] = p2
                self.station_owners["station_4"] = p2
                self.players[p2]["stations"] = ["station_3", "station_4"]
                self.players[p2]["role"] = "Payload, Bio-Support & Comms Director"

        elif self.mode == "4P":
            roles = [
                ("station_1", "Station 1: Mission & Budget Lead"),
                ("station_2", "Station 2: Platform & Energy Lead"),
                ("station_3", "Station 3: Payload & Bio-Systems Lead"),
                ("station_4", "Station 4: Flight & Comms Lead")
            ]
            for idx, (st, rname) in enumerate(roles):
                pid = player_ids[idx] if idx < len(player_ids) else None
                self.station_owners[st] = pid
                if pid:
                    self.players[pid]["stations"] = [st]
                    self.players[pid]["role"] = rname

    def get_elapsed_seconds(self) -> float:
        """Returns elapsed active seconds excluding freeze time."""
        if not self.t_start:
            return 0.0
        now = time.time()
        elapsed = now - self.t_start - self.t_frozen_total
        # Check if currently frozen
        if self.frozen_until and now < self.frozen_until:
            freeze_left = self.frozen_until - now
            elapsed -= (45.0 - freeze_left)
        return max(0.0, elapsed)

    def freeze_timer_for_tutorial(self, seconds: float = 45.0):
        """Urspace Guide Safeguard: freezes the clock for up to 45s on first view."""
        now = time.time()
        self.frozen_until = now + seconds
        self.t_frozen_total += seconds

    def evaluate_systems(self) -> Dict[str, Any]:
        """Calculates current system metrics, mass/power/data balance, and radar."""
        scenario = self.get_scenario()
        res = SystemsEngine.evaluate_mission(scenario, self.selected_components)
        self.last_systems_eval = res
        return res

    def add_dialogue(self, speaker_id: str, message: str, is_shout: bool = False):
        """Adds a message to the conversation hub."""
        char = CHARACTERS.get(speaker_id, {
            "name": speaker_id.title(),
            "color": "#38bdf8",
            "avatar": "💬",
            "title": "Mission Specialist"
        })
        entry = {
            "id": f"msg_{len(self.dialogue_log)+1}",
            "speaker_id": speaker_id,
            "speaker_name": char["name"],
            "speaker_title": char["title"],
            "speaker_avatar": char["avatar"],
            "speaker_color": char["color"],
            "message": message,
            "is_shout": is_shout,
            "timestamp": round(self.get_elapsed_seconds(), 1)
        }
        self.dialogue_log.append(entry)
        if len(self.dialogue_log) > 60:
            self.dialogue_log.pop(0)
        return entry

    def serialize_state(self) -> Dict[str, Any]:
        """Serializes complete room state for WebSocket broadcast."""
        scenario = self.get_scenario()
        systems = self.evaluate_systems()
        elapsed = self.get_elapsed_seconds()
        target_t = ScoringEngine.get_target_time(self.level, self.mode)

        # Freeze state
        now = time.time()
        is_frozen = bool(self.frozen_until and now < self.frozen_until)
        freeze_remaining = max(0, int(self.frozen_until - now)) if is_frozen else 0

        return {
            "room_code": self.room_code,
            "host_name": self.host_name,
            "mode": self.mode,
            "level": self.level,
            "status": self.status,
            "scenario": scenario,
            "players": self.players,
            "station_owners": self.station_owners,
            "selected_components": self.selected_components,
            "available_components": COMPONENTS_BY_STATION,
            "systems": systems,
            "dialogue_log": self.dialogue_log[-20:],
            "elapsed_seconds": round(elapsed, 1),
            "target_seconds": target_t,
            "is_frozen": is_frozen,
            "freeze_remaining": freeze_remaining,
            "unused_hints": self.unused_hints,
            "solved_puzzles": self.solved_puzzles,
            "mastery_xp": self.mastery_xp,
            "active_crisis": self.active_crisis,
            "crisis_votes": self.crisis_votes,
            "vance_vitals": self.vance_vitals,
            "sim_active": self.sim_active,
            "simulation_step": self.simulation_step
        }


class RoomManager:
    """Singleton managing active game rooms."""

    def __init__(self):
        self.rooms: Dict[str, GameRoom] = {}

    def create_room(self, host_name: str, mode: str = "1P", level: int = 1, preferred_code: Optional[str] = None) -> GameRoom:
        """Creates a new game room with unique 4-digit code."""
        if preferred_code and preferred_code.upper() not in self.rooms:
            code = preferred_code.upper()
        else:
            # Generate random 4-character code
            chars = string.ascii_uppercase + "23456789"
            for _ in range(50):
                code = "".join(random.choices(chars, k=4))
                if code not in self.rooms:
                    break

        room = GameRoom(room_code=code, host_name=host_name, mode=mode, level=level)
        self.rooms[code] = room
        return room

    def get_room(self, code: str) -> Optional[GameRoom]:
        return self.rooms.get(code.upper())

    def remove_room(self, code: str):
        if code.upper() in self.rooms:
            del self.rooms[code.upper()]


# Global instance
room_manager = RoomManager()
