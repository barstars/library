from fastapi import APIRouter
from . import register, login

user_router = APIRouter(prefix="/user", tags=["user"])

user_router.include_router(register.router)
user_router.include_router(login.router)
