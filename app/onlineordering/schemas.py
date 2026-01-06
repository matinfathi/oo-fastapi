from pydantic import BaseModel



class OptionRead(BaseModel):
    id: int
    name: str
    price: float
    option_group_fk: int


class OptionCreate(BaseModel):
    name: str
    price: float


class OptionPatch(BaseModel):
    name: str | None = None
    price: float | None = None
    option_group_fk: int | None = None


########################################################################################################################
class OptionGroupRead(BaseModel):
    id: int
    allow_multiple: bool
    is_required: bool
    options: list[OptionRead] = []


class OptionGroupCreate(BaseModel):
    allow_multiple: bool
    is_required: bool


class OptionGroupPatch(BaseModel):
    allow_multiple: bool | None = None
    is_required: bool | None = None
    item_fk: int | None = None


########################################################################################################################
class ItemRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    image: str | None = None
    price: float
    is_available: bool
    option_groups: list[OptionGroupRead] = []


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    image: str | None = None
    price: float
    is_available: bool = True


class ItemPatch(BaseModel):
    name: str | None = None
    description: str | None = None
    image: str | None = None
    price: float | None = None
    is_available: bool | None = None
    category_fk: int | None = None


########################################################################################################################
class CategoryRead(BaseModel):
    id: int
    name: str
    items: list[ItemRead] = []


class CategoryCreate(BaseModel):
    name: str


class CategoryPatch(BaseModel):
    name: str | None = None
    menu_fk: int | None = None


########################################################################################################################
