from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import JSONResponse

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
	"""
    For register the book

	DBDatas -- Data for register book
    db -- Session from the database
    jwt -- The JWT ID from admin
    """
	if await is_admin(db, jwt):
		id_ = await register(db, BRDatas)
		if id_:
			return JSONResponse(status_code=200, content={"success":True,"message":"зарегистрирован"})
		elif id_ == False:
			return JSONResponse(status_code=400, content={"success":False,"message":"Экземпляр (copies) не могуд быт меньше нуля"})
		else:
			return JSONResponse(status_code=400, content={"success":False,"message":"ISBN уже существует"})
	else:
		return JSONResponse(status_code=400, content={"success":False,"message":"вы не администратор"})


@router.post("/add")
async def add_copies_post(ACDatas: AddCopiesDatas,
						db: AsyncGenerator = Depends(get_db),
						jwt: str = Cookie(None)):
	if await is_admin(db, jwt):
		bookDB = await is_book(db, ACDatas.id)
		if bookDB:
			id_ = await add_copies_for_book(db, book_id=str(bookDB.id), copies=ACDatas.copies)
			if id_:
				return JSONResponse(status_code=200, content={"success":True,"message":"добавлено"})
			else:
				return JSONResponse(status_code=400, content={"success":False,"message":"не возможно добавить экземпляр"})
		else:
			return JSONResponse(status_code=400, content={"success":False,"message":"книга не найдена"})
	else:
		return JSONResponse(status_code=400, content={"success":False,"message":"вы не администратор"})

