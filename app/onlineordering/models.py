from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Column, Relationship, Enum as sqlEnum

if TYPE_CHECKING:
    from app.user.models import OoUserModel


CURRENCY_SIGNS = {
    "USD": "$",
    "CAD": "$",
    "EUR": "€",
    "GBP": "£",
}


class Currency(str, Enum):
    USD = "USD"
    CAD = "CAD"
    EUR = "EUR"
    GBP = "GBP"


class Menu(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    description: str | None = None
    price_unit: Currency = Field(sa_column=Column(sqlEnum(Currency, name="currency_enum")))

    locations: list["Location"] = Relationship(back_populates="menu")
    categories: list["Category"] = Relationship(back_populates="menu")

    @property
    def currency_sign(self):
        return CURRENCY_SIGNS.get(self.price_unit.value, None)


class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    latitude: float
    longitude: float
    name: str
    address: str
    working_hours: str | None = None
    is_active: bool = True

    user_fk: int | None = Field(foreign_key="user.id")
    menu_fk: int | None = Field(default=None, foreign_key="menu.id")

    menu: "Menu" = Relationship(back_populates="locations")
    user: "OoUserModel" = Relationship(back_populates="locations")



class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    menu_fk: int = Field(foreign_key="menu.id")

    menu: "Menu" = Relationship(back_populates="categories")
    items: list["Item"] = Relationship(back_populates="category")


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    description: str | None = None
    image: str | None = None
    price: float
    is_available: bool = True

    category_fk: int = Field(foreign_key="category.id")

    category: "Category" = Relationship(back_populates="items")
    option_groups: list["OptionGroup"] = Relationship(back_populates="item")


class OptionGroup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    allow_multiple: bool = False
    is_required: bool = False

    item_fk: int = Field(foreign_key="item.id")

    item: "Item" = Relationship(back_populates="option_groups")
    options: list["Option"] = Relationship(back_populates="option_group")


class Option(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    price: float = 0.0

    option_group_fk: int = Field(foreign_key="optiongroup.id")

    option_group: "OptionGroup" = Relationship(back_populates="options")
