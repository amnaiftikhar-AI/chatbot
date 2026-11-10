from rank_bm25 import BM25Okapi
import re

class BM25Store:
    def __init__(self):
        self.items = []
        self.index = None

    def build(self, items):
        self.items = items
        tokens = [re.findall(r"[a-zA-Z0-9_\-]+", item["content"].lower()) for item in items]
        self.index = BM25Okapi(tokens) if tokens else None

    def search(self, query, k=8):
        if self.index is None:
            return []
        tokens = re.findall(r"[a-zA-Z0-9_\-]+", query.lower())
        scores = self.index.get_scores(tokens)
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [dict(self.items[i], score=float(scores[i]), rank=rank + 1) for rank, i in enumerate(order) if scores[i] > 0]
