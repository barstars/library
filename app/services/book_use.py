from app.models.borrow_book import BorrowNewBook
from app.models.book import BookBase
from app.models.reader import ReaderBase
from app.db.crud.borrow_book import DataBaseManager as BorrowBookDBM
from app.db.crud.book import DataBaseManager as BookDBM

from uuid import UUID
from typing import AsyncGenerator


class NewBorrowedBook:
	def __init__(self, db: AsyncGenerator):
		self.db = db
		self.borrow_book_dbm = BorrowBookDBM(self.db)

	async def new_borrow(self, book_base: BookBase, reader_base: ReaderBase):
		book_id = str(book_base.id)
		reader_id = str(reader_base.id)
		active_books_count = len(await self.borrow_book_dbm.get_reader_active_books(reader_id))
		if (book_base.copies == 0) or (active_books_count == 3):
			return False

		return await self.add_borrow(book_id=book_id, reader_id=reader_id)

	async def add_borrow(self, book_id: str, reader_id: str):

		if (await self.book_copies_reduce(book_id=book_id)):
			BNBook = BorrowNewBook(reader_id=UUID(reader_id), book_id=UUID(book_id))

			id_ = await self.borrow_book_dbm.create(BNBook)
			return id_
		else:
			return False

	async def book_copies_reduce(self,book_id: str):
		book_dbm = BookDBM(self.db)
		if await book_dbm.copies_reduce(book_id):
			return True
		else:
			return False