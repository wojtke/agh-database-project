from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

from .objectid import PydanticObjectId


class Quantity(BaseModel):
    quantity: Optional[Union[str, int, float]]
    unit: Optional[str]


class Ingredient(BaseModel):
    name: str
    quantity: Optional[Quantity]


class Cocktail(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    slug: str
    name: str
    ingredients: List[Ingredient]
    instructions: List[str]
    date_added: Optional[datetime]
    date_updated: Optional[datetime]

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data






