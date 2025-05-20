from fastapi import APIRouter
from . import register

books_router = APIRouter(prefix="/books", tags=["books"])

books_router.include_router(register.router)