from fastapi import APIRouter, Depends, Cookie

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
	reader_base = await is_reader(db, jwt)

	if reader_base:
		borrow_jwt = return_book_datas.id
		borrow_base = await is_borrow(db, borrow_jwt)

		if borrow_base:
			if borrow_base.return_date == None:
				return_book = ReturnBook(db)

				is_return = await return_book.return_book(str(borrow_base.id))
				return {"data":"Книга возвращено"}
			else:
				return {"data":"Книга уже возвращено"}
		else:
			return {"data":"Не полученный книга"}
	else:
		return {"data":"вы не читатель"}
