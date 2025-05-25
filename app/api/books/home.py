from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.services.book_use import get_all_books

from typing import AsyncGenerator

router = APIRouter(
	prefix="",
	tags=["book_home"])

@router.get("/")
async def get_books(db: AsyncGenerator = Depends(get_db)):
	books = await get_all_books(db)
	return JSONResponse(status_code=200, content={"success":True,"message":"Успех",
		"data":books})