from app.core.config import setting
from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt


async def create_access_token(data: dict) -> str:
	"""
	Heshing dict to JWT
	data -- dict. example: {"id":"29e8wj3l4-s83j-d8r0-fjtk59sd"} -> "wuiehf2oefn28o73f8owjd208qf7h2q083f7h2q807fh2q83f7h2837h298f"
	"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=setting.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.HESHALGORITHM)

async def decode_access_token(token: str) -> dict:
	"""
	ReHeshing JWT to dict
	token -- JWT. example: "wuiehf2oefn28o73f8owjd208qf7h2q083f7h2q807fh2q83f7h2837h298f" -> {"id":"29e8wj3l4-s83j-d8r0-fjtk59sd"}
	"""
	try:
		payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.HESHALGORITHM])
		return payload
	except Exception:
		return None