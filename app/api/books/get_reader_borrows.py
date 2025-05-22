from fastapi import APIRouter, Depends, Cookie

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
		return {"data":await get_reader_borrows.get_all_borrows(reader_id)}
	else:
		return {"data":"вы не читатель"}
