from fastapi import APIRouter
from . import register, home, borrow_book, get_reader_borrows, return_book

books_router = APIRouter(prefix="/book", tags=["book"])

books_router.include_router(register.router)
books_router.include_router(home.router)
books_router.include_router(borrow_book.router)
books_router.include_router(get_reader_borrows.router)
books_router.include_router(return_book.router)