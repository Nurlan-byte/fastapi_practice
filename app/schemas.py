from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 
    
class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at: datetime
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str    

class TokenData(BaseModel):
    id: int | None