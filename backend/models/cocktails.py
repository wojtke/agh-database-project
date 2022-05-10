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


class Article(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias = "_id")
    article_id: int
    title: str
    tags: List[str]
    category: str
    content: str
    image_source: str
    n_of_grades: int
    sum_of_grades: int
    n_of_views: int
    date_added: Optional[str]


    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


class Rating(BaseModel):
    article_id: int
    grade: int


class View(BaseModel):
    article_id: int
    n_view: int


class User(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias = "_id")
    user_id: int
    name: str
    login: str
    ratings: List[Rating]
    views: List[View]

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


class Comment(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias = "_id")
    comment_id: int
    user_id: int
    article_id: int
    content: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data
