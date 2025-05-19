from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Column
from pydantic import BaseModel

from app.services.password_hashing import verify_password, hash_password

# DATA BASE MODELS
class AdminBase(Base):
    __tablename__ = "admin"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)

    
    def password_add(self, plain_password: str):
    	self.password_hash = hash_password(plain_password)

    def verify_password(self, plain_password: str) -> bool:
    	return verify_password(plain_password, self.password_hash)

#########################


# pydantic.BaseModel MODELS
class AdminRegisterDatas(BaseModel):
	password: str
	email: str
	username: str

class AdminLoginDatas(BaseModel):
	password: str
	email: str

#########################