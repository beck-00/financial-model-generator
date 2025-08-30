from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# Base User Schema
class UserBase(BaseModel):
        email: EmailStr

# Schema for User Creation
class UserCreate(UserBase):
        password: str

# Schema for User Response
class User(UserBase):
        id: int
        is_active: bool
        created_at: datetime
        updated_at: Optional[datetime] = None

        model_config = ConfigDict(from_attributes=True)

# Schema for Token Response
class Token(BaseModel):
        access_token: str
        refresh_token: str
        token_type: str = "bearer"

# Schema for Token Response
class Token(BaseModel):
        access_token: str
        refresh_token: str
        token_type: str = "bearer"

# Schema for Token Refresh
class TokenRefresh(BaseModel):
        refresh_token: str

# Schema for Login
class UserLogin(BaseModel):
        email: EmailStr
        password: str