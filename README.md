# Intro

This is the backend of Talent Match, CS6120 final project.

It is built with [PostgreSQL](https://www.postgresql.org/) and [FastAPI](https://fastapi.tiangolo.com/).

With this service, users can upload resume data including skills, education, experience and etc. With ![pgvector](https://github.com/pgvector/pgvector) extention, data will be vectorized, so users can search for resume by similarity.

# Get Started

```Python
pip install requirements.txt
```

Setup database with [pgvector](https://github.com/pgvector/pgvector) extention.

## Schema

```Python
class ResumeBase(BaseModel):
  id: str
  category: str
  skills: List[str]
  education: List[str]
  experience: List[str]
```

Run the service.
```Python
python api.py
```

# Usage

## Request and Response Schema

```Python
class ResumeBase(BaseModel):
  id: str
  category: str
  skills: List[str]
  education: List[str]
  experience: List[str]

class SearchQuery(BaseModel):
  skills: List[str] = []
  experience: List[str] = []
  top_n: Optional[int] = 5


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