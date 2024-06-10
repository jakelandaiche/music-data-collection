import asyncio

from .room import Room
from dataclasses import replace

async def tutorial_task(room: Room):
    print("Tutorial (fake game)")

    fake_players = [replace(player) for player in room.players.values()]
    fake_answers = [
        "This is a song about a woman being happy that she is young and succesful.",
        "Chill pop song with an interesting out of tune horns.",
        "A woman singing in a low, repetitive, quiet voice about being successful. The song has a moderately fast tempo and features detuned horns.",
        "ARIANA GRANDE",
        "The track unfolds as a vibrant sonic tapestry, blending pulsating beats with the artist's vocals. Its buoyant energy and uplifting lyrics create a musical journey that encapsulates the essence of triumph and accomplishment by repeating the word successful.",
        "A successful woman",
        "A womans singing over minimal arrangement",
        "uhh",
    ]

    async def update_fake_players():
        objs = [player.to_obj() for player in fake_players]
        await room.send({"type": "players", "players": objs})

    for player in fake_players:
        player.answer = None
        player.total = 0
        player.score = 0
        player.score_info = None

    # Round Start
    await room.broadcast({
        "type": "state", 
        "state": "FAKEROUNDSTART",
        "duration": 15 
        })
    await update_fake_players()
    await room.send({"type": "video", "id": "_IvArrFhcp0", "start_time": 52})
    await asyncio.sleep(15)

    # Collect
    await room.broadcast({
        "type": "state", 
        "state": "FAKEROUNDCOLLECT",
        "duration": 20
        })
    # Input fake answers at timed intervals
    for player, answer in zip(fake_players, fake_answers):
        await asyncio.sleep(1)
        player.answer = answer
        await update_fake_players()
    await asyncio.sleep(1)

    # Compute scores
    try:
        with_answers = [player for player in fake_players if player.answer is not None]
        answers = [player.answer for player in with_answers if player.answer is not None]
        scores, score_infos, match_words = room.scorer.compute_scores(answers)
        await room.send({
            "type": "matchlist",
            "matchlist": match_words 
            })

        for i, player in enumerate(with_answers):
            player.score = scores[i]
            player.total += scores[i]
            player.score_info = score_infos[i]

    except Exception as e:
        print("Error computing scores")
        print(e)

    # Round End
    await update_fake_players()
    await room.broadcast({
        "type": "state", 
        "state": "FAKEROUNDEND",
        "duration": 20
        })
    await asyncio.sleep(20)

    # Round End 2
    await update_fake_players()
    await room.broadcast({
        "type": "state", 
        "state": "FAKEROUNDEND2",
        "duration": 10
        })
    await asyncio.sleep(10)


