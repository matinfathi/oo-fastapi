from fastapi import HTTPException
from sqlmodel import select, delete
from sqlalchemy.orm import selectinload

from app.user.models import Role
from app.onlineordering.models import Menu, Location, Category, Item, Option, OptionGroup


class OptionServices:
    def __init__(self):
        pass

    async def list_option(self, session, current_user, option_group_id, offset, limit):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = select(Option).where(Option.option_group_fk == option_group_id).offset(offset).limit(limit)
        result = await session.exec(statement)

        return result.all()

    async def get_option(self, session, current_user, option_id):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = select(Option).where(Option.id == option_id)
        result = await session.exec(statement)

        return result.first()

    async def create_option(self, session, current_user, option_group_id, option_data):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        option_data_dump = option_data.model_dump()
        option_data_dump["option_group_fk"] = option_group_id

        db_data = Option(**option_data_dump)
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)

        return db_data

    async def patch_option(self, session, current_user, option_id, option_data):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = select(Option).where(Option.id == option_id)
        result = await session.exec(statement)
        db_option = result.first()

        if not result:
            raise HTTPException(status_code=404, detail="Option not found.")

        option_data_dump = option_data.model_dump(exclude_unset=True)

        for key, value in option_data_dump.items():
            setattr(db_option, key, value)

        session.add(db_option)
        await session.commit()
        await session.refresh(db_option)

        return db_option

    async def delete_option(self, session, current_user, option_id):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = delete(Option).where(Option.id == option_id)
        result = await session.exec(statement)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Option not found.")

        await session.commit()

        return {"message": "Option deleted successfully."}


class OptionGroupServices:
    def __init__(self):
        pass

    async def list_option_group(self, session, current_user, item_id, offset, limit):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = (
            select(OptionGroup)
            .where(OptionGroup.item_fk == item_id)
            .options(selectinload(OptionGroup.options))
            .offset(offset)
            .limit(limit)
        )
        result = await session.exec(statement)

        return result.all()

    async def get_option_group(self, session, current_user, option_group_id):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = (
            select(OptionGroup).where(OptionGroup.id == option_group_id).options(selectinload(OptionGroup.options))
        )
        result = await session.exec(statement)

        return result.first()

    async def create_option_group(self, session, current_user, item_id, option_group_data):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        option_group_data_dump = option_group_data.model_dump()
        option_group_data_dump["item_fk"] = item_id

        db_data = OptionGroup(**option_group_data_dump)
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)

        return db_data

    async def patch_option_group(self, session, current_user, option_group_id, option_group_data):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = select(OptionGroup).where(OptionGroup.id == option_group_id)
        result = await session.exec(statement)
        db_option_group = result.first()

        if not db_option_group:
            raise HTTPException(status_code=404, detail="Option Group not found.")

        option_group_data_dump = option_group_data.model_dump(exclude_unset=True)

        for key, value in option_group_data_dump.items():
            setattr(db_option_group, key, value)

        session.add(db_option_group)
        await session.commit()
        await session.refresh(db_option_group)

        return db_option_group

    async def delete_option_group(self, session, current_user, option_group_id):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = delete(OptionGroup).where(OptionGroup.id == option_group_id)
        result = await session.exec(statement)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Option Group not found.")

        await session.commit()

        return {"message": "Option Group deleted successfully."}


class ItemServices:
    def __init__(self):
        pass

    async def list_item(self, session, current_user, category_id, offset, limit):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = (
            select(Item)
            .where(Item.category_fk == category_id)
            .options(selectinload(Item.option_groups).selectinload(OptionGroup.options))
            .offset(offset)
            .limit(limit)
        )
        result = await session.exec(statement)

        return result.all()

    async def get_item(self, session, current_user, item_id):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = (
            select(Item)
            .where(Item.id == item_id)
            .options(selectinload(Item.option_groups).selectinload(OptionGroup.options))
        )
        result = await session.exec(statement)

        return result.first()

    async def create_item(self, session, current_user, category_id, item_data):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        item_data_dump = item_data.model_dump()
        item_data_dump["category_fk"] = category_id

        db_data = Item(**item_data_dump)
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)

        return db_data

    async def patch_item(self, session, current_user, item_id, item_data):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = select(Item).where(Item.id == item_id)
        result = await session.exec(statement)
        db_item = result.first()

        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found.")

        item_data_dump = item_data.model_dump(exclude_unset=True)

        for key, value in item_data_dump.items():
            setattr(db_item, key, value)

        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)

        return db_item

    async def delete_item(self, session, current_user, item_id):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = delete(Item).where(Item.id == item_id)
        result = await session.exec(statement)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found.")

        await session.commit()

        return {"message": "Item deleted successfully."}


class CategoryServices:
    def __init__(self):
        pass

    async def list_category(self, session, current_user, menu_id, offset, limit):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = (
            select(Category)
            .where(Category.menu_fk == menu_id)
            .options(selectinload(Category.items).selectinload(Item.option_groups).selectinload(OptionGroup.options))
            .offset(offset)
            .limit(limit)
        )
        result = await session.exec(statement)

        return result.all()

    async def get_category(self, session, current_user, category_id):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = (
            select(Category)
            .where(Category.id == category_id)
            .options(selectinload(Category.items).selectinload(Item.option_groups).selectinload(OptionGroup.options))
        )
        result = await session.exec(statement)

        return result.first()

    async def create_category(self, session, current_user, menu_id, category_data):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        category_data_dump = category_data.model_dump()
        category_data_dump["menu_fk"] = menu_id

        db_data = Category(**category_data_dump)
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)

        return db_data

    async def patch_category(self, session, current_user, category_id, category_data):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = select(Category).where(Category.id == category_id)
        result = await session.exec(statement)
        db_category = result.first()

        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found.")

        category_data_dump = category_data.model_dump(exclude_unset=True)

        for key, value in category_data_dump.items():
            setattr(db_category, key, value)

        session.add(db_category)
        await session.commit()
        await session.refresh(db_category)

        return db_category

    async def delete_category(self, session, current_user, category_id):
        if current_user.role == Role.Customer:
            raise HTTPException(status_code=403, detail="Not enough permission.")

        statement = delete(Category).where(Category.id == category_id)
        result = await session.exec(statement)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Category not found.")

        await session.commit()

        return {"message": "Category deleted successfully."}
