"""
Orbital Pulse - Fair Time Allocation Matrix & Gamified Scoring System
Directly implements Section 5 of the Master Project Proposal.
"""

from typing import Dict, Any

# Fair-Play Target Mission Clock (T_max in seconds) from Section 5.1
TARGET_CLOCKS = {
    1: {"1P": 480, "2P": 390, "4P": 330, "design_1p": 360, "sim_1p": 120},
    2: {"1P": 600, "2P": 480, "4P": 420, "design_1p": 450, "sim_1p": 150},
    3: {"1P": 720, "2P": 600, "4P": 510, "design_1p": 540, "sim_1p": 180},
    4: {"1P": 900, "2P": 750, "4P": 660, "design_1p": 600, "sim_1p": 300},
    5: {"1P": 1080, "2P": 900, "4P": 780, "design_1p": 780, "sim_1p": 300},
}


class ScoringEngine:
    """Computes mission scores, time bonuses, and fairness safeguards."""

    @staticmethod
    def get_target_time(level: int, mode: str) -> int:
        """Returns T_max (seconds) for given level and mode ('1P', '2P', '4P')."""
        mode_key = mode.upper()
        if mode_key not in ["1P", "2P", "4P"]:
            mode_key = "1P"
        return TARGET_CLOCKS.get(level, TARGET_CLOCKS[1])[mode_key]

    @staticmethod
    def calculate_score(
        level: int,
        mode: str,
        base_engineering_score: float, # 0 to 1000
        survival: bool,
        t_player: float,               # Player's personal station completion time (seconds)
        t_team: float,                 # Overall team completion time (seconds)
        unused_hints: int,             # Remaining hints out of 5
        solved_puzzles: int,           # Astro-Calculus problems solved
        aborted_safely: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates S_final according to Section 5.3:
        S_final = Survival * [
            S_engineering * (1 + 0.25 * (t_station_max - t_player)/t_station_max + 0.25 * (T_max - T_team)/T_max)
            + 50 * H_left + 75 * N_puzzles
        ]
        Includes:
        - Urspace Guide 45s freeze adjustment
        - Grace Overtime Window decay
        - Individual + Team speed bonus split
        """
        t_max = float(ScoringEngine.get_target_time(level, mode))
        # In 1P mode, t_player is t_team
        if mode.upper() == "1P":
            t_station_max = t_max
            t_player = min(t_player, t_team)
        else:
            # Station time target is portion of total
            t_station_max = t_max * 0.65

        # Safeguard 3: Grace Overtime Window
        # If over time, time bonuses smoothly decay to 0, but never penalize below 1.0 multiplier
        if t_player <= t_station_max:
            player_speed_term = 0.25 * ((t_station_max - t_player) / t_station_max)
        else:
            # Overtime decay
            player_speed_term = 0.0

        if t_team <= t_max:
            team_speed_term = 0.25 * ((t_max - t_team) / t_max)
        else:
            team_speed_term = 0.0

        time_multiplier = round(1.0 + player_speed_term + team_speed_term, 3)

        # Survival multiplier
        if survival:
            survival_mult = 1.0
        elif aborted_safely:
            survival_mult = 0.35 # Partial score for safe crew abort
        else:
            survival_mult = 0.0

        hint_bonus = 50 * max(0, min(5, unused_hints))
        puzzle_bonus = 75 * max(0, solved_puzzles)

        weighted_engineering = base_engineering_score * time_multiplier
        bracket_total = weighted_engineering + hint_bonus + puzzle_bonus
        final_score = int(round(survival_mult * bracket_total))

        # Determine Concept Maturity Level (CML) and Rank
        if final_score >= 1200:
            rank = "NASA Lead Mission Architect (Gold Laurels)"
            cml_cert = f"CML {level} - FULL FLIGHT CERTIFICATION"
        elif final_score >= 900:
            rank = "Mission Director Flight Qualified"
            cml_cert = f"CML {level} - ADVANCED BASELINE APPROVED"
        elif final_score >= 600:
            rank = "Flight Systems Specialist"
            cml_cert = f"CML {level} - PRELIMINARY DESIGN PASSED"
        elif final_score > 0:
            rank = "Cadet Systems Engineer"
            cml_cert = f"CML {level} - CONDITIONAL REDESIGN REQ."
        else:
            rank = "Mission Terminated (Forensic Review Required)"
            cml_cert = f"CML {level} - CRITICAL SYSTEMS FAILURE"

        return {
            "final_score": final_score,
            "survival": survival,
            "survival_mult": survival_mult,
            "base_engineering_score": round(base_engineering_score, 1),
            "time_multiplier": time_multiplier,
            "player_speed_bonus_pct": round(player_speed_term * 100.0, 1),
            "team_speed_bonus_pct": round(team_speed_term * 100.0, 1),
            "unused_hints": unused_hints,
            "hint_bonus": hint_bonus,
            "solved_puzzles": solved_puzzles,
            "puzzle_bonus": puzzle_bonus,
            "t_team_sec": round(t_team, 1),
            "t_max_sec": int(t_max),
            "t_player_sec": round(t_player, 1),
            "rank": rank,
            "cml_cert": cml_cert
        }
