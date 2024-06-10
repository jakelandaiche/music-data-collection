from dataclasses import dataclass, field

@dataclass
class ScoreInfo:
    bonus: str
    matches: int
    similarity: int
    unique_words: set[str] = field(default_factory=set)
    word_count: int = 0
    word_len: int = 0

    def to_obj(self):
        return {
            "bonus": self.bonus,
            "matches": self.matches,
            "similarity": self.similarity,
            "unique_words": list(self.unique_words),
            "word_count": self.word_count,
            "word_len": self.word_len,
        }

