import faiss
import numpy as np
from app.dependencies import model, index, chunks


class IngestionService:
    @staticmethod
    def ingest_text(content: str) -> int:
        global chunks
        # Group every 2 non-empty lines as one Q&A chunk
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        new_chunks = [
            f"{lines[i]}\n{lines[i + 1]}" for i in range(0, len(lines) - 1, 2)
        ]
        embeddings = model.encode(new_chunks).astype(np.float32)
        index.add(embeddings)
        chunks.extend(new_chunks)
        return len(new_chunks)
