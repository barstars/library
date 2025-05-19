from app.models.admin import AdminBase, AdminRegisterDatas
from app.services.password_hashing import verify_password

from sqlalchemy import select

from typing import AsyncGenerator
from uuid import UUID

class DataBaseManager:
	def __init__(self, db: AsyncGenerator):
		self.db = db

	async def create_user(self, ARDatas: AdminRegisterDatas):
		datas =ARDatas.model_dump()
		password = datas.pop("password")

		ARDatas = AdminBase(**datas)
		ARDatas.password_add(password)

		self.db.add(ARDatas)
		await self.db.commit()
		return ARDatas.id

	async def login(self, email:str, password:str):
		result = await self.db.execute(select(AdminBase).where(AdminBase.email == email))
		curr = result.scalars().first()
		if curr and curr.verify_password(password):
			return curr.id
		else:
			return None

	async def get_by_id(self, id_: str):
		result = await self.db.execute(select(AdminBase).where(AdminBase.id == UUID(id_)))
		curr = result.scalars().first()
		return curr