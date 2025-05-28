from app.models.book import BookBase, BookRegisterDatas

from sqlalchemy import select

from typing import AsyncGenerator
from uuid import UUID

class DataBaseManager:
	def __init__(self, db: AsyncGenerator):
		"""
		Book database manager
		
		db -- Session from the database
		"""
		self.db = db

	async def create(self, BRDatas: BookRegisterDatas):
		"""
		Create new data

		BRDatas -- Registration data
		"""
		BBase = BookBase(**BRDatas.model_dump())

		self.db.add(BBase)
		await self.db.commit()
		return BBase.id

	async def copies_add(self, id_: str, copies:int=1) -> bool:
		"""
		Add copies from the book

		id_ -- Id from book
		copies -- Number of copies to add. Default 1.
		"""
		curr = await self.get_by_id(id_)
		if curr:
			if (curr.copies + copies >= 0):
				await curr.copies_add(copies)
				await self.db.commit()
				return True
			else:
				return False
		else:
			return False

	async def copies_reduce(self, id_: str) -> bool:
		"""
		Reduce copies from the book

		id_ -- Id from book
		"""
		curr = await self.get_by_id(id_)
		if curr:
			if (curr.copies > 0):
				await curr.copies_reduce()
				await self.db.commit()
				return True
			else:
				return False
		else:
			return False

	async def fetch_all_books(self):
		"""
		Get all books
		"""
		result = await self.db.execute(select(BookBase))
		return result.scalars().all()

	async def get_by_id(self, id_: str):
		"""
		Search by id

		id_ -- Id from book
		"""
		result = await self.db.execute(select(BookBase).where(BookBase.id == UUID(id_)))
		curr = result.scalars().first()
		return curr

	async def delete(self, id_: str):
		"""
		Delete data

		id_ -- Id from book
		"""
		book = await self.get_by_id(id_)
		await self.db.delete(book)
		await self.db.commit()


	async def get_info(self, id_: str):
		"""
		Get info from book

		id_ -- Id from book
		"""
		result = await self.db.execute(select(BookBase).where(BookBase.id == UUID(id_)))
		curr = result.scalars().first()
		info = await curr.get_info()
		return info