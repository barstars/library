from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.models.reader import ReaderLoginDatas
from app.db.session import get_db
from app.services.auth.reader_auth import login
from app.services.generate_jwt import create_access_token

import json
from typing import AsyncGenerator

router = APIRouter(
    prefix="/login",
    tags=["login"])

@router.post("/")
async def login_post(RLDatas: ReaderLoginDatas,
                    response: Response,
                    db: AsyncGenerator = Depends(get_db)):
    id_ = await login(db, RLDatas)
    if id_:
        id_ = str(id_)
        data = {"id":id_}
        jwt = await create_access_token(data)
        month = 5
        max_age = (((60*60)*24)*(30*month))
        response = JSONResponse(status_code=200, content={"success":True,"message":"вы вошли"})
        response.set_cookie(key="jwt", value=jwt, max_age=max_age)
        return response
    else:
        return JSONResponse(status_code=400, content={"success":False,"message":"войти не удалось"})