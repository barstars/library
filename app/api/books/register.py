from fastapi import APIRouter, Depends, Cookie

from app.models.reader import ReaderRegisterDatas
from app.db.session import get_db
from app.services.verification import is_admin
from app.services.auth.reader_auth import register

import json
from typing import AsyncGenerator

router = APIRouter(
	prefix="/register",
	tags=["register"])

@router.post("/")
async def register_post(RRDatas: ReaderRegisterDatas,
						db: AsyncGenerator = Depends(get_db),
						jwt: str = Cookie(None)):
	if await is_admin(db, jwt):
		id_ = await register(db, RRDatas)
		if id_:
			return {"data":"зарегистрирован"}
		else:
			return {"data":"email уже существует"}
	else:
		return {"data":"вы не администратор"}