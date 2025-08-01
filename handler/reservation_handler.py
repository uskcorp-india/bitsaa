import dynamodb.dynamodb_proxy as db
from dao.resort_dao import increment_blocked_room
from utils.logger_factory import get_logger
import validator.reservation_validator as validator
from utils.response_utils import build_response

logger = get_logger(__name__)

def create(reservation: dict):
    reservation_validator = validator.validate(reservation)
    logger.info(f'reservation details: {reservation}')
    if 'errors' in reservation_validator:
        return build_response(reservation_validator['errors'],400)
    else:
        resort_id = reservation.get('resort')['id']
        count = reservation['room_count']
        resort = db.find_resort(resort_id)
        available_rooms = int(resort['available'])
        if available_rooms <= count:
            return build_response(reservation,f"Only {available_rooms} rooms are available, but your trying to book {count} room.")
        reservation_data = db.create_reservation(reservation_validator)
        increment_blocked_room(resort_id,count)
        db.pending_reservation(reservation_data['id'])
        return build_response(reservation_data,'reservation Created Successfully')

def find(reservation_id: str):
    response = db.find_reservation(reservation_id)
    logger.info(response)
    return build_response(response,"reservation Found Successfully")

def update(reservation_id,reservation: dict):
    validated_reservation = validator.validate(reservation)
    logger.info(f'Updating reservation details: {reservation}')

    if 'errors' in validated_reservation:
        return build_response(validated_reservation['errors'], 400)
    else:
        response = db.update_reservation(reservation_id,validated_reservation)
        return build_response(response, 'reservation Updated Successfully')

def delete(reservation_id:str):
    response=db.delete_reservation(reservation_id)
    logger.info(response)
    return build_response(response,message="reservation deleted successfully")