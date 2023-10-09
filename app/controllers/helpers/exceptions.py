from fastapi import HTTPException, status


CREDENTIALS_ERR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

FORBIDDEN_ERR = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden",
    )
