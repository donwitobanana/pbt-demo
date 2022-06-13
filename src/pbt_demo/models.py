from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    description: str


class ItemUpdate(BaseModel):
    description: Optional[str] = None


class Message(BaseModel):
    message: str
