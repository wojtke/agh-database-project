from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional

from .objectid import PydanticObjectId


class Article(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
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
