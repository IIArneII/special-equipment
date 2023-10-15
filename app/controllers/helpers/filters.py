from fastapi import Depends, Query

from app.services.users import UserFilter


def user_filter(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        username: str | None = Query(None),
        email: str | None = Query(None),
    ) -> UserFilter:
    return UserFilter(
        page=page,
        limit=limit,
        username=username,
        email=email,
    )
