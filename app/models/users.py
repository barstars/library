from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
from pydantic import BaseModel

# DATA BASE MODELS
class UserBase(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String)

#########################


# pydantic.BaseModel MODELS
class UserRegister(BaseModel):
	password: str
	email: str
	username: str

#########################

# INSERT INTO users (id,ip_address,useragent,is_admin,password,email,username) VALUES (gen_random_uuid(),'127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64)',TRUE,'hashed_password_here','newadmin@example.com','superadmin');