from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.auth.auth import get_current_user
from src.posts.crud import create_post, get_posts_by_user, create_parameter
from src.schemas.post_schemas import PostCreate, ParameterCreate, Post, Parameter

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

@post_router.post("/", response_model=Post)
async def create_new_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await create_post(db, user_id=current_user.id, post_data=post_data)

@post_router.get("/", response_model=list[Post])
async def get_user_posts(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await get_posts_by_user(db, user_id=current_user.id)

@post_router.post("/parameters/", response_model=Parameter)
async def create_new_parameter(
    parameter_data: ParameterCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await create_parameter(db, user_id=current_user.id, parameter_data=parameter_data)