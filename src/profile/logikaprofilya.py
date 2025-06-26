from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import io
from starlette.responses import StreamingResponse

from src.database import get_db
from src.models.models import UserDB
from src.models.avatars import AvatarDB
from src.auth.auth import get_current_user

pr_router = APIRouter(prefix="/users", tags=["users"])

@pr_router.post("/avatar", status_code=status.HTTP_201_CREATED)
async def upload_avatar(
        file: UploadFile = File(...),
        current_user: UserDB = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, detail="Only JPEG/PNG allowed")
    try:
        contents = await file.read()
        file_data_str = contents.decode('latin1').encode('unicode-escape').decode('ascii')
        avatar = await db.execute(
            select(AvatarDB).where(AvatarDB.user_id == current_user.id)
        )
        avatar = avatar.scalar_one_or_none()
        if avatar:
            avatar.file_data = file_data_str
        else:
            avatar = AvatarDB(user_id=current_user.id, file_data=file_data_str)
            db.add(avatar)
        await db.commit()
        return {"message": "Avatar uploaded successfully"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@pr_router.get("/avatar/{user_id}")
async def get_avatar(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    user = await db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    avatar = await db.execute(
        select(AvatarDB).where(AvatarDB.user_id == user_id)
    )
    avatar = avatar.scalar_one_or_none()

    if not avatar or not avatar.file_data:
        raise HTTPException(status_code=404, detail="Avatar not found")

    try:
        binary_data = avatar.file_data.encode('ascii').decode('unicode-escape').encode('latin1')
        if binary_data.startswith(b'\xff\xd8'):
            media_type = "image/jpeg"
        elif binary_data.startswith(b'\x89PNG'):
            media_type = "image/png"
        else:
            media_type = "application/octet-stream"
        return StreamingResponse(
            io.BytesIO(binary_data),
            media_type=media_type,
            headers={"Content-Disposition": f"inline; filename=avatar_{user_id}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process avatar: {str(e)}"
        )


@pr_router.delete("/avatar", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avatar(
        current_user: UserDB = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    avatar = await db.execute(
        select(AvatarDB).where(AvatarDB.user_id == current_user.id)
    )
    avatar = avatar.scalar_one_or_none()
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )
    await db.delete(avatar)
    await db.commit()
    return None