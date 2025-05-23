from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.services.verification import is_reader
from app.services.book_use import GetReaderBorrows

from typing import AsyncGenerator

router = APIRouter(
	prefix="/getborrows",
	tags=["getborrows"])

@router.get("/all")
async def get_reader_borrows_post(db: AsyncGenerator = Depends(get_db),
								jwt: str = Cookie(None)):
	reader_base = await is_reader(db, jwt)

	if reader_base:
		reader_id = str(reader_base.id)
		get_reader_borrows = GetReaderBorrows(db)
		return JSONResponse(status_code=200, content={"success":True,"message":"Успех",
			"data":await get_reader_borrows.get_all_borrows(reader_id)})
	else:
		return JSONResponse(status_code=400, content={"success":False,"message":"вы не читатель"})

@router.get("/active")
async def get_reader_borrows_post(db: AsyncGenerator = Depends(get_db),
								jwt: str = Cookie(None)):
	reader_base = await is_reader(db, jwt)

	if reader_base:
		reader_id = str(reader_base.id)
		get_reader_borrows = GetReaderBorrows(db)
		return JSONResponse(status_code=200, content={"success":True,"message":"Успех",
			"data":await get_reader_borrows.get_active_borrows(reader_id)})
	else:
		return JSONResponse(status_code=400, content={"success":False,"message":"вы не читатель"})
