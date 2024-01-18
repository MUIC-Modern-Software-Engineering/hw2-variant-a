from dataclasses import dataclass
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlmodel import select
from starlette import status

from leave_system.app import LeaveSystemEngineDep
from leave_system.models import User


@dataclass
class UserSession:
    user_id: int
    username: str


security = HTTPBasic()


def throw_401(msg: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        headers={"WWW-Authenticate": "Basic"},
    )


def get_current_username(
        lse: LeaveSystemEngineDep,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> UserSession:
    input_username = credentials.username
    input_password = credentials.password.encode('utf8')
    with lse.database.session() as session:
        user = session.exec(select(User).where(User.username == input_username)).first()
    if user is None:
        throw_401("Incorrect username or password")

    good_pass = bcrypt.checkpw(input_password, user.password)
    if not good_pass:
        throw_401("Incorrect username or password")
    return UserSession(
        user_id=user.id,
        username=user.username
    )


UserSessionDep = Annotated[UserSession, Depends(get_current_username)]
