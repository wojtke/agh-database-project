from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class Interaction(BaseModel):
    _id = Field(None, alias="_id")
    user_id: int
    article_id: int

    interaction_type: str

    date: datetime = datetime.utcnow()


class InteractionBucket(BaseModel):
    n_interactions: int
    interactions: List[Interaction] = []

    date_start: Optional[datetime] = None
    date_end: datetime = datetime.utcnow()

