# posts/routes.py
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.auth.auth import get_current_user
from src.schemas.post_schemas import PostCreate, PostUpdate, Post
from src.posts.crud import create_post, get_post_by_id, get_posts_by_user, update_post, delete_post

posts_router = APIRouter(prefix="/posts", tags=["Posts"])

@posts_router.post("/", response_model=Post)
async def create_new_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await create_post(db, post_data=post_data, user_id=current_user.id)

@posts_router.get("/{post_id}", response_model=Post)
async def read_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@posts_router.get("/", response_model=list[Post])
async def read_user_posts(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await get_posts_by_user(db, user_id=current_user.id)

@posts_router.put("/{post_id}", response_model=Post)
async def update_existing_post(
    post_id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    elif post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")  # Исправьте статус код
    updated_post = await update_post(db, post_id=post_id, post_data=post_data)
    return updated_post

@posts_router.delete("/{post_id}")
async def delete_existing_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    post = await get_post_by_id(db, post_id)
    if not post:  # Проверяем существование поста
        raise HTTPException(status_code=404, detail="Post not found")
    elif post.user_id != current_user.id:  # Проверяем права пользователя
        raise HTTPException(status_code=403, detail="Unauthorized")
    await delete_post(db, post_id=post_id)
    return {"detail": "Post deleted"}