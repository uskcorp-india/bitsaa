from dao.room_dao import get_all_rooms_from_db

async def get_rooms():
    rooms = await get_all_rooms_from_db()
    return {"rooms": rooms}
