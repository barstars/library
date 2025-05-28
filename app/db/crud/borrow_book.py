from app.models.borrow_book import BorrowedBookBase, BorrowNewBook

from sqlalchemy import select, delete

from typing import AsyncGenerator
from uuid import UUID

class DataBaseManager:
	def __init__(self, db: AsyncGenerator):
		"""
		Borrowed book database manager
		
		db -- Session from the database
		"""
		self.db = db

	async def create(self, BNBook: BorrowNewBook):
		"""
		Create new data

		BNBook -- Registration data
		"""
		BBBase = BorrowedBookBase(**BNBook.model_dump())

		self.db.add(BBBase)
		await self.db.commit()
		return BBBase.id

	async def get_reader_all_books(self, reader_id: str) -> list:
		"""
		Get all borrows for reader

		reader_id -- Id from reader
		"""
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.reader_id == UUID(reader_id)))
		return result.scalars().all()

	async def get_reader_active_books(self, reader_id: str) -> list:
		"""
		Get all active borrows for reader

		reader_id -- Id from reader
		"""
		result = await self.db.execute(select(BorrowedBookBase).where(
			(BorrowedBookBase.reader_id == UUID(reader_id)) &
			(BorrowedBookBase.return_date == None)))
		return result.scalars().all()

	async def is_reader_borrowed_this_book(self, reader_id: str, book_id: str) -> bool:
		"""
		He finds out if the reader has taken this book.

		reader_id -- Id from reader
		book_id -- Id from book
		"""
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
		"""
		Return book

		id_ -- Id from borrow
		"""
		curr = await self.get_by_id(id_)
		await curr.return_data_update()
		await self.db.commit()

	async def get_info(self, id_: str):
		"""
		Get info from borrow

		id_ -- Id from borrow
		"""
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.id == UUID(id_)))
		curr = result.scalars().first()
		info = await curr.get_info()
		return info

	async def get_all_borrow_by_book(self, book_id: str):
		"""
		Get all books data from borrow

		book_id -- Id from book
		"""
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.book_id == UUID(book_id)))
		return result.scalars().all()

	async def delete_by_all_book(self, book_id: str):
		"""
		Delete all books data from borrow

		book_id -- Id from book
		"""
		borrows = await self.db.execute(delete(BorrowedBookBase).where(BorrowedBookBase.book_id == UUID(book_id)))
		await self.db.commit()

	async def get_by_id(self, id_: str):
		"""
		Search by id

		id_ -- Id from borrow
		"""
		result = await self.db.execute(select(BorrowedBookBase).where(BorrowedBookBase.id == UUID(id_)))
		curr = result.scalars().first()
		return curr