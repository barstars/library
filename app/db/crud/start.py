from app.db.base import Base
from app.db.session import engine

async def action_all_table():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)