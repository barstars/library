from app.models.book import BookRegisterDatas
from app.db.crud.book import DataBaseManager

from typing import AsyncGenerator

async def register(db: AsyncGenerator, BRDatas: BookRegisterDatas):
	if BRDatas.copies < 0:
		return False
	dbm = DataBaseManager(db)
	try:
		return await dbm.create(BRDatas)
	except Exception as e:
		return None