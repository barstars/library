from app.db.crud.admin import DataBaseManager as ADataBaseManager
from app.db.crud.reader import DataBaseManager as RDataBaseManager

from .generate_jwt import decode_access_token

from typing import AsyncGenerator



async def is_admin(db: AsyncGenerator, jwt: str) -> bool:
	data = await decode_access_token(jwt)
	if data:
		id_ = data.get("id")
		if id_:
			dbm = ADataBaseManager(db)
			datas = await dbm.get_by_id(id_)
			if datas:
				return True
			else:
				return False
		else:
			return False
	else:
		return False

async def is_reader(db: AsyncGenerator, jwt: str) -> bool:
	data = await decode_access_token(jwt)
	if data:
		id_ = data.get("id")
		if id_:
			dbm = RDataBaseManager(db)
			datas = await dbm.get_by_id(id_)
			if datas:
				return True
			else:
				return False
		else:
			return False
	else:
		return False
