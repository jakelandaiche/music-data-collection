import asyncio
import logging

from asyncio import CancelledError
from data import get_videos
from database import Database

from .utils import Sub
from .room import Room
from .tutorial import tutorial_task

logger = logging.getLogger(__name__)

from .room import Room


async def game_task(room: Room, N=5, tutorial=True):
    """"""

    logger.info(f"Starting game with {room.dataset} and {N} rounds")

    try:
        if room.debug:
            db = Database(file="debug.db")
        else:
            db = Database()
        game_id = db.create_game()
    except Exception:
        logger.exception("game_task: Database error")
        return

    try:
        videos = get_videos(N=N, dataset=room.dataset)
    except Exception:
        logger.exception("game_task: Error retrieving videos")
        return

    try:
        # Init
        for player in room.players.values():
            try:
                player.db_id = str(db.create_player(player.name, game_id))
            except Exception:
                logger.exception("Database")
            player.clear()
            player.total = 0
        await room.update_players()

        # Game Start
        await room.broadcast({
            "type": "state", 
            "state": "GAMESTART",
            "duration": 15
            })
        await asyncio.sleep(15)

        # Tutorial
        if tutorial:
            await tutorial_task(room)

        # Do rounds
        for n in range(1, N + 1):
            # Reset scores
            for player in room.players.values():
                player.clear()
            await room.update_players()

            # Update round number
            await room.send({
                "type": "round_num",
                "round_num": n,
                })

            # Round Start
            await room.broadcast({
                "type": "state", 
                "state": "ROUNDSTART",
                "duration": 15,
                })
            video = videos[n-1]
            await room.send(
                {"type": "video", "id": video["id"], "start_time": video["start_time"]}
            )
            await asyncio.sleep(15)

            # Collect answers
            await room.broadcast({
                "type": "state", 
                "state": "ROUNDCOLLECT",
                "duration": 30
                })

            try:
                await asyncio.wait_for(wait_for_answers(room), timeout=30)
            except TimeoutError:
                logger.info("Timeout")


            # Compute scores
            try:
                with_answers = [player for player in room.players.values() if player.answer is not None]
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
                    player.unique.update(score_infos[i].unique_words)
                    player.wc += score_infos[i].word_count
                    player.wl += score_infos[i].word_len

            except Exception:
                logger.exception("Scoring")

            try:
                for player in room.players.values():
                    db.write_answer(player, n, video["id"])
            except Exception:
                logger.exception("Database")

            # Round end 
            await room.update_players()
            await room.broadcast({
                "type": "state", 
                "state": "ROUNDEND",
                "duration": 45 
                })
            await asyncio.sleep(45)

        await room.broadcast(
            {
                "type": "player_stats",
                "player_stats": [p.to_obj() for p in room.players.values()],
            }
        )

        await room.broadcast({
            "type": "state", 
            "state": "GAMEEND",
            "duration": 0,
            })

    except asyncio.CancelledError:
        logger.info(f"{room.code}: Game cancelled")
        raise
    except Exception:
        logger.exception(f"{room.code}: Exception while running game")
    finally:
        db.cur.close()
        db.con.close()
        room.game = None


async def wait_for_answers(room: Room):
    try:
        with Sub(room.messages) as queue:
            while True:
                try:
                    message = await queue.get()
                    t = message["type"]

                    if t == "answer":
                        name = message["name"]
                        room.players[name].answer = message["answer"]
                        await room.update_players()

                    if all(
                        player.answer is not None for player in room.players.values()
                    ):
                        break
                except KeyError:
                    pass

        logger.info("Received all answers")
    except CancelledError:
        logger.info("Did not receive all answers")
    finally:
        return
