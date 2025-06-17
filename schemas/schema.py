from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
class UserSchema(BaseModel):
    username: str
    email:str
    password_hash:str
    full_name: str
    is_active: bool = True
    role: str

class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class AddressSchema(BaseModel):
    address_line1 : str
    address_line2 : str
    city : str
    state : str
    country : str
    postal_code : str
    phone_number : str
    is_default : bool

class AddressResponseSchema(BaseModel):
    address_line1 : str
    address_line2 : str
    city : str
    state : str
    country : str
    postal_code : str
    phone_number : str
    is_default : bool