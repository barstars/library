from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import JSONResponse

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
	"""
    For borrow book

    db -- Session from the database
    BRDatas -- Data for borrow book
    jwt -- The JWT ID from reader
    """
	reader_base = await is_reader(db, jwt)
	book_base = await is_book(db, BRDatas.id)

	if reader_base:
		if book_base:
			new_borrowed_book = NewBorrowedBook(db)
			id_ = await new_borrowed_book.new_borrow(reader_base=reader_base, book_base=book_base)

			if id_:
				return JSONResponse(status_code=200, content={"success":True,"message":"Книга получено"})
			else:
				return JSONResponse(status_code=400, content={"success":False,"message":"книга не получено"})
		else:
			return JSONResponse(status_code=400, content={"success":False,"message":"книга не существует"})
	else:
		return JSONResponse(status_code=400, content={"success":False,"message":"вы не читатель"})
