from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum



class UserRole(str, Enum):
    admin = "admin"
    viewer = "viewer"

class User(BaseModel):
    username: str
    role: UserRole


# Status Enum
class ItemStatus(str, Enum):
    in_stock = "in_stock"
    low_stock = "low_stock"
    ordered = "ordered"
    discontinued = "discontinued"


class ItemBase(BaseModel):
    name: str
    quantity: int
    category: str
    status: ItemStatus
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    status: Optional[ItemStatus] = None
    description: Optional[str] = None


class Item(ItemBase):
    id: UUID
