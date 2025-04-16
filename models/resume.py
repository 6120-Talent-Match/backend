# models.py - Pydantic models for data validation
from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any


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
