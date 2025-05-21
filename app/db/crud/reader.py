from app.models.reader import ReaderBase, ReaderRegisterDatas
from app.services.password_hashing import verify_password, hash_password

from sqlalchemy import select

from typing import AsyncGenerator
from uuid import UUID

class DataBaseManager:
	def __init__(self, db: AsyncGenerator):
		self.db = db

	async def create(self, RRDatas: ReaderRegisterDatas):
		datas =RRDatas.model_dump()
		password = datas.pop("password")

		RBase = ReaderBase(**datas)
		RBase.password_hash = hash_password(password)

		self.db.add(RBase)
		await self.db.commit()
		return RBase.id

	async def login(self, email:str, password:str):
		result = await self.db.execute(select(ReaderBase).where(ReaderBase.email == email))
		curr = result.scalars().first()
		if curr and verify_password(password, curr.password_hash):
			return curr.id
		else:
			return None

	async def get_by_id(self, id_: str):
		result = await self.db.execute(select(ReaderBase).where(ReaderBase.id == UUID(id_)))
		curr = result.scalars().first()
		return curr