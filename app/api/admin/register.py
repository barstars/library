from fastapi import APIRouter, Depends, Request, Cookie
from fastapi.responses import JSONResponse

from app.models.admin import AdminRegisterDatas
from app.db.session import get_db
from app.services.verification import is_admin
from app.services.auth.admin_auth import register

import json
from typing import AsyncGenerator

router = APIRouter(
	prefix="/register",
	tags=["register"])

@router.post("/")
async def register_post(ARDatas: AdminRegisterDatas,
						request: Request,
						db: AsyncGenerator = Depends(get_db),
						jwt: str = Cookie(None)):
	if await is_admin(db, jwt):
		id_ = await register(db, ARDatas)
		if id_:
			return JSONResponse(status_code=200, content={"success":True,"message":"зарегистрирован"})
		else:
			return JSONResponse(status_code=400, content={"success":False,"message":"email уже существует"})
	else:
		return JSONResponse(status_code=400, content={"success":False,"message":"вы не администратор"})