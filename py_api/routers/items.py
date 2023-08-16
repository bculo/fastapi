from typing import Annotated, Union

from fastapi import Path, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from domain.exceptions import NotFoundException
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


class Item(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = Field(default=10.5)
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@router.patch("/{item_id}", response_model=Item)
async def update_item(item_id: Annotated[str, Path()],
                      item: Annotated[Item, Body()]):
    stored_item_data = items.get(item_id)
    if stored_item_data is None:
        raise NotFoundException("Item not found")

    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

