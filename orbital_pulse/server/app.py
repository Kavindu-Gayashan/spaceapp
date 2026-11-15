"""
Orbital Pulse - FastAPI Application Server
Provides REST endpoints and WebSocket mounting for the Mission Control Deck.
"""

import os
from pathlib import Path
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from orbital_pulse.server.rooms import room_manager
from orbital_pulse.server.ws import handle_websocket_connection
from orbital_pulse.models.campaign import CAMPAIGN_LEVELS
from orbital_pulse.models.tutorials import URSPACE_TUTORIALS
from orbital_pulse.models.puzzles import ASTRO_CALCULUS_PUZZLES
from orbital_pulse.models.components import COMPONENTS_BY_STATION

app = FastAPI(title="Orbital Pulse", description="NASA Space Apps Challenge 2026 - Space Mission Design Game")

# Static files directory
STATIC_DIR = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class CreateRoomRequest(BaseModel):
    host_name: str
    mode: str = "1P"
    level: int = 1
    preferred_code: str = ""


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    return FileResponse(index_file)


@app.post("/api/rooms/create")
async def create_room(req: CreateRoomRequest):
    room = room_manager.create_room(
        host_name=req.host_name,
        mode=req.mode,
        level=req.level,
        preferred_code=req.preferred_code or None
    )
    return {
        "success": True,
        "room_code": room.room_code,
        "mode": room.mode,
        "level": room.level,
        "host_name": room.host_name
    }


@app.get("/api/rooms/{code}")
async def get_room_info(code: str):
    room = room_manager.get_room(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "room_code": room.room_code,
        "host_name": room.host_name,
        "mode": room.mode,
        "level": room.level,
        "status": room.status,
        "player_count": len(room.players)
    }


@app.get("/api/campaign/levels")
async def get_levels():
    return CAMPAIGN_LEVELS


@app.get("/api/tutorials")
async def get_tutorials():
    return URSPACE_TUTORIALS


@app.get("/api/puzzles")
async def get_puzzles():
    return ASTRO_CALCULUS_PUZZLES


@app.get("/api/components")
async def get_components():
    return COMPONENTS_BY_STATION


@app.websocket("/ws/{room_code}/{player_id}/{player_name}")
async def websocket_route(websocket: WebSocket, room_code: str, player_id: str, player_name: str):
    await handle_websocket_connection(websocket, room_code, player_id, player_name)
