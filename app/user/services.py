from fastapi import HTTPException
from sqlmodel import select

from app.user.models import OoUserModel as User


class UserServices:
    def __init__(self):
        pass

    async def list_users(*, current_user, session):
        if current_user.role != "SuperAdmin":
            raise HTTPException(status_code=403, detail="Not enough permission.")

        result = await session.exec(select(User))
        return result.all()

    async def get_user(*, current_user, session, **kwargs):
        pass