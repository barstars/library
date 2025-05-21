from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.services.get_data import get_all_books

from typing import AsyncGenerator

router = APIRouter(
	prefix="",
	tags=["book_home"])

@router.get("/")
async def get_books(db: AsyncGenerator = Depends(get_db)):
	books = await get_all_books(db)
	return {"books":books}