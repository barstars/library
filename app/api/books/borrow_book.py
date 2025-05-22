from fastapi import APIRouter, Depends, Cookie

from app.models.borrow_book import BorrowedBookDatas
from app.db.session import get_db
from app.services.verification import is_reader, is_book
from app.services.book_use import NewBorrowedBook

from typing import AsyncGenerator

router = APIRouter(
	prefix="/borrow",
	tags=["borrow"])

@router.post("/")
async def borrow_book_post(BRDatas: BorrowedBookDatas,
						db: AsyncGenerator = Depends(get_db),
						jwt: str = Cookie(None)):
	reader_base = await is_reader(db, jwt)
	book_base = await is_book(db, BRDatas.id)

	if reader_base:
		if book_base:
			new_borrowed_book = NewBorrowedBook(db)
			id_ = await new_borrowed_book.new_borrow(reader_base=reader_base, book_base=book_base)

			if id_:
				return {"data":"книга получено"}
			else:
				return {"data":"книга не получено"}
		else:
			return {"data":"книга не существует"}
	else:
		return {"data":"вы не читатель"}
