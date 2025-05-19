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
    name: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    year: Mapped[str] = mapped_column(String)
    isbn: Mapped[Optional[str]] = mapped_column(String, unique=True)
    instances: Mapped[int] = mapped_column(Integer, default=1)

#########################


# pydantic.BaseModel MODELS
class BookRegister(BaseModel):
	password: str
	email: str
	username: str