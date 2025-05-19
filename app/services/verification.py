from app.db.crud.admin import DataBaseManager

from .generate_jwt import decode_access_token

from typing import AsyncGenerator



async def is_admin(db: AsyncGenerator, jwt: str) -> bool:
	data = await decode_access_token(jwt)
	if data:
		id_ = data.get("id")
		if id_:
			dbm = DataBaseManager(db)
			datas = await dbm.get_by_id(id_)
			if datas:
				return True
			else:
				return False
		else:
			return False
	else:
		return False