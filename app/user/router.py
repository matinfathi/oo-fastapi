from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from app.user.schemas import UserRead, UserCreate, UserCreateByAdmin, UserUpdate
from app.user.services import UserServices

from app.core.security import get_current_user
from app.core.database_async import get_session
from app.core.dependencies import get_user_service


user_router = APIRouter()


@user_router.get("/list", tags=["Users"])
async def list_users(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[UserServices, Depends(get_user_service)],
) -> list[UserRead]:
    return await service.list_users(current_user=current_user, session=session)


@user_router.get("/get", tags=["Users"])
async def get_user(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[UserServices, Depends(get_user_service)],
    user_id: Annotated[int | None, Query()] = None,
    email: Annotated[EmailStr | None, Query()] = None,
    username: Annotated[str | None, Query()] = None,
) -> UserRead:
    return await service.get_user(
        current_user=current_user, session=session, user_id=user_id, email=email, username=username
    )


@user_router.post("/add", tags=["Users"])
async def create_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[UserServices, Depends(get_user_service)],
    user_data: UserCreate,
) -> UserRead:
    return await service.create_user(session=session, user_data=user_data)


@user_router.post("/add_by_admin", tags=["Users"])
async def create_user_by_admin(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[UserServices, Depends(get_user_service)],
    user_data: UserCreateByAdmin,
) -> UserRead:
    return await service.create_user_by_admin(current_user=current_user, session=session, user_data=user_data)


@user_router.patch("/patch/{user_id}", tags=["Users"])
async def update_user(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[UserServices, Depends(get_user_service)],
    user_data: UserUpdate,
    user_id: int,
) -> UserRead:
    return await service.update_user(current_user=current_user, session=session, user_data=user_data, user_id=user_id)


@user_router.delete("/delete/{user_id}", tags=["Users"])
async def delete_user(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[UserServices, Depends(get_user_service)],
    user_id: int,
) -> dict:
    return await service.delete_user(current_user=current_user, session=session, user_id=user_id)
