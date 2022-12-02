from http import HTTPStatus
from os import environ
from secrets import compare_digest

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

VALID_API_KEY = environ["VALID_API_KEY"]


def validate_api_key(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> None:
    if compare_digest(cred.credentials, VALID_API_KEY):
        return
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED, detail="invalid credentials"
    )
