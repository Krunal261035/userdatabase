from pydantic import BaseModel,EmailStr,field_validator,StringConstraints
from datetime import datetime
from typing import Optional
from typing import Annotated
OnlyAlphabets = Annotated[str, StringConstraints(pattern='^[A-Za-z]+$')]
class UserSchema(BaseModel):
    username: str
    email:str
    password_hash:str
    full_name: OnlyAlphabets
    is_active: bool = True
    role: str

    @field_validator('password_hash')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain a lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain a number")
        if not any(c in '!@#$%^&*()-_=+[{]};:\'",<.>/?`~' for c in value):
            raise ValueError("Password must contain a special character")
        return value

class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None



class AddressSchema(BaseModel):
    address_line1 : str
    address_line2 : str
    city : str
    state : str
    country : str
    postal_code : str
    phone_number : str
    is_default : bool

class AddressSchemaDisplay(BaseModel):
    address_line1 : str
    address_line2 : str
    city : str
    state : str
    country : str
    postal_code : str
    phone_number : str
    is_default : bool


class AddToCartSchema(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    price: float
    total: float

class UpdateCartItemSchema(BaseModel):
    cart_item_id: int
    quantity: int