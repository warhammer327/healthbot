# RAG Healthcare Knowledge Assistant

A FastAPI backend for a bilingual (English/Japanese) RAG-powered assistant.

---

## Project Structure

```
healthbot
├── app
│   ├── core
│   ├── dependencies.py
│   ├── __init__.py
│   ├── main.py
│   ├── middleware
│   │   ├── authenticate.py
│   │   └── __init__.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── generate.py
│   │       ├── ingest.py
│   │       ├── __init__.py
│   │       └── retrieve.py
│   ├── schemas
│   │   ├── base_response.py
│   │   ├── generate.py
│   │   ├── ingest.py
│   │   ├── __init__.py
│   │   └── retrieve.py
│   ├── services
│   │   ├── generation_service.py
│   │   ├── ingestion_service.py
│   │   └── retrieval_service.py
│   └── utils
│       └── translate.py
├── data
│   └── answers.txt
├── docker-compose.yml
├── Dockerfile
├── __pycache__
│   └── main.cpython-313.pyc
├── pyproject.toml
├── README.md
├── requirements.txt
└── uv.lock
```

---

## Requirements

- Python 3.13+
- Docker 23+
- Sample knowledge source is at project-root/data/answers.txt
- Internet connection

> **Note:** On first run, the sentence-transformer model will be downloaded. This may take some time depending on internet connection.

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

---

## Start

```bash
docker compose up
```

The API will be available at `http://localhost:8000`.  
Swagger docs at `http://localhost:8000/docs`.

All requests require the header `X-API-Key: abcd`. It is hardcoded at the moment, move it to env before deployment.

---

## API Usage

All endpoints require the header:

```
X-API-Key: abcd
```

---

### `POST /ingest`

Upload a `.txt` document, it generates an embedding, and stores it in FAISS.

**Example**

```bash
curl -X POST http://localhost:8000/v1/ingest  \
  -H "X-API-Key: abcd"  \
  -F "file=@{project-root-addresss}/data/answers.txt"
```

**Response**

```json
{
  "success":true,
  "error":null,
  "filename":"answers.txt"
}
```

---

> kb_language is the language of knowledgebase.

### `POST /retrieve`

Submit a query in English or Japanese. Returns the top-3 most relevant documents with similarity scores.

**Example**

```bash
# English output 
curl "http://localhost:8000/v1/retrieve?query=What+is+a+fever&kb_language=en&output_language=en" \
  -H "X-API-Key: abcd"
```

```json
{
  "success":true,
  "error":null,
  "results":[
    {"rank":2,"score":3.7711,"chunk":"What is the definition of a fever in an adult?\nA body temperature of 100.4°F (38°C) or higher."},
    {"rank":2,"score":13.2865,"chunk":"What are the classic symptoms of a myocardial infarction (heart attack) in men?\nChest pain or pressure, pain radiating to the left arm or jaw, shortness of breath, and diaphoresis (sweating)."},
    {"rank":3,"score":14.5788,"chunk":"What does a \"pulse oximeter\" measure?\nThe oxygen saturation level (SpO2) in the blood, indicating how well oxygen is being delivered to the body."}
  ]
}
```

```bash
# Japanese output
curl "http://localhost:8000/v1/retrieve?query=What+is+a+fever&kb_language=en&output_language=ja" \
  -H "X-API-Key: abcd"
```

```json
{"success":true,
  "error":null,
  "results":[
    {"rank":1,"score":3.7711,"chunk":"成人の発熱の定義は何ですか?\n体温が38℃以上であること。"},
    {"rank":2,"score":13.2865,"chunk":"男性の心筋梗塞（心臓発作）の典型的な症状は何ですか?\n胸の痛みや圧迫感、左腕や顎に広がる痛み、息切れ、発汗（発汗）。"},
    {"rank":3,"score":14.5788,"chunk":"「パルスオキシメーター」は何を測定するのですか？\n血液中の酸素飽和度 (SpO2) は、酸素が体にどの程度届けられているかを示します。"}
  ]
}
```

---

### `POST /generate`

Combines retrieved documents with the query to produce a mock LLM response. Responds in the same language as the query.

**Example**

```bash
# English output 
curl "http://localhost:8000/v1/generate?query=What+is+a+fever&kb_language=en" \
  -H "X-API-Key: abcd"
```

```json
{
  "success":true,
  "error":null,
  "response":"Based on the available medical guidelines:\n\nWhat is the definition of a fever in an adult?\nA body temperature of 100.4°F (38°C) or higher.\nWhat are the classic symptoms of a myocardial infarction (heart attack) in men?\nChest pain or pressure, pain radiating to the left arm or jaw, shortness of breath, and diaphoresis (sweating).\nWhat does a \"pulse oximeter\" measure?\nThe oxygen saturation level (SpO2) in the blood, indicating how well oxygen is being delivered to the body.\n\nIn summary, the retrieved information addresses your query about: What is a fever"
}
```

```bash
# Japanese output
 curl -G "http://localhost:8000/v1/generate?kb_language=en" \
  --data-urlencode "query=発熱とは何ですか" \
  -H "X-API-Key: abcd"
```

```json
{
  "success":true,
  "error":null,
  "response":"利用可能な医療ガイドラインに基づいて:\n\n成人の発熱の定義は何ですか?\n体温が38℃以上であること。\n男性の心筋梗塞（心臓発作）の典型的な症状は何ですか?\n胸の痛みや圧迫感、左腕や顎に広がる痛み、息切れ、発汗（発汗）。\n「パルスオキシメーター」は何を測定するのですか？\n血液中の酸素飽和度 (SpO2) は、酸素が体にどの程度届けられているかを示します。\n\n要約すると、取得された情報は、「発熱とは何か」という質問に答えます。"
}
```

---

## Notes

- Data is stored **in-memory** — it resets on container restart. Re-ingest your file after restarting.
- The `generate` endpoint uses a mock LLM response (no actual model call), it just wraps the retrieved chunks.
- Supported output languages for `/retrieve`: `en`, `ja`.
- The API key is hardcoded as `abcd` — move it to an environment variable before any real deployment.
