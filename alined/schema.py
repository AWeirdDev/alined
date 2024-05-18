from __future__ import annotations

from typing import List, Literal, Union
from pydantic import BaseModel, Field


class Emoji(BaseModel):
    index: int
    length: int
    product_id: str = Field(..., alias="productId")
    emoji_id: str = Field(..., alias="emojiId")


class Mentions(BaseModel):
    mentionees: List[Union[MentioneeUser, MentioneeAll]]


class MentioneeAll(BaseModel):
    type: Literal["all"]
    index: int
    length: int


class MentioneeUser(BaseModel):
    type: Literal["user"]
    index: int
    length: int
    user_id: str = Field(..., alias="userId")
