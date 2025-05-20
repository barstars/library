from fastapi import APIRouter, Depends, Response

from app.models.admin import AdminLoginDatas
from app.db.session import get_db
from app.services.auth.admin_auth import login
from app.services.generate_jwt import create_access_token

import json
from typing import AsyncGenerator

router = APIRouter(
	prefix="/login",
	tags=["login"])

@router.post("/")
async def login_post(ALDatas: AdminLoginDatas,
                    response: Response,
                    db: AsyncGenerator = Depends(get_db)):
    id_ = await login(db, ALDatas)
    if id_:
        id_ = str(id_)
        data = {"id":id_}
        jwt = await create_access_token(data)
        month = 5
        max_age = (((60*60)*24)*(30*month))
        response.set_cookie(key="jwt", value=jwt, max_age=max_age)
        return {"data":id_}
    else:
        return {"data":"войти не удалось"}