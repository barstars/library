from fastapi import FastAPI

from app.api.reader.router import reader_router
from app.api.admin.router import admin_router
from app.api.books.router import books_router

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

app.include_router(reader_router)
app.include_router(admin_router)
app.include_router(books_router)