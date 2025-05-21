from app.models.borrow_book import BorrowedBookBase, BorrowNewBook

from sqlalchemy import select

from typing import AsyncGenerator
from uuid import UUID

class DataBaseManager:
	def __init__(self, db: AsyncGenerator):
		self.db = db

	async def create(self, BNBook: BorrowNewBook):
		BBBase = BorrowedBookBase(**BNBook.model_dump())

		self.db.add(BBBase)
		await self.db.commit()
		return BBBase.id

	async def get_reader_all_books(self, reader_id: str):
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.reader_id == UUID(reader_id)))
		return result.scalars().all()

	async def get_reader_active_books(self, reader_id: str):
		result = await self.db.execute(select(BorrowedBookBase).where((BorrowedBookBase.reader_id == UUID(reader_id) and (BorrowedBookBase.return_date != None))))
		return result.scalars().all()

	async def get_by_id(self, id_: str):
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.id == UUID(id_)))
		curr = result.scalars().first()
		return curr