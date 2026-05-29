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
    
    model_config = ConfigDict(from_attributes=True)
    
class UserBase(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(UserBase):
    pass
    
