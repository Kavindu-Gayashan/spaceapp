"""
Orbital Pulse - WebSocket Message Router & Live State Synchronizer
Handles real-time actions: component selection, hints, tutorials, crisis votes, and simulations.
"""

import json
import time
import asyncio
from typing import Dict, Any
from fastapi import WebSocket, WebSocketDisconnect

from orbital_pulse.server.rooms import room_manager, GameRoom
from orbital_pulse.models.components import COMPONENTS_BY_STATION
from orbital_pulse.models.characters import CHARACTERS, TRADE_STUDY_DIALOGUES
from orbital_pulse.models.tutorials import URSPACE_TUTORIALS
from orbital_pulse.models.puzzles import check_puzzle_solution, ASTRO_CALCULUS_PUZZLES
from orbital_pulse.engine.scoring import ScoringEngine
from orbital_pulse.engine.biomedicine import BiomedicineEngine


async def broadcast_room_state(room: GameRoom):
    """Broadcasts updated room state to all connected WebSockets in room."""
    data = {"type": "state_update", "payload": room.serialize_state()}
    msg_text = json.dumps(data)
    disconnected = []
    for pid, ws in room.connections.items():
        try:
            await ws.send_text(msg_text)
        except Exception:
            disconnected.append(pid)

    for pid in disconnected:
        if pid in room.connections:
            del room.connections[pid]


async def handle_websocket_connection(websocket: WebSocket, room_code: str, player_id: str, player_name: str):
    await websocket.accept()

    room = room_manager.get_room(room_code)
    if not room:
        await websocket.send_text(json.dumps({"type": "error", "message": f"Room {room_code} not found"}))
        await websocket.close()
        return

    # Register player in room
    room.connections[player_id] = websocket
    if player_id not in room.players:
        room.players[player_id] = {
            "id": player_id,
            "name": player_name,
            "ready": False,
            "stations": [],
            "role": "Mission Engineer"
        }

    # Re-assign stations for the mode
    room.assign_stations_for_mode()

    # Initial Welcome message
    if not room.dialogue_log:
        scenario = room.get_scenario()
        room.add_dialogue(
            "sterling",
            f"Welcome to the Mission Design Lab for {scenario['name']} ({scenario['cml']}). Configure your systems and prepare for launch!"
        )

    await broadcast_room_state(room)

    try:
        while True:
            text = await websocket.receive_text()
            msg = json.loads(text)
            action = msg.get("action")
            payload = msg.get("payload", {})

            if action == "start_mission":
                room.status = "designing"
                room.t_start = time.time()
                room.add_dialogue("chen", "Flight hardware bays open. All stations: begin preliminary design trade studies.")
                await broadcast_room_state(room)

            elif action == "select_component":
                station = payload.get("station")
                component_id = payload.get("component_id")

                # Verify ownership (or 1P mode)
                owns_station = (room.station_owners.get(station) == player_id) or (room.mode == "1P")
                if owns_station and station in COMPONENTS_BY_STATION:
                    # Find component in catalog
                    matched_comp = None
                    for comp in COMPONENTS_BY_STATION[station]:
                        if comp["id"] == component_id:
                            matched_comp = comp
                            break

                    room.selected_components[station] = matched_comp

                    # Check for character trade study banter
                    if component_id in TRADE_STUDY_DIALOGUES:
                        diag = TRADE_STUDY_DIALOGUES[component_id]
                        room.add_dialogue(diag["speaker"], diag["message"])

                    await broadcast_room_state(room)

            elif action == "use_hint":
                if room.unused_hints > 0:
                    room.unused_hints -= 1
                    eval_res = room.evaluate_systems()
                    bottlenecks = eval_res.get("bottlenecks", [])
                    if bottlenecks:
                        top = bottlenecks[0]
                        room.add_dialogue("chen", f"DIAGNOSTIC SCAN ALERT [{top['subsystem']}]: {top['issue']} Remedy: {top['remedy']}", is_shout=True)
                    else:
                        room.add_dialogue("chen", "DIAGNOSTIC SCAN: All subsystems within nominal flight tolerances! Ready for orbit.")
                    await broadcast_room_state(room)

            elif action == "open_tutorial":
                tut_id = payload.get("tutorial_id")
                if tut_id in URSPACE_TUTORIALS:
                    # Built-in safeguard 1: Freeze clock for up to 45 seconds on first view
                    if tut_id not in room.completed_tutorials:
                        room.freeze_timer_for_tutorial(45.0)
                        room.add_dialogue("rostova", f"Urspace Guide opened: '{URSPACE_TUTORIALS[tut_id]['title']}'. Mission clock temporarily frozen for 45s.")
                    await broadcast_room_state(room)

            elif action == "complete_tutorial":
                tut_id = payload.get("tutorial_id")
                if tut_id in URSPACE_TUTORIALS and tut_id not in room.completed_tutorials:
                    room.completed_tutorials.append(tut_id)
                    xp = URSPACE_TUTORIALS[tut_id].get("mastery_xp", 100)
                    room.mastery_xp += xp
                    room.add_dialogue("rostova", f"Urspace Guide Module Mastered! +{xp} Mastery XP awarded to squad.")
                    await broadcast_room_state(room)

            elif action == "solve_puzzle":
                puzzle_id = payload.get("puzzle_id")
                submitted_answer = float(payload.get("answer", 0.0))
                sol = check_puzzle_solution(puzzle_id, submitted_answer)

                if sol.get("is_correct"):
                    room.unused_hints = min(5, room.unused_hints + 1)
                    room.solved_puzzles += 1
                    room.add_dialogue("vance", f"ASTRO-CALCULUS REFILL SOLVED! '{puzzle_id}' verified (+1 Diagnostic Hint, +75 Bonus pts). {sol['step_solution']}")
                await websocket.send_text(json.dumps({"type": "puzzle_result", "payload": sol}))
                await broadcast_room_state(room)

            elif action == "station_ready":
                station = payload.get("station")
                now_elapsed = room.get_elapsed_seconds()
                room.station_done_times[station] = now_elapsed
                room.player_done_times[player_id] = now_elapsed
                if player_id in room.players:
                    room.players[player_id]["ready"] = True
                await broadcast_room_state(room)

            elif action == "start_simulation":
                # Advance to simulation phase
                room.status = "simulating"
                room.sim_active = True
                room.simulation_step = 1
                scenario = room.get_scenario()
                room.add_dialogue("vance", f"Ignition sequence start! Entering {scenario['target_orbit']}. Telemetry streaming live.")

                # If scenario has a mid-mission crisis, queue it
                crisis = scenario.get("crisis_event")
                if crisis:
                    room.active_crisis = crisis
                    room.add_dialogue("vance", f"EMERGENCY ADVISORY: {crisis['title']}! All stations report to crisis voting!", is_shout=True)

                await broadcast_room_state(room)

            elif action == "cast_crisis_vote":
                option_id = payload.get("option_id")
                room.crisis_votes[player_id] = option_id

                # Check if all connected players voted
                total_players = len(room.players)
                total_votes = len(room.crisis_votes)

                # In 1P, 1 vote resolves it. In multi, majority or full vote resolves it.
                if total_votes >= total_players or (room.mode == "1P" and total_votes >= 1):
                    # Tally votes
                    votes_count = {}
                    for opt in room.crisis_votes.values():
                        votes_count[opt] = votes_count.get(opt, 0) + 1
                    winning_option_id = max(votes_count, key=votes_count.get)

                    # Find winning option config
                    winning_opt = None
                    for opt in room.active_crisis["options"]:
                        if opt["id"] == winning_option_id:
                            winning_opt = opt
                            break

                    room.add_dialogue("vance", f"DECISION ADOPTED: '{winning_opt['label']}'! {winning_opt['explanation']}")

                    # If Level 4, simulate biomedical trauma result
                    if room.level == 4:
                        mitigations = room.evaluate_systems().get("active_mitigations", [])
                        bio_sim = BiomedicineEngine.simulate_trauma_crisis(
                            vance_vitals=room.vance_vitals,
                            active_mitigations=mitigations,
                            power_allocated_medical_w=950.0 if winning_opt.get("effect", {}).get("stabilization") else 200.0,
                            telemedicine_link_active=True,
                            fast_return_selected=not winning_opt.get("effect", {}).get("stabilization"),
                            elapsed_seconds=room.get_elapsed_seconds()
                        )
                        room.vance_vitals = bio_sim
                        if bio_sim["patient_survived"]:
                            room.add_dialogue("rostova", f"Vance Vitals: {bio_sim['status_text']} HR: {bio_sim['heart_rate_bpm']} bpm, BP: {bio_sim['blood_pressure_sys']}/{bio_sim['blood_pressure_dia']} mmHg.")
                        else:
                            room.add_dialogue("rostova", f"CRITICAL CASUALTY: {bio_sim['status_text']}", is_shout=True)

                    # Clear crisis
                    room.active_crisis = None
                    room.crisis_votes = {}
                    await broadcast_room_state(room)

            elif action == "finish_mission":
                # Compute final forensic debrief
                room.status = "debrief"
                systems_eval = room.evaluate_systems()
                t_team = room.get_elapsed_seconds()
                t_player = room.player_done_times.get(player_id, t_team)

                survival = systems_eval.get("all_passed", False)
                if room.level == 4:
                    survival = survival and room.vance_vitals.get("patient_survived", True)

                score_data = ScoringEngine.calculate_score(
                    level=room.level,
                    mode=room.mode,
                    base_engineering_score=systems_eval.get("base_engineering_score", 500.0),
                    survival=survival,
                    t_player=t_player,
                    t_team=t_team,
                    unused_hints=room.unused_hints,
                    solved_puzzles=room.solved_puzzles
                )

                debrief_payload = {
                    "score": score_data,
                    "systems": systems_eval,
                    "scenario": room.get_scenario(),
                    "vance_vitals": room.vance_vitals if room.level == 4 else None,
                    "nasa_mission_match": room.get_scenario().get("nasa_mission_match")
                }

                data = {"type": "mission_debrief", "payload": debrief_payload}
                msg_text = json.dumps(data)
                for ws in room.connections.values():
                    try:
                        await ws.send_text(msg_text)
                    except Exception:
                        pass
                await broadcast_room_state(room)

            elif action == "send_chat":
                msg_content = payload.get("message", "").strip()
                if msg_content:
                    speaker_id = player_name.lower().replace(" ", "_")
                    entry = {
                        "id": f"msg_{len(room.dialogue_log)+1}",
                        "speaker_id": speaker_id,
                        "speaker_name": player_name,
                        "speaker_title": room.players.get(player_id, {}).get("role", "Flight Controller"),
                        "speaker_avatar": "👩‍🚀",
                        "speaker_color": "#38bdf8",
                        "message": msg_content,
                        "is_shout": False,
                        "timestamp": round(room.get_elapsed_seconds(), 1)
                    }
                    room.dialogue_log.append(entry)
                    await broadcast_room_state(room)

    except WebSocketDisconnect:
        if player_id in room.connections:
            del room.connections[player_id]
        if player_id in room.players:
            room.players[player_id]["connected"] = False
        await broadcast_room_state(room)
