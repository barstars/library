from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON

# DATA BASE MODELS
class BorrowUserBase(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    jwt_ids: Mapped[dict] = mapped_column(JSON)

#########################