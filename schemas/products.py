from pydantic import BaseModel
from enum import Enum
from typing import List
class SizeEnum(str, Enum):
    M = "M"
    L = "L"
    XL = "XL"
class ProductCategory(BaseModel):
    name:str
    description:str

class ProductSchema(BaseModel):
    product_name :str
    price :str
    size :SizeEnum
    image :List[str]
    stock : int
    description :str
    category_id :int

class UserResponseSchema(BaseModel):
    username: str
    email:str
    full_name: str
    is_active: bool = True
    role: str

    class Config:
        from_attributes = True

class CartSchema(BaseModel):
    user_id : int

class OrderFromCartRequest(BaseModel):
    product_id: int
    quantity: int