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
        book_dict = await edit_id_for_jwt(key_name="id", dataOUT=BookOUT, dataDB=book)
        books.append(book_dict)
    return books

async def edit_id_for_jwt(dataOUT, dataDB, key_name: str = None) -> dict:
    data_out_dict = dataOUT.from_orm(dataDB).model_dump()
    if key_name:
        jwt_id = await create_access_token({key_name: str(data_out_dict[key_name])})
        data_out_dict[key_name] = jwt_id
    return data_out_dict