from app.models.borrow_book import BorrowNewBook
from app.models.book import BookBase
from app.models.reader import ReaderBase

from app.db.crud import borrow_book, book

from .get_data import edit_id_for_jwt

from uuid import UUID
from typing import AsyncGenerator


class NewBorrowedBook:
	def __init__(self, db: AsyncGenerator):
		self.db = db
		self.borrow_book_dbm = borrow_book.DataBaseManager(self.db)

	async def new_borrow(self, book_base: BookBase, reader_base: ReaderBase):
		book_id = str(book_base.id)
		reader_id = str(reader_base.id)

		reader_active_books_count = len(await self.borrow_book_dbm.get_reader_active_books(reader_id))
		is_reader_borrowed_this_book = await self.borrow_book_dbm.is_reader_borrowed_this_book(reader_id,book_id)

		if (book_base.copies == 0) or (reader_active_books_count == 3) or is_reader_borrowed_this_book:
			print("book_base.copies:",book_base.copies)
			print("reader_active_books_count:",reader_active_books_count)
			print("is_reader_borrowed_this_book:",is_reader_borrowed_this_book)
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
		book_dbm = book.DataBaseManager(self.db)
		if await book_dbm.copies_reduce(book_id):
			return True
		else:
			return False

class GetReaderBorrows:
	def __init__(self, db: AsyncGenerator):
		self.db = db
		self.borrow_book_dbm = borrow_book.DataBaseManager(self.db)


	async def get_all_borrows(self, reader_id: str) -> list:
		book_dbm = book.DataBaseManager(self.db)
		borrowDB_list = await self.borrow_book_dbm.get_reader_all_books(reader_id)

		books_info = []
		for borrowDB in borrowDB_list:

			borrow_book_info_dict = await self.borrow_book_dbm.get_info(str(borrowDB.id))
			book_info_dict = await book_dbm.get_info(str(borrowDB.book_id))

			book_info_dict.update(borrow_book_info_dict)
			books_info.append(book_info_dict)

		return books_info