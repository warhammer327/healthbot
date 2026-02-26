# RAG Healthcare Knowledge Assistant

A FastAPI backend for a bilingual (English/Japanese) RAG-powered assistant.

---

## Project Structure

```
rag-healthcare-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entry point + all route definitions
│   ├── auth.py          # X-API-Key header authentication
│   ├── embeddings.py    # FAISS index management + sentence-transformers
│   └── translate.py     # Bilingual translation (googletrans)
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI/CD pipeline
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.13+
- Docker

> **Note:** On first run, the sentence-transformer model will be downloaded automatically. This may take a minute or two depending on your connection. Subsequent starts will use the cached model and load instantly.

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

---

## Docker Setup

### Build the image

```bash
docker build -t healthbot .
```

### Run the container

```bash
docker run -e API_KEY=your-secret-key -p 8000:8000 healthbot
```

---

## API Usage

All endpoints require the header:

```
X-API-Key: your-secret-key
```

---

### `POST /ingest`

Upload a `.txt` document in English or Japanese. The app auto-detects the language, generates an embedding, and stores it in FAISS.

**Request** — `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `file` | `.txt` | Plain text document to ingest |

**Example**

```bash
curl -X POST http://localhost:8000/ingest \
  -H "X-API-Key: your-secret-key" \
  -F "file=@guidelines.txt"
```

**Response**

```json
{
  "message": "Ingested successfully",
  "language": "en",
  "doc_id": 0
}
```

---

### `POST /retrieve`

Submit a query in English or Japanese. Returns the top-3 most relevant documents with similarity scores.

**Request** — `application/json`

```json
{
  "query": "What are the latest recommendations for Type 2 diabetes management?"
}
```

**Example**

```bash
curl -X POST http://localhost:8000/retrieve \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "Type 2 diabetes management"}'
```

**Response**

```json
{
  "results": [
    {
      "doc_id": 0,
      "text": "...",
      "language": "en",
      "score": 0.91
    }
  ]
}
```

---

### `POST /generate`

Combines retrieved documents with the query to produce a mock LLM response. Responds in the same language as the query. Optionally translates output.

**Request** — `application/json`

```json
{
  "query": "2型糖尿病の管理について教えてください",
  "output_language": "en"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | Your question in EN or JA |
| `output_language` | `"en"` or `"ja"` | No | Force output language (defaults to query language) |

**Example**

```bash
curl -X POST http://localhost:8000/generate \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "diabetes treatment", "output_language": "ja"}'
```

**Response**

```json
{
  "query": "diabetes treatment",
  "language_detected": "en",
  "output_language": "ja",
  "response": "糖尿病の治療に関して、以下の情報が見つかりました：..."
}
```

---

## CI/CD (GitHub Actions)

TBD

---

## Design Notes

**Scalability & Modularity**  

**Future Improvements**  

---

## AI Usage Disclosure

This project was built with the assistance of Claude (Anthropic). All code and written content was reviewed, understood, and verified by the submitter.
