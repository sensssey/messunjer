from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.post_models import Post, Parameter, PostParameter
from src.schemas.post_schemas import PostCreate, ParameterCreate

async def create_post(db: AsyncSession, user_id: int, post_data: PostCreate):
    new_post = Post(user_id=user_id, title=post_data.title, content=post_data.content)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    for param in post_data.parameters:
        parameter_id = param["parameter_id"]
        value = param["value"]
        post_parameter = PostParameter(post_id=new_post.id, parameter_id=parameter_id, value=value)
        db.add(post_parameter)
    await db.commit()

    return new_post

async def get_posts_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Post).where(Post.user_id == user_id))
    return result.scalars().all()

async def create_parameter(db: AsyncSession, user_id: int, parameter_data: ParameterCreate):
    new_parameter = Parameter(user_id=user_id, **parameter_data.dict())
    db.add(new_parameter)
    await db.commit()
    await db.refresh(new_parameter)
    return new_parameter