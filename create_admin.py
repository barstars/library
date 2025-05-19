from app.db.crud.admin import DataBaseManager
from app.db.session import get_db
from app.models.admin import AdminRegisterDatas

import asyncio
from typing import AsyncGenerator


async def run():
	async for db in get_db():
	    dbm = DataBaseManager(db)

	    username = "admin" #input("Username")
	    email = "admin@gmail.com" #input("Email")
	    password = "admin" #input("Password")

	    ARDatas = AdminRegisterDatas(username=username,email=email,password=password)
	    id_ = await dbm.create_user(ARDatas)
	    print(id_)
	    print(type(id_))


asyncio.run(run())