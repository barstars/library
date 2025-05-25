from app.services.generate_jwt import create_access_token


async def db_to_dict(dataOUT, dataDB) -> dict:
    data_out_dict = dataOUT.from_orm(dataDB).model_dump()
    return data_out_dict

async def edit_id_for_jwt(data: dict, key_name: str):
    jwt = await create_access_token({key_name:str(data[key_name])})
    data[key_name] = jwt
    return data