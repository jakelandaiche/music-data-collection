import sqlite3
import time

INITSCRIPT = """
CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, date);
CREATE TABLE IF NOT EXISTS players(id INTEGER PRIMARY KEY, username, game, FOREIGN KEY(game) REFERENCES games(id));
CREATE TABLE IF NOT EXISTS answers(id INTEGER PRIMARY KEY, answer, round, score, player, video_id, FOREIGN KEY(player) REFERENCES players(id));
CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY, round, tags, norm_val, FOREIGN KEY(round) references rounds(id));
"""

class Database:
    def __init__(self, file="musicbox.db"):
        self.con = sqlite3.connect(file)
        self.cur = self.con.executescript(INITSCRIPT)

    def create_game(self):
        self.cur.execute(f"INSERT INTO games(date) VALUES('{time.time()}')")
        self.con.commit()
        return self.cur.lastrowid

    def create_player(self, name, game_id):
        self.cur.execute(
            f"INSERT INTO players(username, game) VALUES('{name}', {game_id})"
        )
        self.con.commit()
        return self.cur.lastrowid

    def write_answer(self, player, round, video_id):
        self.cur.execute(
            f"INSERT INTO answers(answer, round, score, player, video_id) VALUES('{player.answer}', {round}, {player.score}, {player.db_id}, '{video_id}')"
        )
        self.con.commit()
