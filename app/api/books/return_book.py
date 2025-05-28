from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.services.verification import is_reader, is_borrow
from app.services.book_use import ReturnBook
from app.models.borrow_book import ReturnBookDatas

from typing import AsyncGenerator

router = APIRouter(
	prefix="/returnbook",
	tags=["returnbook"])

@router.post("/")
async def return_book(return_book_datas:ReturnBookDatas,
					db: AsyncGenerator = Depends(get_db),
					jwt: str = Cookie(None)):
	"""
    For return the book

	return_book_datas -- Data for return book
    db -- Session from the database
    jwt -- The JWT ID from reader
    """
	reader_base = await is_reader(db, jwt)

	if reader_base:
		borrow_jwt = return_book_datas.id
		borrow_base = await is_borrow(db, borrow_jwt)

		if borrow_base:
			if borrow_base.return_date == None:
				return_book = ReturnBook(db)

				is_return = await return_book.return_book(str(borrow_base.id))
				return JSONResponse(status_code=200, content={"success":True,"message":"Книга возвращено"})
			else:
				return JSONResponse(status_code=400, content={"success":False,"message":"Книга уже возвращено"})
		else:
			return JSONResponse(status_code=400, content={"success":False,"message":"Не полученный книга"})
	else:
		return JSONResponse(status_code=400, content={"success":False,"message":"Вы не читатель"})
