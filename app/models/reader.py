from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Column
from pydantic import BaseModel

# DATA BASE MODELS
class ReaderBase(Base):
	"""
	Database model for reader
	"""
    __tablename__ = "reader"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)

#########################


# pydantic.BaseModel MODELS
class ReaderRegisterDatas(BaseModel):
	"""
	Reader registration data
	"""
	password: str
	email: str
	username: str

class ReaderLoginDatas(BaseModel):
	"""
	Reader login data
	"""
	password: str
	email: str

#########################