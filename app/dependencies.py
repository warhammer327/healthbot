import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "paraphrase-multilingual-mpnet-base-v2",
)

# In-memory store: index + chunks
index = faiss.IndexFlatL2(768)
chunks: list[str] = []
