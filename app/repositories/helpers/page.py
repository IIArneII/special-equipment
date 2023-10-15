from sqlalchemy.orm import Query
from typing import TypeVar, Type

from app.services.models.base import Page, BaseFilter


T = TypeVar('T')


def build_page(model: Type[T], query: Query, filter: BaseFilter) -> Page[T]:
    count = query.count()
    elements = query.offset((filter.page - 1) * filter.limit).limit(filter.limit).all()
    
    elements = [model.model_validate(e) for e in elements]

    return Page[model].get_page(elements, filter.page, filter.limit, count)
