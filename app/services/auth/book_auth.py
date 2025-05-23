from app.models.book import BookRegisterDatas
from app.db.crud.book import DataBaseManager as BookDBM
from app.db.crud.borrow_book import DataBaseManager as BorrowBookDBM

from typing import AsyncGenerator

async def register(db: AsyncGenerator, BRDatas: BookRegisterDatas):
	if BRDatas.copies < 0:
		return False
	dbm = BookDBM(db)
	try:
		return await dbm.create(BRDatas)
	except Exception as e:
		return None

async def add_copies_for_book(db: AsyncGenerator, book_id: str, copies: int):
	dbm = BookDBM(db)
	return await dbm.copies_add(book_id, copies=copies)

async def delete_book(db: AsyncGenerator, book_id: str):
	borrow_book_dbm = BorrowBookDBM(db)
	await borrow_book_dbm.delete_by_all_book(book_id)

	book_dbm = BookDBM(db)
	await book_dbm.delete(book_id)