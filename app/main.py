from fastapi import FastAPI

# from app.api.user import router as user_router
from app.api.admin.router import admin_router

from app.db.crud.start import action_all_table

from contextlib import asynccontextmanager

app = FastAPI()

@app.on_event("startup")
async def startup_event():
	await action_all_table()
	print("STRATUP")

@app.on_event("shutdown")
async def shutdown_event():
	print("OUT")

# app.include_router(user_router.router)
app.include_router(admin_router)