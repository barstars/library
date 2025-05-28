from app.services.generate_jwt import create_access_token


async def db_to_dict(dataOUT, dataDB) -> dict:
	"""
	DB to dict

	dataOUT -- pydantic model for to dict
	dataDB -- Data from Base
	"""
    data_out_dict = dataOUT.from_orm(dataDB).model_dump()
    return data_out_dict

async def edit_id_for_jwt(data: dict, key_name: str):
	"""
	Edit dict data from key_name to JWT. Exemple: data={"id":"ctfvgybhunjmihgbvtfr-asda", "username":"admin"} key_name="id" -> {"id":"43ge453e4tg3w4tw3t", "username":"admin"}
	
	data -- dict data
	key_name -- key name from data
	"""
    jwt = await create_access_token({key_name:str(data[key_name])})
    data[key_name] = jwt
    return data