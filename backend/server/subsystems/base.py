from asyncio import create_task

from ..subsystem import Subsystem
from ..game import game_task 
from ..room import Room

base = Subsystem("Base room functionality")

@base.on("start")
async def start_game(message, room):
    num_players = len(room.players) 
    all_ready = all(player.ready for player in room.players.values())
    tutorial = message["tutorial"] 

    if (num_players >= Room.MIN_TO_START) and all_ready:
        print("starting!")
        room.game = create_task(game_task(room, N=room.nrounds, tutorial=tutorial))
    elif room.debug:
        room.game = create_task(game_task(room, N=room.nrounds, tutorial=tutorial))


@base.on("restart")
async def restart(_, room):
    room.game = None
    for player in room.players.values():
        player.ready = False
    await room.update_players()
    await room.broadcast({
        "type": "reset",
        })


@base.on("dataset")
async def update_dataset(message, room):
    room.dataset = message["dataset"]


@base.on("nrounds")
async def update_nrounds(message, room):
    room.nrounds = int(message["nrounds"])


@base.on("playercolor")
async def update_player_color(message, room):
    player = room.players[message["name"]]
    player.color = message["color"]
    await room.update_players()


@base.on("playerready")
async def update_player_ready(message, room):
    player = room.players[message["name"]]
    player.ready = message["ready"]
    await room.update_players()

