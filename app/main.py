from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
