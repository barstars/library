from app.core.config import setting
from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=setting.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.HESHALGORITHM)

async def decode_access_token(token: str) -> dict:
	try:
		payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.HESHALGORITHM])
		return payload
	except JWTError:
		return None