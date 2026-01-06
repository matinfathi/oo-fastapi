from enum import Enum

from sqlmodel import SQLModel, Field, Relationship, Column, Enum as sqlEnum

from app.onlineordering.models import Location


class Role(str, Enum):
    Customer = "Customer"
    Owner = "Owner"
    SuperAdmin = "SuperAdmin"


class OoUserModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str | None = None
    last_name: str | None = None
    username: str = Field(index=True, unique=True)
    phone_number: str | None = None
    email: str = Field(index=True, unique=True)
    hashed_password: str
    image: str | None = None

    role: Role = Field(sa_column=Column(sqlEnum(Role, name="role_enum")))

    locations: list[Location] = Relationship(back_populates="user")
