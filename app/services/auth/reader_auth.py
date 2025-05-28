from app.models.reader import ReaderRegisterDatas, ReaderLoginDatas
from app.db.crud.reader import DataBaseManager

from typing import AsyncGenerator

async def register(db: AsyncGenerator, RRDatas: ReaderRegisterDatas):
	"""
	Register reader
	
	db -- Session from the database
	RRDatas -- Registration data
	"""
	dbm = DataBaseManager(db)
	try:
		return await dbm.create(RRDatas)
	except Exception as e:
		return None

async def login(db: AsyncGenerator, RLDatas: ReaderLoginDatas):
	"""
	They check the data to log in to the account

	db -- Session from the database
	RLDatas -- login data
	"""
	dbm = DataBaseManager(db)
	return await dbm.login(**RLDatas.model_dump())