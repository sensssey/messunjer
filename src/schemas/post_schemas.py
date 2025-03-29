from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass  # Все поля необязательные благодаря PostBase

class Post(PostBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True
