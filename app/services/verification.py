from app.db.crud.admin import DataBaseManager as AdminDBM
from app.db.crud.reader import DataBaseManager as ReaderDBM
from app.db.crud.book import DataBaseManager as BookDBM
from app.db.crud.borrow_book import DataBaseManager as BorrowBookDBM

from .generate_jwt import decode_access_token

from typing import AsyncGenerator



async def is_admin(db: AsyncGenerator, jwt: str):
	"""
	Check whether it is an admin or not,
	if the admin returns his data in the base type,
	if not, then False

	db -- Session from the database
	jwt -- The JWT ID from admin
	"""
	data = await decode_access_token(jwt)
	if data:
		id_ = data.get("id")
		if id_:
			dbm = AdminDBM(db)
			datas = await dbm.get_by_id(id_)
			if datas:
				return datas
			else:
				return False
		else:
			return False
	else:
		return False

async def is_reader(db: AsyncGenerator, jwt: str):
	"""
	Check whether it is an reader or not,
	if the reader returns his data in the base type,
	if not, then False

	db -- Session from the database
	jwt -- The JWT ID from reader
	"""
	data = await decode_access_token(jwt)
	if data:
		id_ = data.get("id")
		if id_:
			dbm = ReaderDBM(db)
			datas = await dbm.get_by_id(id_)
			if datas:
				return datas
			else:
				return False
		else:
			return False
	else:
		return False

async def is_book(db: AsyncGenerator, jwt: str):
	"""
	Check whether it is an book or not,
	if the book returns his data in the base type,
	if not, then False

	db -- Session from the database
	jwt -- The JWT ID from book
	"""
	data = await decode_access_token(jwt)
	if data:
		id_ = data.get("id")
		if id_:
			dbm = BookDBM(db)
			datas = await dbm.get_by_id(id_)
			if datas:
				return datas
			else:
				return False
		else:
			return False
	else:
		return False

async def is_borrow(db: AsyncGenerator, jwt: str):
	"""
	Check whether it is an borrow or not,
	if the borrow returns his data in the base type,
	if not, then False
	
	db -- Session from the database
	jwt -- The JWT ID from borrow
	"""
	data = await decode_access_token(jwt)
	if data:
		id_ = data.get("id")
		if id_:
			dbm = BorrowBookDBM(db)
			datas = await dbm.get_by_id(id_)
			if datas:
				return datas
			else:
				return False
		else:
			return False
	else:
		return False