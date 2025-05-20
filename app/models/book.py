from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer
from pydantic import BaseModel
import uuid
from typing import Optional

# DATA BASE MODELS
class BookBase(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[Optional[str]] = mapped_column(String nullable=True)
    isbn: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    copies: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

#########################

# pydantic.BaseModel MODELS
class BookRegister(BaseModel):
	name: str
	author: str
	year: Optional[str] = None
    isbn: Optional[str] = None
    copies: Optional[int] = None