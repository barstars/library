from app.models.book import BookRegisterDatas
from app.db.crud.book import DataBaseManager

from typing import AsyncGenerator

async def register(db: AsyncGenerator, BRDatas: BookRegisterDatas):
	dbm = DataBaseManager(db)
	try:
		return await dbm.create(BRDatas)
	except Exception as e:
		return None