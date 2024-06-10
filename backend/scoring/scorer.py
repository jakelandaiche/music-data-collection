import math 
import re
from collections import defaultdict

from .info import ScoreInfo 
from .similarity import Similarity

common_words = {"the", "and", "that", "have", "for", "not", "with", "music"}

class Scorer:
    def __init__(self):
        self.sim_checker = Similarity()

    """
    Processes a list of answers, returning in order:
    -   Scores
    -   Score info
    -   A list of all match words
    """
    def compute_scores(self, answers: list[str]) -> tuple[list[int], list[ScoreInfo], list[str]]:
        # Compute similarity scores
        sim_scores = self.sim_checker.sim_scores(answers)
        answer_sim_scores = [math.floor(sim_score*1000) for sim_score in sim_scores]

        # Strip answers of punctuation and non-space whitespace
        stripped_answers = [re.sub('[^A-za-z0-9]+', ' ', answer).lower() for answer in answers]
        answer_wc = [len(answer.split()) for answer in stripped_answers]
        answer_wl = [sum(len(word) for word in answer) for answer in stripped_answers]

        # Get unique words
        unfiltered_answer_words = [set(answer.split()) for answer in stripped_answers]

        # Filter out by length and common words
        def filter_words(words: set[str]):
            return set(word for word in words if len(word) > 2) - common_words 
        answer_words = [filter_words(words) for words in unfiltered_answer_words]
        
        # Count repeat words between answers
        word_frequency: defaultdict[str, int] = defaultdict(int)
        for words in answer_words:
            for word in words:
                word_frequency[word] += 1

        # Contains words that have matches, 
        # and how many matches each word has (frequency - 1)
        word_matches: dict[str, int] = dict()
        for word, frequency in word_frequency.items():
            if frequency > 1:
                word_matches[word] = frequency - 1
         
        # Get number of matches for each answer
        def sum_matches(words: set[str]):
            return sum(word_matches[word] for word in words if word in word_matches)
        answer_matches = [sum_matches(words) for words in answer_words]

        # Compute multipliers
        def compute_multiplier(matches: int):
            return min(matches/10, 1.0) * 0.35
        answer_multipliers = [compute_multiplier(matches) for matches in answer_matches]

        # Compute scores
        def compute_score(i: int):
            sim_score = answer_sim_scores[i]
            multiplier = 1 + answer_multipliers[i]
            matches = answer_matches[i]
            score = (sim_score + matches**2) * multiplier
            return int(score)
        scores: list[int] = []
        for i in range(len(answers)):
            scores.append(compute_score(i))

        # Create ScoreInfo list
        score_infos: list[ScoreInfo] = []
        for i in range(len(answers)):
            score_infos.append(ScoreInfo(
                bonus=f"{100*answer_multipliers[i]:.3f}%",
                similarity=answer_sim_scores[i],
                matches=answer_matches[i],
                unique_words=answer_words[i],
                word_count=answer_wc[i],
                word_len=answer_wl[i]
            ))

        # Done
        return scores, score_infos, list(word_matches.keys()) 
