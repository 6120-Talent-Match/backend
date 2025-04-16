# api.py - FastAPI application
from fastapi import FastAPI, HTTPException, Depends
from typing import List
import uvicorn

from db import TalentMatchDB
from search import ResumeSearchEngine
from config import settings
from models.resume import ResumeBase, SearchQuery, SearchResponse, SearchResult
from models.response import createSuccessResponse, createErrorResponse, StandardResponse

app = FastAPI(title="TalentMatch AI API")


def get_db():
  return TalentMatchDB(settings.db_params)


def get_search_engine():
  return ResumeSearchEngine(settings.db_params)


@app.post("/resumes", status_code=201)
async def add_resume(resume: ResumeBase, db: TalentMatchDB = Depends(get_db)):
  try:
    db.insert_resume(resume.dict())
    return createSuccessResponse(None)
  except Exception as e:
    return createErrorResponse(str(e))


@app.post("/search")
async def search_resumes(query: SearchQuery, search_engine: ResumeSearchEngine = Depends(get_search_engine)):
  try:
    results = search_engine.search(
        skills=query.skills, experience=query.experience, top_n=query.top_n)
    # Create SearchResponse
    search_response = SearchResponse(results=results)
    # Wrap it in StandardResponse
    return createSuccessResponse(search_response)
  except Exception as e:
    return createErrorResponse(str(e))


@app.get("/health")
async def health_check():
  return createSuccessResponse(None)

if __name__ == "__main__":
  uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
