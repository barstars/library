from app.models.admin import AdminRegisterDatas, AdminLoginDatas
from app.db.crud.admin import DataBaseManager

from typing import AsyncGenerator

async def register(db: AsyncGenerator, ARDatas: AdminRegisterDatas):
	dbm = DataBaseManager(db)
	try:
		return await dbm.create(ARDatas)
	except Exception as e:
		return None

async def login(db: AsyncGenerator, ALDatas: AdminLoginDatas):
	dbm = DataBaseManager(db)
	return await dbm.login(**ALDatas.model_dump())