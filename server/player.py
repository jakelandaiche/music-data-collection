from websockets.server import WebSocketServerProtocol as Socket

from dataclasses import dataclass, field


class PlayerStats:
    def __init__(self):
        self._num_answers = 0
        self._average_length = 0
        self._unique_words = set()

    def count_unique(self):
        return len(self._unique_words)

    def update_length(self, new_len):
        self._num_answers += 1
        self._average_length = (
            self._average_length + (new_len - self._average_length) / self._num_answers
        )


@dataclass(eq=False, frozen=False)
class Player:
    """
    A dataclass that holds fields for a Player, which is
    a member of a Room
    """

    websocket: Socket | None
    name: str

    color: str = "#000000"
    color_list: list[int] = field(default_factory=list)
    ready: bool = False
    answer: str | None = None
    score: int = 0
    total: int = 0
    db_id: str | None = None
    stats: PlayerStats = None

    @property
    def connected(self):
        return self.websocket is not None

    def to_obj(self):
        return {
            "name": self.name,
            "connected": self.connected,
            "color": self.color,
            "color_list": self.color_list,
            "ready": self.ready,
            "answer": self.answer,
            "score": self.score,
            "total": self.total,
            "db_id": self.db_id,
        }


class PlayerManager:
    def __init__(self):
        pass
