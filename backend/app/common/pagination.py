from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    page: int = Field(ge=1)
    limit: int = Field(ge=1, le=100)
    total: int
    pages: int


def build_page(items: list[T], total: int, page: int, limit: int) -> Page[T]:
    return Page(items=items, page=page, limit=limit, total=total, pages=ceil(total / limit) if total else 0)
