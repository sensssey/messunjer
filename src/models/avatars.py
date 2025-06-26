from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.database import Base


class AvatarDB(Base):
    __tablename__ = "avatars"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    file_data = Column(Text)

    user = relationship("UserDB", back_populates="avatar")
