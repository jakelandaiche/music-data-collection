from sentence_transformers import SentenceTransformer, util

class Similarity:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    def sim_scores(self, sentences: list[str]):
        scores = []
        tensors = [self.model.encode(s, convert_to_tensor=True) for s in sentences]
        l = len(tensors)
        if l == 1:
            return [0]
        for x in range(l):
            tot = 0
            cur = tensors[x]
            for y in range(l):
                if y != x:
                    tot += util.pytorch_cos_sim(tensors[y], cur).item()
            scores.append(tot / (l - 1))
        return scores

