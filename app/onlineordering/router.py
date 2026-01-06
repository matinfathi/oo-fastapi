from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.schemas import UserRead
from app.onlineordering.services import OptionServices, OptionGroupService, ItemServices
from app.onlineordering.schemas import (
    OptionRead,
    OptionCreate,
    OptionPatch,
    OptionGroupRead,
    OptionGroupCreate,
    OptionGroupPatch,
    ItemRead,
    ItemPatch,
    ItemCreate,
    CategoryRead,
    CategoryCreate,
    CategoryPatch,
)

from app.core.security import get_current_user
from app.core.database_async import get_session
from app.core.dependencies import get_option_service, get_option_group_service, get_item_service


oo_router = APIRouter()


@oo_router.get("/list-option/{option_group_id}", tags=["Option"])
async def list_option(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionServices, Depends(get_option_service)],
    option_group_id: int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
) -> list[OptionRead]:
    return await service.list_option(
        session=session, current_user=current_user, option_group_id=option_group_id, offset=offset, limit=limit
    )


@oo_router.get("/get-option/{option_id}", tags=["Option"])
async def get_option(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionServices, Depends(get_option_service)],
    option_id: int,
) -> OptionRead:
    return await service.get_option(session=session, current_user=current_user, option_id=option_id)


@oo_router.post("/create-option/{option_group_id}", tags=["Option"])
async def create_option(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionServices, Depends(get_option_service)],
    option_group_id: int,
    option_data: OptionCreate,
) -> OptionRead:
    return await service.create_option(
        session=session, current_user=current_user, option_group_id=option_group_id, option_data=option_data
    )


@oo_router.delete("/delete-option/{option_id}", tags=["Option"])
async def delete_option(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionServices, Depends(get_option_service)],
    option_id: int,
) -> dict:
    return await service.delete_option(session=session, current_user=current_user, option_id=option_id)


@oo_router.patch("/patch-option/{option_id}", tags=["Options"])
async def patch_option(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionServices, Depends(get_option_service)],
    option_id: int,
    option_data: OptionPatch,
) -> OptionRead:
    return await service.patch_option(
        session=session, current_user=current_user, option_id=option_id, option_data=option_data
    )


########################################################################################################################
@oo_router.get("/list-option-group/{item_id}", tags=["Option Group"])
async def list_option_group(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionGroupService, Depends(get_option_group_service)],
    item_id: int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
) -> list[OptionGroupRead]:
    return await service.list_option(
        session=session, current_user=current_user, item_id=item_id, offset=offset, limit=limit
    )


@oo_router.get("/get-option-group/{option_group_id}", tags=["Option Group"])
async def get_option_group(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionGroupService, Depends(get_option_group_service)],
    option_group_id: int,
) -> OptionGroupRead:
    return await service.get_option_group(session=session, current_user=current_user, option_group_id=option_group_id)


@oo_router.post("/create-option-group/{item_id}", tags=["Option Group"])
async def create_option_group(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionGroupService, Depends(get_option_group_service)],
    item_id: int,
    option_group_data: OptionGroupCreate,
) -> OptionGroupRead:
    return await service.create_option_group(
        session=session, current_user=current_user, item_id=item_id, option_group_data=option_group_data
    )


@oo_router.patch("/patch-option-group/{option_group_id}", tags=["Option Group"])
async def patch_option_group(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionGroupService, Depends(get_option_group_service)],
    option_group_id: int,
    option_group_data: OptionGroupPatch,
) -> OptionGroupRead:
    return await service.patch_option_group(
        session=session, current_user=current_user, option_group_id=option_group_id, option_group_data=option_group_data
    )


@oo_router.delete("/delete-option-group/{option_group_id}", tags=["Option Group"])
async def delete_option_group(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[OptionGroupService, Depends(get_option_group_service)],
    option_group_id: int,
) -> dict:
    return await service.delete_option_group(
        session=session, current_user=current_user, option_group_id=option_group_id
    )


########################################################################################################################
@oo_router.get("/list-item/{category}", tags=["Item"])
async def list_item(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    category: int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
) -> list[ItemRead]:
    return await service.list_item(
        session=session, current_user=current_user, category_id=category, offset=offset, limit=limit
    )


@oo_router.get("/get-item/{item_id}", tags=["Item"])
async def get_item(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    item_id: int,
) -> ItemRead:
    return await service.get_item(session=session, current_user=current_user, item_id=item_id)


@oo_router.post("/create-item/{category_id}", tags=["Item"])
async def create_item(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    category_id: int,
    item_data: ItemCreate,
) -> ItemRead:
    return await service.create_item(
        session=session, current_user=current_user, category_id=category_id, item_data=item_data
    )


@oo_router.patch("/patch-item/{item_id}", tags=["Item"])
async def patch_item(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    item_id: int,
    item_data: ItemPatch,
) -> ItemRead:
    return await service.patch_item(session=session, current_user=current_user, item_id=item_id, item_data=item_data)


@oo_router.delete("/delete-item/{item_id}", tags=["Item"])
async def delete_item(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    item_id: int,
) -> dict:
    return await service.delete_item(session=session, current_user=current_user, item_id=item_id)


########################################################################################################################
@oo_router.get("/list-category/", tags=["Category"])
async def list_category(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
) -> list[CategoryRead]:
    return await service.list_category(session=session, current_user=current_user, offset=offset, limit=limit)


@oo_router.get("/get-category/{category_id}", tags=["Category"])
async def get_category(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    category_id: int,
) -> CategoryRead:
    return await service.get_category(session=session, current_user=current_user, category_id=category_id)


@oo_router.post("/create-category/", tags=["Category"])
async def create_category(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    category_data: CategoryCreate,
) -> CategoryRead:
    return await service.create_category(session=session, current_user=current_user, category_data=category_data)


@oo_router.patch("/patch-category/{category_id}", tags=["Category"])
async def patch_category(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    category_id: int,
    category_data: CategoryPatch,
) -> CategoryRead:
    return await service.patch_category(
        session=session, current_user=current_user, category_id=category_id, category_data=category_data
    )


@oo_router.delete("/delete-category/{category_id}", tags=["Category"])
async def delete_category(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[ItemServices, Depends(get_item_service)],
    category_id: int,
) -> dict:
    return await service.delete_category(session=session, current_user=current_user, category_id=category_id)
