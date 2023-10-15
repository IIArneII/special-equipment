from pydantic import BaseModel as PydanticBaseModel, Field
from datetime import datetime
from humps import camelize
from math import ceil
from typing import TypeVar, Generic


T = TypeVar('T')


class BaseModel(PydanticBaseModel):
    class Config:
        alias_generator = camelize
        populate_by_name = True
        from_attributes = True
        use_enum_values = True


class EntityBaseModel(BaseModel):
    id: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime


class Page(BaseModel, Generic[T]):
    elements: list[T]
    page: int = Field(ge=1)
    limit: int = Field(ge=1, le=100)
    total_pages: int = Field(ge=0)
    total_elements: int = Field(ge=0)

    def get_page(elements: list[T], page: int, limit: int, total_elements: int):
        elements_page = Page(
            elements = elements,
            page=page,
            limit=limit,
            total_elements=total_elements,
            total_pages=0,
        )
        elements_page.total_elements = ceil(total_elements / limit)
        return elements_page


class BaseFilter(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)
