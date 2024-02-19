import json
from asyncio import create_task

from .utils import generate_code
from .room import ROOMS, Room
from .subsystem import Subsystem

from .subsystems.base import base
from .subsystems.echo import echo


SUBSYSTEMS: list[Subsystem] = [echo, base]


async def ws_handler(websocket):
    """
    WebSocket connection handler, determines what type of connection
    (player or host) and then pushes messages to the correct room
    """

    print(f"New connection: {websocket.remote_address}, {websocket.id}")

    info = await get_info(websocket)
    if info is None:
        return

    if info["type"] == "host":
        print(f"{websocket.remote_address} is host")
        room: Room = info["room"]
        await room.bind_host(websocket)

    if info["type"] == "player":
        print(f"{websocket.remote_address} is player")
        room: Room = info["room"]
        name = info["name"]
        await room.bind_player(websocket, name)

    print(f"{websocket.remote_address}: Handler terminated")


async def get_info(websocket):
    """
    Consumes websocket messages until either an "init" or a "join"
    message is read. Then it will attempt to find or create the
    corresponding room. It will also check if the player exists
    """

    # Consume websocket messages
    async for message in websocket:

        # Check if message is json
        try:
            message = json.loads(message)
        except:
            continue

        # Message must have type
        if "type" not in message:
            continue

        # Case: Message type is "init"
        # (Host connection)
        if message["type"] == "init":

            code = message.get("code", generate_code())
            if code in ROOMS:
                room = ROOMS[code]
            else:
                room = Room()
                for subsystem in SUBSYSTEMS:
                    print(f"Installing {subsystem.name}")
                    room.subsystems.add(create_task(subsystem.bind(room)))
                ROOMS[code] = room

            # Done
            return {"type": "host", "room": room}

        # Case: Message type is "join"
        # (Player connection)
        if message["type"] == "join":
            # "join" message must have "code"
            if "code" in message:
                code = message["code"]
                if code in ROOMS:
                    # Get room if exists
                    room = ROOMS[code]
                else:
                    # If not, ignore
                    continue
            else:
                continue

            # "join" message must have "name"
            if "name" in message:
                name = message["name"]
            else:
                continue

            return {"type": "player", "room": room, "name": name}

    # Can only reach here if connection was closed
    return None
