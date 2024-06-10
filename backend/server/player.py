from dataclasses import dataclass, field
from websockets.server import WebSocketServerProtocol as Socket

from scoring import ScoreInfo

@dataclass(eq=False, frozen=False)
class Player:
    """
    A dataclass that holds fields for a Player, which is
    a member of a Room
    """

    name: str
    color: str = "#000000"
    connected: bool = False
    ready: bool = False
    answer: str | None = None
    score: int = 0
    total: int = 0
    db_id: str | None = None
    score_info: ScoreInfo | None = None
    wc: int = 1
    wl: int = 0
    unique: set = field(default_factory=set)

    def __post__init__(self):
        self.websocket: Socket | None = None

    def clear(self):
        self.answer = None
        self.score = 0
        self.score_info = None

    def to_obj(self):
        return {
            "name": self.name,
            "connected": self.connected,
            "color": self.color,
            "ready": self.ready,
            "answer": self.answer,
            "score": self.score,
            "total": self.total,
            "db_id": self.db_id,
            "score_info": self.score_info.to_obj() if self.score_info is not None else None,
            "unique_words": len(self.unique),
            "avg_len": self.wl/self.wc if self.wc != 0 else None,
        }
