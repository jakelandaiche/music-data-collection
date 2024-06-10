"""
Room module
"""

import logging
import json

from asyncio import Task, create_task, sleep, CancelledError
from typing import Iterable 

from websockets.server import WebSocketServerProtocol as Socket
from websockets.exceptions import ConnectionClosed

from scoring import Scorer

from .utils import Hub, send
from .player import Player

logger = logging.getLogger(__name__)

class Room:
    """ 
    A Room object. 

    Holds data for each room, including a message queue that aggregates socket messages.
    """
    MAX_PLAYERS = 8 
    MIN_TO_START = 3
    

    def __init__(self, code: str, socket=None, debug=True):
        self.code = code
        self.debug = debug
        self.dead = False
        self.tutorial = False

        # The Host WebSocket tied to this room.
        self.socket: Socket | None = socket 
        
        # The centralized message queue for this room.
        self.messages = Hub()

        # The running systems
        self.subsystems: set[Task] = set()

        # Players and their timeouts
        self.players: dict[str, Player] = dict()

        # This holds the timeout task, which is called whenever
        # the room loses the host websocket.
        # It gets cancelled if a new host websocket reconnects to it
        self.destroy_task: Task | None = None

        # Game info
        self.dataset: str = "musicCaps1.csv"
        self.nrounds: int = 5

        # The currently running game
        self.game: Task | None = None

        self.scorer = Scorer()


    @property
    def connections(self) -> Iterable[Socket]:
        return (player.websocket for player in self.players.values() if player.websocket is not None)


    @property
    def nconnected(self) -> int:
        return sum(1 for player in self.players.values() if player.connected)


    async def bind_host(self, socket: Socket):
        """
        Registers a WebSocket as the room's host websocket,
        and consumes messages from it until its closure
        """

        logger.debug(f"{socket.remote_address[0]}: Trying to bind to room {self.code}")

        # Check if room already has a host socket
        if self.socket is not None:
            return

        if self.destroy_task is not None:
            self.destroy_task.cancel("Host socket reestablished")
            self.destroy_task = None

        # Set socket and return init message
        self.socket = socket
        await socket.send(json.dumps({
            "type": "init",
            "code": self.code
            }))

        
        # Push messages to queue
        async for message in socket:
            message = json.loads(message)
            self.messages.pub(message)
        
        # Remove websocket
        # Note code can only reach here if connection was closed
        self.socket = None
        self.destroy_task = create_task(self.destroy_timeout())

    

    async def bind_player(self, websocket: Socket, name: str):
        """
        Registers a WebSocket as the websocket for one 
        of the players.

        A player is either created or rebound as necessary
        """

        logger.debug(f"Trying to bind player {name}...")
    
        # If there are too many players, don't
        if self.nconnected >= Room.MAX_PLAYERS:
            return
        
        # Check if there is already a player with the given name
        if name in self.players:
            if not self.players[name].connected:
                # Resend player info
                await send(websocket, {
                    "type": "playerinfo",
                    "player": self.players[name].to_obj()
                    })
            else:
                # Player is already connected
                return
        else:
            # Create player
            self.players[name] = Player(name=name)

        # Bind websocket to player
        self.players[name].websocket = websocket
        self.players[name].connected = True
        
        # Send init message
        await send(websocket, {
            "type": "init",
            "code": self.code
            })

        await self.update_players()

        # Push messages
        async for message in websocket:
            message = json.loads(message)
            self.messages.pub(message)

        # Remove websocket
        # Note code can only reach here if connection was closed
        self.players[name].websocket = None
        self.players[name].connected = False
        await self.update_players()
        

    async def update_players(self):
        """
        Sends over all player information to the Host 
        websocket
        """
        players = [player.to_obj() for player in self.players.values() if player.connected]
        await self.send({"type":"players", "players":players})


    async def destroy_timeout(self, timeout=10):
        try:
            logger.debug(f"{self.code}: Marking self dead in {timeout} seconds")
            await sleep(timeout)

            self.dead = True
            for subsystem in list(self.subsystems):
                subsystem.cancel()
                await subsystem
            for connection in list(self.connections):
                await connection.close()
            
        except CancelledError:
            logger.debug(f"{self.code}: Self-destruct cancelled")


    async def send(self, message: dict):
        """Send a message to the Host websocket"""
        if self.socket is not None:
            try:
                await send(self.socket, message)
            except ConnectionClosed:
                pass
        else:
            logger.debug("Attempted to send message to nonexistent Host socket")


    async def broadcast(self, message, with_host=True):
        """
        Sends a message to all websockets, with the option
        to also send to the host WebSocket (true by default)
        """
        logger.info(list(self.connections))
        logger.info(message)
        for connection in self.connections:
            logger.info(connection)
            await send(connection, message)

        if with_host:
            await self.send(message)

