from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.post_models import Post
from src.schemas.post_schemas import PostUpdate, PostCreate


async def create_post(db: AsyncSession, post_data: PostCreate, user_id: int):
    new_post = Post(
        user_id=user_id,
        title=post_data.title,
        content=post_data.content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


async def get_post_by_id(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalars().first()

async def get_posts_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Post).where(Post.user_id == user_id))
    return result.scalars().all()

async def update_post(db: AsyncSession, post_id: int, post_data: PostUpdate):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()

    if not post:
        return None

    # Обновляем поля
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content

    post.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(post)
    return post

async def delete_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()

    if not post: 
        return None

    await db.delete(post)
    await db.commit()
    return post