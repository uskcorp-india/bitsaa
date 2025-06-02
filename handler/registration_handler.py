from dao.user_dao import register_user_in_db
from validators.user_validator import validate_user_data

async def register_user(data):
    validate_user_data(data)
    result = await register_user_in_db(data)
    return {"message": "User registered successfully", "user_id": result['user_id']}
