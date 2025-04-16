# 🧠 Talent Match Backend

This is the backend service for **Talent Match**, a CS6120 final project.

Built with [FastAPI](https://fastapi.tiangolo.com/) and [PostgreSQL](https://www.postgresql.org/), the service enables intelligent resume storage and retrieval. With the help of the [pgvector](https://github.com/pgvector/pgvector) extension, all resume entries are vectorized to support semantic search based on skills and experience.

---

## 🚀 Getting Started

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

> Make sure you have PostgreSQL installed with the `pgvector` extension enabled.

### 🗃️ Database Schema

```python
class ResumeBase(BaseModel):
    id: str
    category: str
    skills: List[str]
    education: List[str]
    experience: List[str]
```

### ▶️ Run the API Server

```bash
python api.py
```

---

## 📡 API Usage

### 🔍 Resume Search

#### Request Schema

```python
class SearchQuery(BaseModel):
    skills: List[str] = []
    experience: List[str] = []
    top_n: Optional[int] = 5
```

#### Response Schema

```python
class SearchResult(BaseModel):
    id: str
    category: str
    similarity_score: float
    skills: List[str]
    education: List[str]
    experience: List[str]

class SearchResponse(BaseModel):
    results: List[SearchResult]
```

Send a POST request to `/search` with `skills` and/or `experience` to retrieve the most relevant resumes using vector similarity.

---

## 🧠 Features

- Fast and lightweight API with **FastAPI**
- **pgvector**-powered semantic search
- JSON-based schema for simple integration
- Ideal for resume matching, HR tools, or AI recruiting systems

---

## 📄 License

Licensed under the [Apache License 2.0](LICENSE).

---

Built with ❤️ for CS6120 Final Project