from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, Text
from pydantic import BaseModel
import uuid
from typing import Optional

# DATA BASE MODELS
class BookBase(Base):
    """
    Database model for book
    """
    __tablename__ = "book"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    isbn: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    copies: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    async def copies_add(self, copies: int):
        """
        Add copies for book

        copies -- Number of copies to add
        """
        self.copies += copies

    async def copies_reduce(self):
        """
        Reduce copies
        """
        self.copies -= 1

    async def get_info(self):
        """
        Get info from book
        """
        return {"name":self.name,
                "author":self.author,
                "year":self.year}

#########################

# pydantic.BaseModel MODELS
class BookRegisterDatas(BaseModel):
    """
    Book registration data
    """
    name: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: Optional[int] = 1
    description: Optional[str] = None

class AddCopiesDatas(BaseModel):
    """
    Datas for add copies book
    """
    id: str
    copies: int

class DeleteBookDatas(BaseModel):
    """
    Datas for aelete book
    """
    id: str

class BookOUT(BaseModel):
    """
    Pydantic for database book"""
    id: uuid.UUID
    name: str
    author: str
    year: Optional[int]
    isbn: Optional[str]
    copies: int

    class Config:
        from_attributes=True

#########################