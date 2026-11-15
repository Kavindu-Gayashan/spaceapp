"""
Unit tests for Fair-Play Scoring System & Safeguards
"""

import pytest
from orbital_pulse.engine.scoring import ScoringEngine


def test_target_clocks():
    assert ScoringEngine.get_target_time(1, "1P") == 480
    assert ScoringEngine.get_target_time(1, "2P") == 390
    assert ScoringEngine.get_target_time(1, "4P") == 330
    assert ScoringEngine.get_target_time(4, "1P") == 900
    assert ScoringEngine.get_target_time(5, "1P") == 1080


def test_score_calculation_nominal():
    # Successful mission completed on time
    res = ScoringEngine.calculate_score(
        level=1,
        mode="1P",
        base_engineering_score=800.0,
        survival=True,
        t_player=300.0,
        t_team=300.0,
        unused_hints=4,
        solved_puzzles=1
    )

    assert res["survival"] is True
    assert res["time_multiplier"] > 1.0
    assert res["hint_bonus"] == 200 # 4 * 50
    assert res["puzzle_bonus"] == 75  # 1 * 75
    assert res["final_score"] > 800
    assert "CML 1" in res["cml_cert"]


def test_score_catastrophic_failure():
    # Failed mission produces 0 final score
    res = ScoringEngine.calculate_score(
        level=4,
        mode="4P",
        base_engineering_score=750.0,
        survival=False,
        t_player=400.0,
        t_team=600.0,
        unused_hints=2,
        solved_puzzles=0
    )
    assert res["final_score"] == 0
    assert "CRITICAL SYSTEMS FAILURE" in res["cml_cert"]


def test_grace_overtime_decay():
    # Exceeding T_max doesn't crash or go negative; multiplier decays to 1.0
    res = ScoringEngine.calculate_score(
        level=1,
        mode="1P",
        base_engineering_score=500.0,
        survival=True,
        t_player=900.0, # Target is 480
        t_team=900.0,
        unused_hints=0,
        solved_puzzles=0
    )
    assert res["time_multiplier"] == 1.0
    assert res["final_score"] == 500
