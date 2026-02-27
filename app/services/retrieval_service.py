import numpy as np
from app.dependencies import model, index, chunks


class RetrievalService:
    @staticmethod
    def retrieve(query: str, top_k: int = 3) -> list[dict]:
        if index.ntotal == 0:
            return []
        embedding = model.encode([query]).astype(np.float32)
        distances, indices = index.search(embedding, min(top_k, index.ntotal))
        return [
            {
                "rank": rank + 1,
                "score": round(float(distances[0][rank]), 4),
                "chunk": chunks[i],
            }
            for rank, i in enumerate(indices[0])
        ]
