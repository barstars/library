from fastapi import APIRouter, Depends, Cookie

from app.models.book import BookRegisterDatas
from app.db.session import get_db
from app.services.verification import is_admin
from app.services.auth.book_auth import register

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
		else:
			return {"data":"ISBN уже существует"}
	else:
		return {"data":"вы не администратор"}