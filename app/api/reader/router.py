from fastapi import APIRouter
from . import register, login

reader_router = APIRouter(prefix="/reader", tags=["reader"])

reader_router.include_router(register.router)
reader_router.include_router(login.router)
