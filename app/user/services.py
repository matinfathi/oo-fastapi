from fastapi import HTTPException
from sqlmodel import select, delete

from app.user.models import Role, OoUserModel as User
from app.core.security import get_password_hash


class UserServices:
    def __init__(self):
        pass

    async def list_users(self, current_user, session, offset, limit):
        print(current_user.role)
        if current_user.role != Role.SuperAdmin:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = select(User).offset(offset).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def get_user(self, current_user, session, user_id, username, email):
        if current_user.role != Role.SuperAdmin:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        if user_id is not None:
            result = await session.exec(select(User).where(User.id == user_id))
        elif username is not None:
            result = await session.exec(select(User).where(User.username == username))
        elif email is not None:
            result = await session.exec(select(User).where(User.email == email))
        else:
            raise HTTPException(status_code=400, detail="Provide information.")

        return result.first()

    async def create_user(self, session, user_data):
        user_json = user_data.model_dump()
        user_json["hashed_password"] = get_password_hash(user_json.pop("password"))
        user_json["role"] = "Customer"

        db_user = User(**user_json)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    async def create_user_by_admin(self, current_user, session, user_data):
        if current_user.role != Role.SuperAdmin:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        user_json = user_data.model_dump()
        user_json["hashed_password"] = get_password_hash(user_json.pop("password"))

        db_user = User(**user_json)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    async def update_user(self, current_user, session, user_id, user_data):
        if current_user.role != Role.SuperAdmin and current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        result = await session.exec(select(User).where(User.id == user_id))
        db_user = result.first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found.")

        user_data = user_data.model_dump(exclude_unset=True)
        if "password" in user_data.keys():
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

        for key, value in user_data.items():
            setattr(db_user, key, value)

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    async def delete_user(self, current_user, session, user_id):
        if current_user.role != Role.SuperAdmin and current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = delete(User).where(User.id == user_id)
        result = await session.exec(statement)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found.")

        await session.commit()

        return {"message": "User deleted successfully."}
