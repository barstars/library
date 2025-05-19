from fastapi import APIRouter
from . import register, login

admin_router = APIRouter(prefix="/admin", tags=["admin"])

admin_router.include_router(register.router)
admin_router.include_router(login.router)
