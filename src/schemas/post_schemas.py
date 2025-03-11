from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

# Базовая модель для параметров
class ParameterBase(BaseModel):
    name: str
    description: Optional[str] = None

# Модель для создания параметра
class ParameterCreate(ParameterBase):
    pass

# Модель для чтения параметра
class Parameter(ParameterBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Замена orm_mode

# Базовая модель для поста
class PostBase(BaseModel):
    title: str
    content: str

# Модель для создания поста
class PostCreate(PostBase):
    parameters: List[Dict[str, str]] = []  # Список параметров

# Модель для чтения поста
class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Замена orm_mode

# Базовая модель для связи пост-параметр
class PostParameterBase(BaseModel):
    parameter_id: int
    value: float

# Модель для создания связи пост-параметр
class PostParameterCreate(PostParameterBase):
    pass