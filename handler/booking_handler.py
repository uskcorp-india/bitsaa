from dao.booking_dao import create_booking_in_db, is_room_available
from validators.booking_validator import validate_booking_data

async def create_booking(data):
    validate_booking_data(data)  # raise exception if invalid

    room_id = data['room_id']
    if not await is_room_available(room_id, data['date']):
        return {"error": "Room not available"}

    result = await create_booking_in_db(data)
    return {"message": "Booking successful", "booking_id": result['booking_id']}
