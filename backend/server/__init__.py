"""
The MusicBox Server class
"""
import asyncio
import logging
import websockets
import ssl
import json

from typing import Coroutine
from dataclasses import dataclass
from asyncio import Task, create_task
from websockets.server import WebSocketServerProtocol as Socket

from .room import Room
from .subsystems.base import base
from .utils import generate_code

logger = logging.getLogger(__name__)

@dataclass
class ServerOptions:
    host: str = "localhost"
    port: int = 8080

    file: str = "filtered.csv"
    debug: bool = False
    ssl: bool = True 
    ssl_cert = "/home/jake/music-data-collection/fullchain1.pem"
    ssl_key = "/home/jake/music-data-collection/privkey1.pem"

class Server:

    rooms: dict[str, Room] = dict()

    def __init__(self, opts=ServerOptions()):
        self.opts = opts
        self.tasks: set[Task] = set()


    def create_task(self, coro: Coroutine):
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)


    async def start(self):
        if self.opts.ssl:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(self.opts.ssl_cert, keyfile=self.opts.ssl_key)
        else:
            ssl_context = None

        async with websockets.serve(
            self.ws_handler, self.opts.host, self.opts.port, ssl=ssl_context
        ):
            logger.info(f"Starting on {self.opts.host}:{self.opts.port}")
            await asyncio.Future()


    async def ws_handler(self, websocket: Socket):
        """
        WebSocket connection handler, determines what type of connection
        (player or host) and then pushes messages to the correct room
        """
        logger.info(f"{websocket.remote_address[0]}: New connection")

        info = await self.get_info(websocket)
        if info is None:
            return

        code: str = info["room"]
        room: Room = self.rooms[code]

        # Host connection
        if info["type"] == "host":
            logger.info(f"{websocket.remote_address[0]}: Is Host")
            await room.bind_host(websocket)

        # Player connection
        if info["type"] == "player":
            logger.info(f"{websocket.remote_address[0]}: Is Player")
            name = info["name"]
            await room.bind_player(websocket, name)

        logger.info(f"{websocket.remote_address[0]}: Socket handler terminated")


    async def get_info(self, websocket):
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
            except Exception as ex:
                logger.error(f"Message was not json: {ex}")
                continue

            # Message must have type
            if "type" not in message:
                continue

            # Case: Message type is "init"
            # (Host connection)
            if message["type"] == "init":
                new_code = generate_code()
                code = message.get("code", new_code)
                if code in self.rooms:
                    # Get room if exists
                    room = self.rooms[code]
                else:
                    room = Room(new_code, None, self.opts.debug)
                    room.subsystems.add(create_task(base.bind(room)))

                    self.rooms[code] = room

                # Clean out dead rooms
                to_del = []
                for key, room in self.rooms.items():
                    if room.dead:
                        to_del.append(key)
                for key in to_del:
                    del self.rooms[key]

                return {"type": "host", "room": code}

            # Case: Message type is "join"
            # (Player connection)
            if message["type"] == "join":
                # "join" message must have "code"
                if "code" in message:
                    code = message["code"]
                    if code in self.rooms:
                        # Get room if exists
                        room = self.rooms[code]
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

                return {"type": "player", "room": code, "name": name}

        # Can only reach here if connection was closed
        return None
