import asyncio
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, EmailStr

# Инициализация FastAPI
app = FastAPI()

# Конфигурация базы данных
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:lovechaseolsen@localhost/users_db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для моделей SQLAlchemy
class Base(DeclarativeBase):
    pass

# Модель пользователя
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

# Pydantic-схема для создания пользователя
class UserCreate(BaseModel):
    username: str
    email: EmailStr

# Зависимость для получения сессии базы данных
async def get_db():
    async with SessionLocal() as session:
        yield session

# Эндпоинт для создания пользuvicorn app.main:app --reloadователя
@app.post("/users/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким же email
    result = await db.execute(select(UserModel).where(UserModel.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Создаем нового пользователя
    new_user = UserModel(username=user.username, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Обновляем объект для получения сгенерированного id

    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

# Функция для миграции базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Выполняем миграцию при запуске
@app.on_event("startup")
async def on_startup():
    await init_db()



