from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    limit: int
    total: int
    pages: int

def paginate(items: list[T], page: int, limit: int, total: int) -> PaginatedResponse[T]:
    pages = (total + limit - 1) // limit if limit > 0 else 0
    return PaginatedResponse(
        items=items,
        page=page,
        limit=limit,
        total=total,
        pages=pages
    )
