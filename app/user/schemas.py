from pydantic import BaseModel

from app.user.models import Role


class UserRead(BaseModel):
    id: int
    name: str | None = None
    last_name: str | None = None
    username: str
    phone_number: str | None = None
    email: str
    role: Role
    # locations: list[LocationRead] = []


class UserCreate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    username: str
    phone_number: str | None = None
    email: str
    password: str


class UserCreateByAdmin(BaseModel):
    name: str | None = None
    last_name: str | None = None
    username: str
    phone_number: str | None = None
    email: str
    password: str
    role: Role


class UserUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    username: str | None = None
    phone_number: str | None = None
    email: str | None = None
    password: str | None = None
    role: Role | None = None
