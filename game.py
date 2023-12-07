import asyncio
import json
import random

from data import get_videos
from database import Database


def decide_winner(answers):
    return random.choice(answers)


class Game:
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
    ]

    def __init__(self, room, N):
        self.state = "START"
        self.room = room
        self.N = N
        self.db = Database()
        self.game_id = self.db.create_game()

    def score_answers(self, answers: list[str]):
        scores = []
        for i in range(len(answers)):
            score = 0
            mult = 10
            answer_l = answers[i].replace(".", "").replace(",", "").split(" ")
            answer_s = set(answer_l)
            for word in answer_s:
                if word not in self.common_words:
                    if mult < 20:
                        mult += 1
                    for j in range(len(answers)):
                        if j != i:
                            score += 1 if answers[j].count(word) else 0
            scores.append(score * mult)
        return scores

    async def run(self):
        # game explanation
        self.room.room_text = (
            f"<h3>MusicBox</h3>" + "Welcome to MusicBox. The game will start soon"
        )
        await self.room.update_frontend()
        await self.room.set_countdown(15)
        await asyncio.sleep(17)

        for player in self.room.players.values():
            player.db_id = self.db.create_player(player.name, self.game_id)

        for i in range(self.N):
            # play audio
            for player in self.room.players.values():
                player.answer = ""
            self.room.show_answers = False
            video = get_videos()[0]
            msg = {
                "type": "video",
                "id": video["id"],
                "start_time": video["start_time"],
            }
            await self.room.websocket.send(json.dumps(msg))

            self.room.room_text = (
                f"<h3>Round {i+1}</h3>" + "Listen to this audio carefully"
            )
            await self.room.update_frontend()
            await self.room.set_countdown(15)
            await asyncio.sleep(17)

            # collect answers
            self.room.room_text = f"<h3>Round {i+1}</h3>" + "Put down your answers"
            await self.room.update_frontend()
            await self.room.set_countdown(30)
            await asyncio.sleep(32)

            # round end
            usernames = []
            answers = []
            for player in self.room.players.values():
                usernames.append(player.name)
                answers.append(player.answer)

            for username, score in zip(usernames, self.score_answers(answers)):
                self.db.write_answer(username, score)

            print(f"results for {video['id']}")
            print(answers)
            self.room.room_text = f"<h3>Round {i+1}</h3>" + "The answers revealed"
            self.room.show_answers = True
            await self.room.update_frontend()
            await self.room.set_countdown(15)
            await asyncio.sleep(17)

        self.room.room_text = "The game is over. Thanks for playing"
        self.db.cur.close()
        self.db.con.close()
        await self.room.update_frontend()
