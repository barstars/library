from app.db.crud.book import DataBaseManager as BookDBManager
from app.models.book import BookDB_for_pydantic
from app.services.generate_jwt import create_access_token

from typing import AsyncGenerator

async def get_all_books(db: AsyncGenerator):
    dbm = BookDBManager(db)
    booksDB = await dbm.fetch_all_books()
    if not booksDB:
        return None

    books = []
    for book in booksDB:
        book_data = BookDB_for_pydantic.from_orm(book).model_dump()
        jwt_id = await create_access_token({"id": str(book_data["id"])})
        book_data["id"] = jwt_id
        books.append(book_data)
    return books