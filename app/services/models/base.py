from pydantic import BaseModel as PydanticBaseModel, Field
from datetime import datetime
from fastapi import Query
from humps import camelize


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


class Page(BaseModel):
    page: int = Field(ge=1)
    limit: int = Field(ge=1, le=100)
    total_pages: int = Field(ge=0)
    total_elements: int = Field(ge=0)


class Filter(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)

    def get_filter(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
        return Filter(page=page, limit=limit)
