from fastapi import HTTPException
from sqlmodel import select

from app.user.models import Role, OoUserModel as User
from app.core.security import get_password_hash


class UserServices:
    def __init__(self):
        pass

    async def list_users(self, current_user, session):
        print(current_user.role)
        if current_user.role != Role.SuperAdmin:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        result = await session.exec(select(User))
        return result.all()

    async def get_user(self, current_user, session, **kwargs):
        if current_user.role != Role.SuperAdmin:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        if kwargs["user_id"] is not None:
            result = await session.exec(select(User).where(User.id == kwargs["user_id"]))
        elif kwargs["username"] is not None:
            result = await session.exec(select(User).where(User.username == kwargs["username"]))
        elif kwargs["email"] is not None:
            result = await session.exec(select(User).where(User.email == kwargs["email"]))
        else:
            raise HTTPException(status_code=400, detail="Provide information.")

        return result.first()

    async def create_user(self, session, **kwargs):
        user_json = kwargs["user_data"].model_dump()
        user_json["hashed_password"] = get_password_hash(user_json.pop("password"))
        user_json["role"] = "Customer"

        db_user = User(**user_json)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    async def create_user_by_admin(self, current_user, session, **kwargs):
        if current_user.role != Role.SuperAdmin:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        user_json = kwargs["user_data"].model_dump()
        user_json["hashed_password"] = get_password_hash(user_json.pop("password"))

        db_user = User(**user_json)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    async def update_user(self, current_user, session, **kwargs):
        if current_user.role != Role.SuperAdmin and current_user.id != kwargs["user_id"]:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        db_user = await session.exec(select(User).where(User.id == kwargs["user_id"]))
        if not db_user:
            HTTPException(status_code=404, detail="User not found.")

        user_data = kwargs["user_data"].model_dump()
        for key, value in user_data.items():
            setattr(db_user, key, value)

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    async def delete_user(self, current_user, session, **kwargs):
        if current_user.role != Role.SuperAdmin and current_user.id != kwargs["user_id"]:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        db_user = await session.exec(select(User).where(User.id == kwargs["user_id"]))
        if not db_user:
            HTTPException(status_code=404, detail="User not found.")

        session.delete(db_user)
        await session.commit()

        return {"message": "User deleted successfully."}
