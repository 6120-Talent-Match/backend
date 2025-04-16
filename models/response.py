from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class StandardResponse(BaseModel, Generic[T]):
  data: Optional[T] = None
  error: Optional[str] = None


def createSuccessResponse(data: Any) -> StandardResponse:
  return StandardResponse(data=data, error=None)


def createErrorResponse(message: str) -> StandardResponse:
  return StandardResponse(data=None, error=message)
