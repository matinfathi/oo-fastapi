from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.user.schemas import UserRead
from app.user.models import OoUserModel as User
from app.core.security import get_current_user
from app.core.database import get_session


user_router = APIRouter()


@user_router.get("/list")
async def list_users(
    current_user: Annotated[UserRead, Depends(get_current_user)], session: Annotated[Session, Depends(get_session)]
) -> list[UserRead]:
    if not current_user.role == "SuperAdmin":
        raise HTTPException(status_code=403, detail="Not enough permission.")
    return session.exec(select(User)).all()
