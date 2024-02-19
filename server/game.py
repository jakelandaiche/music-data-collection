import asyncio
import math
from asyncio import CancelledError

from data import get_videos
from database import Database
from similarity import Similarity

from .utils import Sub
from .room import Room


async def game_task(room: Room, N=5):
    print(f"Starting game with {room.dataset} and {N} rounds")
    try:
        db = Database()
        game_id = db.create_game()
    except Exception as e:
        print("Database error")
        print(e)
        return

    try:
        videos = get_videos(N=N, dataset=room.dataset)
    except Exception as e:
        print("Error retrieving videos")
        print(e)

    try:
        # Init
        for player in room.players.values():
            try:
                player.db_id = db.create_player(player.name, game_id)
            except Exception as e:
                print("Database error")
                print(e)
            player.answer = None
            player.total = 0
            player.score = 0
            player.color_list = []
        await room.update_players()

        # Game Start
        await room.broadcast({"type": "state", "state": "GAMESTART"})
        await asyncio.sleep(15)

        for n in range(1, N + 1):
            # Reset scores
            for player in room.players.values():
                player.answer = None
                player.score = 0
                player.color_list = []
            await room.update_players()

            # Update round number
            await room.send(
                {
                    "type": "round_num",
                    "round_num": n,
                }
            )

            # Round Start
            await room.broadcast({"type": "state", "state": "ROUNDSTART"})
            video = videos[n - 1]
            await room.send(
                {"type": "video", "id": video["id"], "start_time": video["start_time"]}
            )
            await asyncio.sleep(20)

            # Collect answers
            await room.broadcast({"type": "state", "state": "ROUNDCOLLECT"})
            try:
                await asyncio.wait_for(wait_for_answers(room), timeout=30)
            except TimeoutError:
                pass

            # Compute scores
            try:
                compute_scores(room)
            except Exception as e:
                print("Error computing scores")
                print(e)

            try:
                for player in room.players.values():
                    db.write_answer(player, n)
            except Exception as e:
                print("Error writing to database")
                print(e)

            # Round end
            await room.update_players()
            await room.broadcast({"type": "state", "state": "ROUNDEND"})
            await asyncio.sleep(30)

        await room.broadcast({"type": "state", "state": "GAMEEND"})

    except asyncio.CancelledError:
        raise
    except Exception as e:
        print("Error in game")
        print(e)
    finally:
        db.cur.close()
        db.con.close()
        room.game = None


sim_checker = Similarity()

common_words = [
    "the",
    "be",
    "to",
    "of",
    "and",
    "a",
    "in",
    "that",
    "have",
    "it",
    "for",
    "not",
    "on",
    "with",
    "as",
    "at",
    "if",
    "music",
    "this",
    "then",
    "he",
    "is",
    "or",
    "i",
    "so",
]


def compute_scores(room):
    with_answers = [
        player for player in room.players.values() if player.answer is not None
    ]
    sim_scores = sim_checker.sim_scores([player.answer for player in with_answers])
    colors: dict[str, int] = {"the": 0}

    for i in range(len(with_answers)):
        player = with_answers[i]
        score = math.floor(sim_scores[i] * 1000)
        mult = 0

        # get words
        answer_l = player.answer.replace(".", "").replace(",", "").split(" ")
        answer_s = set()

        matches = 0

        for word in answer_l:
            if word not in common_words:
                if word not in answer_s:
                    # increase multiplier for each unique uncommon word
                    if mult < 20:
                        mult += 1
                match = False
                # more points for words in common with others
                for other in with_answers:
                    if other is not player and other.answer.count(word):
                        match = True
                if match:
                    matches += 1
                    # keep track of what words have been matching and assign each a number
                    if word not in colors:
                        colors[word] = max(colors.values()) + 1
                    player.color_list.append(colors[word])
                else:
                    player.color_list.append(0)
                answer_s.add(word)
            else:
                player.color_list.append(0)

        player.score = (score + matches ^ 2) * (1 + mult / 100)
        player.total = player.total + player.score


async def wait_for_answers(room):
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
                    print("No key")

        print("Received all answers")
    except CancelledError:
        print("Did not receive all answers")
    finally:
        return
