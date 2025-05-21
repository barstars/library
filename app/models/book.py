from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer
from pydantic import BaseModel
import uuid
from typing import Optional

# DATA BASE MODELS
class BookBase(Base):
    __tablename__ = "book"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    isbn: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    copies: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    async def copies_add(self):
        self.copies += 1

    async def copies_reduce(self):
        self.copies -= 1

#########################

# pydantic.BaseModel MODELS
class BookRegisterDatas(BaseModel):
    name: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: Optional[int] = 1

class BookDB_for_pydantic(BaseModel):
    id: uuid.UUID
    name: str
    author: str
    year: Optional[int]
    isbn: Optional[str]
    copies: int

    class Config:
        from_attributes=True


#########################