from typing import Union

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5


class Test(BaseModel):
    name: Union[str, None]
    age: int
