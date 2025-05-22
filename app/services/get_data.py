from app.db.crud.book import DataBaseManager as BookDBManager
from app.models.book import BookOUT
from app.services.generate_jwt import create_access_token

from typing import AsyncGenerator

async def get_all_books(db: AsyncGenerator):
    dbm = BookDBManager(db)
    booksDB = await dbm.fetch_all_books()
    if not booksDB:
        return None

    books = []
    for book in booksDB:
        book_dict = await db_to_dict(dataOUT=BookOUT, dataDB=book)
        book_dict_jwt = await edit_id_for_jwt(data=book_dict, key_name="id")
        books.append(book_dict_jwt)
    return books

async def db_to_dict(dataOUT, dataDB) -> dict:
    data_out_dict = dataOUT.from_orm(dataDB).model_dump()
    return data_out_dict

async def edit_id_for_jwt(data: dict, key_name: str):
    jwt = await create_access_token({key_name:str(data[key_name])})
    data[key_name] = jwt
    return data