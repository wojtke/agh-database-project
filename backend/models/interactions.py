from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Optional

from .. import interactions

BUCKET_SIZE = timedelta(days=1)


class Interaction(BaseModel):
    _id = Field(None, alias="_id")
    user_id: int
    article_id: int

    interaction_type: str

    date: datetime = datetime.utcnow()

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


class InteractionBucket(BaseModel):
    _id = Field(None, alias="_id")
    n_interactions: int = 0
    interactions: List[Interaction] = []

    date_start: Optional[datetime] = datetime.utcnow()\
        .replace(hour=0, minute=0, second=0, microsecond=0)
    date_end: Optional[datetime] = date_start + BUCKET_SIZE

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


def add_interaction(user_id: int, article_id: int, type: str):
    """Add an interaction to the database."""
    if not user_id or not article_id:
        return

    interaction = Interaction(
        user_id=user_id,
        article_id=article_id,
        interaction_type=type,
    )
    last_bucket = interactions.find_one({}, sort=[("date_end", -1)])
    if last_bucket is None or last_bucket["date_end"] < interaction.date:
        last_bucket = InteractionBucket().to_bson()
        interactions.insert_one(last_bucket)

    id = last_bucket["_id"]
    interactions.find_one_and_update(
        {"_id": id},
        {
            "$addToSet": {
                "interactions": interaction.to_bson()
            },
            "$inc": {"n_interactions": 1}
        }
    )
