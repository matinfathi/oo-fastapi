from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship, Column, Enum as sqlEnum

if TYPE_CHECKING:
    from app.onlineordering.models import Location


class Role(str, Enum):
    Customer = "Customer"
    Owner = "Owner"
    SuperAdmin = "SuperAdmin"


class OoUserModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str | None = None
    last_name: str | None = None
    username: str
    phone_number: str | None = None
    email: str

    role: Role = Field(sa_column=Column(sqlEnum(Role, "role_enum")))

    locations: list["Location"] = Relationship(back_populates="user")
