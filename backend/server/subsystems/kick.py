from ..subsystem import Subsystem

kick = Subsystem("Kicking people")
@kick.on("player")
async def kick_player(message, room):
    try:
        name = message["name"]
        if name in room.players:
            player = room.players[name]
            await player.websocket.close()
            del room.players[name]
            await room.update_players()
    except:
        pass
