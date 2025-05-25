from fastapi import FastAPI

from app.api.reader.router import reader_router
from app.api.admin.router import admin_router
from app.api.books.router import books_router


app = FastAPI()

app.include_router(reader_router)
app.include_router(admin_router)
app.include_router(books_router)