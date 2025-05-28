from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import JSONResponse

from app.models.book import BookRegisterDatas, DeleteBookDatas
from app.db.session import get_db
from app.services.verification import is_admin, is_book
from app.services.auth.book_auth import delete_book

from typing import AsyncGenerator

router = APIRouter(
	prefix="/delete",
	tags=["delete"])

@router.post("/")
async def delete_book_post(DBDatas: DeleteBookDatas,
						db: AsyncGenerator = Depends(get_db),
						jwt: str = Cookie(None)):
	"""
    For delete book

    db -- Session from the database
    DBDatas -- Data delete
    jwt -- The JWT ID from admin
    """
	if await is_admin(db, jwt):
		bookDB = await is_book(db, DBDatas.id)
		if bookDB:
			await delete_book(db, book_id=str(bookDB.id))
			return JSONResponse(status_code=200, content={"success":True,"message":"книга удалена"})
		else:
			return JSONResponse(status_code=400, content={"success":False,"message":"книга не найдена"})
	else:
		return JSONResponse(status_code=400, content={"success":False,"message":"вы не администратор"})
