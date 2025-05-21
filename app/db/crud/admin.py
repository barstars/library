from app.models.admin import AdminBase, AdminRegisterDatas
from app.services.password_hashing import verify_password, hash_password

from sqlalchemy import select

from typing import AsyncGenerator
from uuid import UUID

class DataBaseManager:
	def __init__(self, db: AsyncGenerator):
		self.db = db

	async def create(self, ARDatas: AdminRegisterDatas):
		datas =ARDatas.model_dump()
		password = datas.pop("password")

		ABase = AdminBase(**datas)
		ABase.password_hash = hash_password(password)

		self.db.add(ABase)
		await self.db.commit()
		return ABase.id

	async def login(self, email:str, password:str):
		result = await self.db.execute(select(AdminBase).where(AdminBase.email == email))
		curr = result.scalars().first()
		if curr and  verify_password(password, curr.password_hash):
			return curr.id
		else:
			return None

	async def get_by_id(self, id_: str):
		result = await self.db.execute(select(AdminBase).where(AdminBase.id == UUID(id_)))
		curr = result.scalars().first()
		return curr