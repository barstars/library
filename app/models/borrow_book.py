from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, ForeignKey
from pydantic import BaseModel

import datetime
import uuid

# DATA BASE MODELS
class BorrowedBookBase(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reader_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reader.id"))
    book_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("book.id"))
    borrow_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    return_date: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    async def return_data_update(self):
    	self.return_date = datetime.datetime.utcnow()

    async def get_info(self):
        if self.return_date:
            return {"id":self.id,
                "borrow_date":str(self.borrow_date),
                "return_date":str(self.return_date)}
        else:
            return {"id":self.id,
                "borrow_date":str(self.borrow_date),
                "return_date":self.return_date}

#########################

# pydantic.BaseModel MODELS

class BorrowedBookDatas(BaseModel):
	id: str

class BorrowNewBook(BaseModel):
	reader_id: uuid.UUID
	book_id: uuid.UUID

class ReturnBookDatas(BaseModel):
    id: str

#########################