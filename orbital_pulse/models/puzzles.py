"""
Orbital Pulse - Astro-Calculus Refill Terminal Puzzles
Directly implements Section 5.4 of the Master Project Proposal.
"""

from typing import Dict, List, Any


ASTRO_CALCULUS_PUZZLES: List[Dict[str, Any]] = [
    {
        "id": "puz_derivative_power",
        "title": "Calculus Derivative: Instantaneous Power Drain",
        "concept": "First Derivative (dE / dt = P)",
        "question": (
            "During a deep lunar eclipse, battery energy E(t) (in Watt-hours) drops according to the quadratic equation: "
            "E(t) = 600 - 5t², where t is time in hours. "
            "What is the instantaneous power drain |dE / dt| at t = 4 hours?"
        ),
        "formula": r"P(t) = \left|\frac{dE}{dt}\right| = \left|\frac{d}{dt}(600 - 5t^2)\right| = 10t",
        "hint": "Take the derivative with respect to t: d/dt(600) = 0, d/dt(-5t²) = -10t. Then evaluate at t = 4.",
        "unit": "Watts (W)",
        "correct_answer": 40.0,
        "tolerance": 0.5,
        "step_solution": "dE/dt = -10t. At t = 4 hr, |dE/dt| = 10 * 4 = 40 Watts.",
        "reward_hints": 1,
        "reward_points": 75
    },
    {
        "id": "puz_maxima_apogee",
        "title": "Calculus Maxima: Sounding Probe Apogee Scan",
        "concept": "Optimization / Critical Points (dh / dt = 0)",
        "question": (
            "A prospecting sounding probe's altitude above a crater floor follows the trajectory: "
            "h(t) = -3t² + 30t + 15 (km). "
            "At what time t (in seconds) does it reach peak altitude (apogee) to trigger the hyperspectral spectrometer?"
        ),
        "formula": r"\frac{dh}{dt} = -6t + 30 = 0 \implies t = \frac{30}{6}",
        "hint": "Set the first derivative dh/dt equal to zero to find the stationary point (maximum altitude).",
        "unit": "seconds (s)",
        "correct_answer": 5.0,
        "tolerance": 0.1,
        "step_solution": "dh/dt = -6t + 30. Setting -6t + 30 = 0 gives 6t = 30, so t = 5 seconds.",
        "reward_hints": 1,
        "reward_points": 75
    },
    {
        "id": "puz_integral_xenon",
        "title": "Calculus Integral: Ion Thruster Propellant Burn",
        "concept": "Definite Integral (∫ r(t) dt)",
        "question": (
            "An electric ion thruster gradually ramps up its xenon propellant burn rate according to r(t) = 3t² grams per hour. "
            "How many total grams of xenon propellant are consumed from t = 0 to t = 3 hours?"
        ),
        "formula": r"m_{\text{xenon}} = \int_0^3 3t^2 \, dt = \left[ t^3 \right]_0^3 = 3^3 - 0^3",
        "hint": "Integrate 3t² with respect to t: the antiderivative is t³. Evaluate [t³] from t=0 to t=3.",
        "unit": "grams (g)",
        "correct_answer": 27.0,
        "tolerance": 0.5,
        "step_solution": "∫ 3t² dt = t³. Evaluating between 0 and 3 gives 3³ - 0³ = 27 grams.",
        "reward_hints": 1,
        "reward_points": 75
    },
    {
        "id": "puz_inverse_square",
        "title": "Deep-Space Solar Flux: Inverse-Square Scaling",
        "concept": "Inverse-Square Law (P ∝ 1 / r²)",
        "question": (
            "A high-efficiency solar array produces 800 W at Earth orbit (r = 1.0 AU). "
            "Using the Inverse-Square Law (Power ∝ 1 / r²), how much power will it produce at a metallic asteroid located at r = 2.0 AU?"
        ),
        "formula": r"P(r) = P_0 \times \left(\frac{r_0}{r}\right)^2 = 800 \times \left(\frac{1}{2}\right)^2 = \frac{800}{4}",
        "hint": "Power scales inversely with distance squared. At 2 AU, the distance is doubled, so the area over which light spreads is quadrupled (2² = 4).",
        "unit": "Watts (W)",
        "correct_answer": 200.0,
        "tolerance": 2.0,
        "step_solution": "P(2 AU) = 800 / (2.0)² = 800 / 4 = 200 Watts.",
        "reward_hints": 1,
        "reward_points": 75
    },
    {
        "id": "puz_eclss_oxygen",
        "title": "Biomedical Life-Support: ECLSS Mass Balance",
        "concept": "ECLSS Oxygen Mass Balance & Rate Integration",
        "question": (
            "An injured astronaut in the trauma stabilization pod consumes 0.9 kg of O₂ per day. "
            "If your Lunar Ice Reactor extracts 0.15 kg of O₂ per hour, how many total hours must it run to produce the oxygen required for a 3-day emergency return to Earth?"
        ),
        "formula": r"t_{\text{run}} = \frac{0.9 \text{ kg/day} \times 3 \text{ days}}{0.15 \text{ kg/hour}}",
        "hint": "First calculate total oxygen required: 0.9 kg/day * 3 days = 2.7 kg. Then divide by the extraction rate of 0.15 kg/hr.",
        "unit": "hours",
        "correct_answer": 18.0,
        "tolerance": 0.2,
        "step_solution": "Total O₂ needed = 0.9 * 3 = 2.7 kg. Extraction time = 2.7 / 0.15 = 18 hours.",
        "reward_hints": 1,
        "reward_points": 75
    }
]


def check_puzzle_solution(puzzle_id: str, submitted_answer: float) -> Dict[str, Any]:
    """Verifies user answer against puzzle criteria."""
    for puzzle in ASTRO_CALCULUS_PUZZLES:
        if puzzle["id"] == puzzle_id:
            diff = abs(float(submitted_answer) - puzzle["correct_answer"])
            is_correct = diff <= puzzle["tolerance"]
            return {
                "puzzle_id": puzzle_id,
                "is_correct": is_correct,
                "submitted_answer": submitted_answer,
                "correct_answer": puzzle["correct_answer"],
                "unit": puzzle["unit"],
                "step_solution": puzzle["step_solution"],
                "reward_hints": puzzle["reward_hints"] if is_correct else 0,
                "reward_points": puzzle["reward_points"] if is_correct else 0
            }
    return {"error": "Puzzle not found", "is_correct": False}
