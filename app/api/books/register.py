from fastapi import APIRouter, Depends, Cookie

from app.models.book import BookRegisterDatas, AddCopiesDatas
from app.db.session import get_db
from app.services.verification import is_admin, is_book
from app.services.auth.book_auth import register, add_copies_for_book

from typing import AsyncGenerator

router = APIRouter(
	prefix="/register",
	tags=["register"])

@router.post("/")
async def register_post(BRDatas: BookRegisterDatas,
						db: AsyncGenerator = Depends(get_db),
						jwt: str = Cookie(None)):
	if await is_admin(db, jwt):
		id_ = await register(db, BRDatas)

		if id_:
			return {"data":"зарегистрирован"}
		elif id_ == False:
			return {"data":"Экземпляр (copies) не могуд быт меньше нуля"}
		else:
			return {"data":"ISBN уже существует"}
	else:
		return {"data":"вы не администратор"}

@router.post("/add")
async def add_copies_post(ACDatas: AddCopiesDatas,
						db: AsyncGenerator = Depends(get_db),
						jwt: str = Cookie(None)):
	if await is_admin(db, jwt):
		bookDB = await is_book(db, ACDatas.id)
		if bookDB:
			id_ = await add_copies_for_book(db, book_id=str(bookDB.id), copies=ACDatas.copies)

			if id_:
				return {"data":"добавлено"}
			else:
				return {"data":"не возможно добавить экземпляр"}
		else:
			return {"data":"книга не найдена"}
	else:
		return {"data":"вы не администратор"}
