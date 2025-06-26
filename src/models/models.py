from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    avatar = relationship("AvatarDB", back_populates="user", uselist=False, lazy="selectin")
