from app.models.borrow_book import BorrowedBookBase, BorrowNewBook

from sqlalchemy import select, delete

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

	async def get_reader_all_books(self, reader_id: str) -> list:
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.reader_id == UUID(reader_id)))
		return result.scalars().all()

	async def get_reader_active_books(self, reader_id: str) -> list:
		result = await self.db.execute(select(BorrowedBookBase).where(
			(BorrowedBookBase.reader_id == UUID(reader_id)) &
			(BorrowedBookBase.return_date == None)))
		return result.scalars().all()

	async def is_reader_borrowed_this_book(self, reader_id: str, book_id: str) -> bool:
		result = await self.db.execute(select(BorrowedBookBase).where(
			(BorrowedBookBase.reader_id == UUID(reader_id)) &
			(BorrowedBookBase.book_id == UUID(book_id))
		))
		curr = result.scalars().first()
		if curr:
			return True
		else:
			return False

	async def return_book(self, id_: str):
		curr = await self.get_by_id(id_)
		await curr.return_data_update()
		await self.db.commit()

	async def get_info(self, id_: str):
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.id == UUID(id_)))
		curr = result.scalars().first()
		info = await curr.get_info()
		return info

	async def get_all_borrow_by_book(self, book_id: str):
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.book_id == UUID(book_id)))
		return result.scalars().all()

	async def delete_by_all_book(self, book_id: str):
		borrows = await self.db.execute(delete(BorrowedBookBase).where(BorrowedBookBase.book_id == UUID(book_id)))
		await self.db.commit()

	async def get_by_id(self, id_: str):
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.id == UUID(id_)))
		curr = result.scalars().first()
		return curr