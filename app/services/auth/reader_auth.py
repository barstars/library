from app.models.reader import ReaderRegisterDatas, ReaderLoginDatas
from app.db.crud.reader import DataBaseManager

from typing import AsyncGenerator

async def register(db: AsyncGenerator, RRDatas: ReaderRegisterDatas):
	dbm = DataBaseManager(db)
	try:
		return await dbm.create_user(RRDatas)
	except Exception as e:
		return None

async def login(db: AsyncGenerator, RLDatas: ReaderLoginDatas):
	dbm = DataBaseManager(db)
	return await dbm.login(**RLDatas.model_dump())