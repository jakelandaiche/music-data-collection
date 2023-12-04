import json
import asyncio
import websockets

from player import Player
from game import Game

ROOMS = dict()

class Room:
    """ room """
    DESTROY_TIMEOUT=60*15

    def __init__(self, websocket, key):
        print("Room created")

        self.key = key 
        self.websocket = websocket

        self.players = dict()
        self.show_answers = False
        self.history = []
        self.room_text = ""
        
        self.message_handlers = []

        self.queue = asyncio.Queue()
        self.messages = asyncio.Queue()


        self.task = asyncio.create_task(self.run())


    def broadcast(self, message):
        websockets.broadcast( (player.websocket for player in self.players) , message)


    async def set_countdown(self, t):
        countdown_message = {
                "type": "countdown",
                "time": t
                }
        await self.websocket.send(json.dumps(countdown_message))

    async def update_frontend(self):
        update_message = {
                "type": "update",
                "players": [player.to_obj() for player in self.players.values()],
                "text": self.room_text,
                "show_answers": self.show_answers 
                }
        await self.websocket.send(json.dumps(update_message))

    async def run(self):
        init_message = {
                "type": "init",
                "join": self.key
                }
        await self.websocket.send(json.dumps(init_message))

        while True:
            message = await self.messages.get()

            # handle websocket messages
            if "ws_id" in message:
                ws_id = message["ws_id"]

                # host connection close
                if message["type"] == "conn_close" and ws_id == self.websocket.id:
                    print("Room closing in 15 minutes, bye")
                    self.destruct_task = asyncio.create_task(self.destruct())

                # host reconnect 
                    # should cancel self.destruct_task

                # start game
                if message["type"] == "start" and ws_id == self.websocket.id:
                    self.game = Game(self, 3)
                    asyncio.create_task(self.game.run())

                # player connection close
                if message["type"] == "conn_close" and ws_id in self.players:
                    print("Player left")
                    del self.players[ws_id]
                    await self.update_frontend()

                # new player
                if message["type"] == "player_data": 
                    print("New player")
                    player = Player(message["username"])
                    self.players[ws_id] = player
                    await self.update_frontend()

                # answer 
                if message["type"] == "answer" and ws_id in self.players: 
                    print("Answer")
                    self.players[ws_id].answer = message["text"]


            print(f"Message in room {self.key}: {message}")

            self.messages.task_done()


    async def destruct(self):
        await asyncio.sleep(self.DESTROY_TIMEOUT)
        del ROOMS[self.key]
        self.task.cancel()

