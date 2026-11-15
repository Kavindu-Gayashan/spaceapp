"""
Unit tests for Astro-Calculus Refill Terminal Puzzles
Directly tests Section 5.4 puzzle solutions.
"""

import pytest
from orbital_pulse.models.puzzles import check_puzzle_solution, ASTRO_CALCULUS_PUZZLES


def test_puzzle_derivative():
    # Puzzle 1: |dE/dt| at t=4 for E = 600 - 5t^2 -> answer 40 W
    res = check_puzzle_solution("puz_derivative_power", 40.0)
    assert res["is_correct"] is True
    assert res["reward_hints"] == 1
    assert res["reward_points"] == 75

    # Wrong answer
    res_wrong = check_puzzle_solution("puz_derivative_power", 25.0)
    assert res_wrong["is_correct"] is False


def test_puzzle_maxima():
    # Puzzle 2: peak altitude for h(t) = -3t^2 + 30t + 15 -> answer t = 5 s
    res = check_puzzle_solution("puz_maxima_apogee", 5.0)
    assert res["is_correct"] is True


def test_puzzle_integral():
    # Puzzle 3: integral of 3t^2 from 0 to 3 -> answer 27 g
    res = check_puzzle_solution("puz_integral_xenon", 27.0)
    assert res["is_correct"] is True


def test_puzzle_inverse_square():
    # Puzzle 4: 800W at 1 AU -> at 2 AU answer is 200 W
    res = check_puzzle_solution("puz_inverse_square", 200.0)
    assert res["is_correct"] is True


def test_puzzle_eclss():
    # Puzzle 5: 0.9 kg/day * 3 days / 0.15 kg/hr -> answer 18 hours
    res = check_puzzle_solution("puz_eclss_oxygen", 18.0)
    assert res["is_correct"] is True
