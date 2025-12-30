from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.schemas import UserRead
from app.user.services import UserServices

from app.core.security import get_current_user
from app.core.database_async import get_session
from app.core.dependencies import get_user_service


user_router = APIRouter()


@user_router.get("/list")
async def list_users(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[UserServices, Depends(get_user_service)],
) -> list[UserRead]:
    return await service.list_users(current_user=current_user, session=session)
