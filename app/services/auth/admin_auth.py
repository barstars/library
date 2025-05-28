from app.models.admin import AdminRegisterDatas, AdminLoginDatas
from app.db.crud.admin import DataBaseManager

from typing import AsyncGenerator

async def register(db: AsyncGenerator, ARDatas: AdminRegisterDatas):
	"""
	Register admin

	db -- Session from the database
	ARDatas -- Registration data
	"""
	dbm = DataBaseManager(db)
	try:
		return await dbm.create(ARDatas)
	except Exception as e:
		return None

async def login(db: AsyncGenerator, ALDatas: AdminLoginDatas):
	"""
	They check the data to log in to the account
	
	db -- Session from the database
	ALDatas -- login data
	"""
	dbm = DataBaseManager(db)
	return await dbm.login(**ALDatas.model_dump())